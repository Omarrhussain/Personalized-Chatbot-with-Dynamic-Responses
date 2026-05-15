# 🤖 Personalized RAG Chatbot - 9-Layer Production Architecture

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini](https://img.shields.io/badge/Gemini-2.5--Flash-4285F4?logo=google-gemini)](https://deepmind.google/technologies/gemini/)
[![FAISS](https://img.shields.io/badge/VectorDB-FAISS-CF0000?logo=facebook)](https://github.com/facebookresearch/faiss)

A professional-grade, self-correcting RAG (Retrieval-Augmented Generation) system built on a sophisticated **9-Layer AI Production Architecture**. This project transitions from a basic demo to a robust, scalable, and observable production-ready application.

---

## 🏗️ 9-Layer Architecture Overview

This project is built using a modular design to ensure high reliability, security, and performance.

### 1. 🛠️ Services Layer
- **`services/rag_pipeline.py`**: Central orchestration of the entire RAG flow.
- **`services/memory.py`**: Intelligent conversational state management.
- **`services/semantic_cache.py`**: Fast retrieval of previous answers to reduce latency and cost.
- **`services/router.py`**: Intelligent query routing.

### 2. 🧠 Agents Layer (Self-Correcting)
- **`agents/document_grader.py`**: Validates retrieved documents for relevance.
- **`agents/decomposer.py`**: Breaks down complex queries into manageable sub-tasks.
- **`agents/adaptive_router.py`**: Dynamically adjusts routing based on query complexity.

### 3. 📝 Prompts Layer
- **`prompts/registry.py`**: Centralized, versioned, and typed prompt templates.
- **`prompts/versions.py`**: Version control for all system and RAG prompts.
- **`prompts/types.py`**: Type definitions for robust prompt management.

### 4. 🛡️ Security Layer (Tri-Guard System)
- **`security/input_guard.py`**: Validates user inputs for prompt injection or malicious content.
- **`security/content_guard.py`**: Redacts PII and sensitive data from retrieved context.
- **`security/output_guard.py`**: Validates model responses for quality and safety.

### 5. 📊 Evaluation Layer
- **`evaluation/golden_dataset.py`**: Baseline datasets for continuous testing.
- **`evaluation/offline_eval.py`**: Comprehensive offline testing of pipeline performance.
- **`evaluation/online_monitor.py`**: Real-time monitoring for hallucinations and latency.

### 6. 👁️ Observability Layer
- **`observability/tracing.py`**: Per-stage execution tracing with unique Trace IDs.
- **`observability/cost_tracking.py`**: Real-time token usage and cost per query tracking.
- **`observability/feedback.py`**: Link user feedback directly to execution traces.

### 7. 🤖 Agent Context
- **`.claude/agent_context.md`**: Dedicated context for AI coding assistants to understand the codebase before making changes.

### 8. 🎨 Custom Frontend
- **`static/`**: A premium, custom-built web interface (HTML/CSS/JS) designed for a "Gemini-like" spacious and modern experience.

### 9. 🚀 Deployment
- **`railway.json`**: Pre-configured for seamless cloud deployment on Railway.
- **`api_server.py`**: Production-ready FastAPI server with built-in frontend hosting.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- A Google Gemini API Key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Personalized_Chatbot
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # On Windows
   source .venv/bin/activate # On Unix/macOS
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

### Running the Application

Start the combined API and Frontend server:
```bash
python api_server.py
```
Open your browser and navigate to **`http://localhost:8000`**.

---

## 🧪 Testing & Evaluation

Run the offline evaluation suite to check pipeline performance:
```bash
python evaluation/offline_eval.py
```

---

## 🛠️ Key Technologies
- **LLM**: Gemini 2.5 Flash
- **Orchestration**: FastAPI
- **Vector DB**: FAISS
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Styling**: Premium Vanilla CSS (Modern Minimalist)

---

## 📄 License
This project is for demonstration and production readiness assessment.

## 🤝 Contributing
Contributions are welcome! Please ensure any changes adhere to the 9-layer architectural principles.
