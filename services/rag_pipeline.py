import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
import sys
import logging
from pathlib import Path
from typing import Dict, List, Tuple

from services.memory import Memory
from services.semantic_cache import SemanticCache
from prompts.registry import PromptRegistry
from security.input_guard import InputGuard
from security.output_guard import OutputGuard
from observability.tracing import Tracing
from agents.adaptive_router import AdaptiveRouter
from agents.decomposer import Decomposer
from agents.document_grader import DocumentGrader
from security.content_guard import ContentGuard
from observability.cost_tracking import CostTracker
from evaluation.online_monitor import OnlineMonitor
from datetime import datetime

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, vector_db_path: str = None, use_small_model: bool = None):
        """
        Initialize Gemini RAG System Pipeline
        """
        if use_small_model is None:
            is_cloud = any([
                os.getenv('RAILWAY_ENVIRONMENT_NAME'),
                os.getenv('RENDER') == 'true',
                os.getenv('DYNO'),
                os.getenv('VERCEL'),
            ])
            use_small_model = is_cloud
            
        self.use_small_model = use_small_model
        model_name = "gemini-rag-small" if use_small_model else "gemini-rag"
        logger.info(f"Using vector database: {model_name}")
        
        if vector_db_path is None:
            project_root = Path(__file__).parent.parent
            possible_paths = [
                project_root / "model" / model_name,
                project_root / "src" / "model" / model_name,
                project_root / model_name,
                Path("/app/model") / model_name,
                Path("/app") / model_name,
                Path("/opt/render/project/src/model") / model_name,
                Path("/opt/render/project") / model_name,
            ]
            self.vector_db_path = None
            for path in possible_paths:
                if path.exists():
                    self.vector_db_path = path
                    logger.info(f"Found vector database at: {path}")
                    break
            
            if not self.vector_db_path:
                self.vector_db_path = possible_paths[0]
                logger.warning(f"Vector DB not found, using default: {self.vector_db_path}")
        else:
            self.vector_db_path = Path(vector_db_path)
            
        self.vector_db = self._load_vector_db()
        self.retriever = self.vector_db.as_retriever(search_kwargs={"k": 3}) if self.vector_db else None
        self.model = self._initialize_gemini()
        self.memory = Memory()
        self.input_guard = InputGuard()
        self.output_guard = OutputGuard()
        self.tracing = Tracing()
        self.cache = SemanticCache()
        
        # New layers & agents
        self.router = AdaptiveRouter()
        self.decomposer = Decomposer()
        self.grader = DocumentGrader()
        self.content_guard = ContentGuard()
        self.cost_tracker = CostTracker()
        self.monitor = OnlineMonitor()
        
        logger.info("RAG Pipeline initialized successfully!")

    def _load_vector_db(self):
        logger.info(f"🔍 Looking for vector database at: {self.vector_db_path}")
        try:
            if not self.vector_db_path.exists():
                logger.warning(f"Vector DB not found at {self.vector_db_path}. Will run without context.")
                return None
            
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
            vector_db = FAISS.load_local(str(self.vector_db_path), embeddings, allow_dangerous_deserialization=True)
            logger.info("✅ Vector database loaded successfully!")
            return vector_db
        except Exception as e:
            logger.error(f"Failed to load vector database: {e}")
            return None

    def _initialize_gemini(self):
        project_root = Path(__file__).parent.parent
        env_path = project_root / ".env"
        
        # Load from .env if it exists
        if env_path.exists():
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key.strip()] = value.strip().strip("'\"")
            logger.info("✅ Loaded environment variables from .env")
            
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment or .env file")
        
        if api_key:
            genai.configure(api_key=api_key)
            
        # Define Function Calling tool
        def get_current_time():
            """Returns the current date and time."""
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Using gemini-2.5-flash as requested
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            tools=[get_current_time]
        )  
        logger.info("✅ Gemini 2.5 Flash model initialized with tools!")
        return model

    def ask_question(self, question: str, use_history: bool = True) -> Dict:
        import time
        start_time = time.time()
        trace_id = f"req_{hash(question) % 10000}"
        self.tracing.start_trace(trace_id, "ask_question")
        try:
            # 1. Check Input Security (Safety & Alignment / Guardrails)
            is_safe, msg = self.input_guard.check(question)
            if not is_safe:
                self.tracing.end_trace(trace_id)
                return {'success': False, 'answer': msg, 'sources_count': 0}

            # 2. Check Cache
            cached_ans = self.cache.get(question)
            if cached_ans:
                self.tracing.end_trace(trace_id)
                return {'success': True, 'answer': cached_ans, 'sources_count': 0, 'cached': True}

            # 3. Agent Orchestration & Multi-agent Systems: Route intent
            intent = self.router.route(question)
            logger.info(f"Routed intent: {intent}")
            
            # Decompose complex questions
            sub_queries = self.decomposer.decompose(question)
            
            # 4. Retrieve Context & Retrieval Quality (Grounding & Embeddings)
            valid_docs = []
            if self.retriever and intent != "chitchat":
                for sq in sub_queries:
                    docs = self.retriever.invoke(sq)
                    for doc in docs:
                        # Document Grader filters out irrelevant chunks (Chunking & Retrieval Quality)
                        if self.grader.grade(doc.page_content, sq):
                            valid_docs.append(doc)
            
            # 5. Data Privacy: Content Guard scrubs PII
            safe_context_chunks = []
            for d in valid_docs:
                clean, sanitized = self.content_guard.sanitize(d.page_content)
                safe_context_chunks.append(sanitized)
                
            # Remove duplicates and combine
            safe_context_chunks = list(set(safe_context_chunks))
            context = "\n\n".join(safe_context_chunks)
            sources_count = len(safe_context_chunks)
                
            # 6. Get Memory Context (State Management & Context Windows)
            history_text = self.memory.get_history_text() if use_history else ""
            
            # 7. Prompt Engineering: Build Prompt (System Prompts)
            prompt = PromptRegistry.get_rag_prompt(context, history_text, question)
            
            # 8. Generate Response (Function calling is available to the model)
            response = self.model.generate_content(prompt)
            answer = response.text
            
            # 9. Token Costs Tracking
            usage = getattr(response, 'usage_metadata', None)
            if usage:
                self.cost_tracker.calculate_cost("gemini-2.5-flash", usage.prompt_token_count, usage.candidates_token_count)
            
            # 10. Check Output Security (Output Validation & Guardrails)
            out_safe, out_msg = self.output_guard.check(answer)
            if not out_safe:
                answer = out_msg
            else:
                # Cache successful response
                self.cache.set(question, answer)
            
            # 11. Update Memory
            if use_history:
                self.memory.add_exchange(question, answer)
                
            self.tracing.end_trace(trace_id)
            duration = time.time() - start_time
            
            # 12. Evals & Monitoring: Online Monitor for Hallucinations & Latency (Inference latency, Hallucinations)
            self.monitor.check_anomaly(duration, True, sources_count)
            
            return {
                'success': True,
                'answer': answer,
                'sources_count': sources_count
            }
            
        except Exception as e:
            logger.error(f"Error in ask_question: {str(e)}")
            self.tracing.end_trace(trace_id)
            duration = time.time() - start_time
            # Log failure to online monitor (Fallback logic)
            self.monitor.check_anomaly(duration, False, 0)
            return {
                'success': False,
                'answer': f"Error: {str(e)}",
                'sources_count': 0
            }

    @property
    def conversation_history(self) -> List[Tuple[str, str]]:
        return self.memory.get_raw_history()

    def clear_history(self):
        self.memory.clear()
