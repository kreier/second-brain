import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

SERVICE_NAME = "curator"
VERSION = "0.1.0"
MEMORY_PATH = Path(os.getenv("MEMORY_PATH", "/memory"))

app = FastAPI(title="Second Brain - Curator Service", version=VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "version": VERSION,
        "memory_mounted": MEMORY_PATH.exists(),
    }


@app.get("/api/curator/status")
def status():
    inbox_path = MEMORY_PATH / "raw" / "inbox"
    archive_path = MEMORY_PATH / "raw" / "archive"
    processed_path = MEMORY_PATH / "processed"

    inbox_count = 0
    if inbox_path.exists():
        inbox_count = len([f for f in inbox_path.iterdir() if f.is_file() and f.name != ".gitkeep"])

    archive_count = 0
    if archive_path.exists():
        archive_count = len([f for f in archive_path.iterdir() if f.is_file() and f.name != ".gitkeep"])

    curated_count = 0
    if processed_path.exists():
        curated_count = len([f for f in processed_path.rglob("*.md") if f.name != ".gitkeep"])

    return {
        "service": SERVICE_NAME,
        "version": VERSION,
        "inbox_items": inbox_count,
        "archived_sources": archive_count,
        "curated_notes": curated_count,
        "status": "idle",
    }


@app.post("/api/curator/scan")
def trigger_scan():
    inbox_path = MEMORY_PATH / "raw" / "inbox"
    files = []
    if inbox_path.exists():
        files = [f.name for f in inbox_path.iterdir() if f.is_file() and f.name != ".gitkeep"]
    return {
        "status": "scanned",
        "found_files": files,
        "count": len(files),
    }


@app.post("/api/curator/process")
def process_batch(batch_size: int = 50, dry_run: bool = False):
    return {
        "status": "queued",
        "batch_size": batch_size,
        "dry_run": dry_run,
        "message": "Curator pipeline scheduled (Phase 2 implementation)",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
