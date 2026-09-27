import os
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

SERVICE_NAME = "brain"
VERSION = "0.1.0"
MEMORY_PATH = Path(os.getenv("MEMORY_PATH", "/memory"))
INTELLIGENCE_ENDPOINT = os.getenv("INTELLIGENCE_ENDPOINT", "http://10.5.5.5:11434")
INTELLIGENCE_MODEL = os.getenv("INTELLIGENCE_MODEL", "qwen-3.8-27b")

app = FastAPI(title="Second Brain - Brain Knowledge Service", version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    prompt: str
    context_notes: Optional[List[str]] = None
    stream: bool = False


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "version": VERSION,
        "intelligence_endpoint": INTELLIGENCE_ENDPOINT,
        "model": INTELLIGENCE_MODEL,
        "memory_mounted": MEMORY_PATH.exists(),
    }


@app.get("/api/brain/status")
def status():
    return {
        "service": SERVICE_NAME,
        "version": VERSION,
        "intelligence_endpoint": INTELLIGENCE_ENDPOINT,
        "model": INTELLIGENCE_MODEL,
        "fts_index_ready": (MEMORY_PATH / "second_brain.db").exists(),
        "status": "ready",
    }


@app.get("/api/brain/search")
def search(q: str = "", limit: int = 10):
    return {
        "query": q,
        "limit": limit,
        "results": [],
        "message": "Search index placeholder (Phase 3 implementation)",
    }


@app.post("/api/brain/query")
def query_knowledge(req: QueryRequest):
    return {
        "query": req.prompt,
        "model": INTELLIGENCE_MODEL,
        "response": f"Simulated Brain response for: '{req.prompt}'. Full multi-GPU integration scheduled for Phase 3/8.",
        "tokens_used": {"prompt": len(req.prompt.split()), "completion": 20},
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
