#!/usr/bin/env python3
"""
Personalized RAG Chatbot - API Server
Single entry point that serves both the API and the web frontend.
Run with: python api_server.py
Open:     http://localhost:8000
"""
import uvicorn
import os
import sys
import time
import logging
import traceback
import webbrowser
from pathlib import Path

# ── Resolve absolute paths ──────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent
STATIC_DIR = PROJECT_ROOT / "static"

# Ensure the project root is on sys.path so all our packages resolve
sys.path.insert(0, str(PROJECT_ROOT))

# ── Logging ─────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── FastAPI setup ───────────────────────────────────────────────────
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.rag_pipeline import RAGPipeline

app = FastAPI(
    title="Personalized RAG Chatbot API",
    description="AI Chatbot with RAG capabilities powered by Gemini 2.5 Flash",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static directory using an absolute path so it always resolves
STATIC_DIR.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# ── Models ──────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    use_history: bool = True

class ChatResponse(BaseModel):
    success: bool
    answer: str
    sources_count: int
    response_time: float

# ── Routes ──────────────────────────────────────────────────────────
@app.get("/")
async def root():
    index_file = STATIC_DIR / "index.html"
    if not index_file.exists():
        return {"error": "Frontend not found. Make sure static/index.html exists."}
    return FileResponse(str(index_file))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "chatbot-api"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat with the Gemini RAG chatbot"""
    start_time = time.time()
    try:
        # Lazy-init the pipeline on first request
        if not hasattr(app.state, "chatbot") or app.state.chatbot is None:
            logger.info("Initializing RAG Pipeline...")
            app.state.chatbot = RAGPipeline()
            logger.info("✅ RAG Pipeline ready!")

        result = app.state.chatbot.ask_question(request.message, request.use_history)
        response_time = time.time() - start_time

        return ChatResponse(
            success=result["success"],
            answer=result["answer"],
            sources_count=result.get("sources_count", 0),
            response_time=response_time,
        )
    except Exception as e:
        response_time = time.time() - start_time
        logger.error(f"Chat error: {e}")
        logger.error(traceback.format_exc())
        return ChatResponse(
            success=False,
            answer=f"Error: {e}",
            sources_count=0,
            response_time=response_time,
        )

@app.get("/conversation/history")
async def get_conversation_history():
    """Get current conversation history"""
    try:
        if hasattr(app.state, "chatbot") and app.state.chatbot:
            return {
                "history": app.state.chatbot.conversation_history,
                "total_turns": len(app.state.chatbot.conversation_history),
            }
        return {"history": [], "total_turns": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/conversation/clear")
async def clear_conversation_history():
    """Clear conversation history"""
    try:
        if hasattr(app.state, "chatbot") and app.state.chatbot:
            app.state.chatbot.clear_history()
            return {"message": "Conversation history cleared"}
        return {"message": "No chatbot instance found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ── Entry point ─────────────────────────────────────────────────────
if __name__ == "__main__":
    HOST = "127.0.0.1"
    PORT = 8000

    print("=" * 50)
    print("  Personalized RAG Chatbot")
    print(f"  http://{HOST}:{PORT}")
    print("=" * 50)

    # Auto-open the browser
    webbrowser.open(f"http://{HOST}:{PORT}")

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=False,
        log_level="info",
    )