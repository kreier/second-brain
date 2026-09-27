# Second Brain — Service APIs & Contracts

**Version:** 0.1.0-dev  
**Communication Protocol:** HTTP / JSON REST + Server-Sent Events (SSE)

---

## Service Port Allocation

| Service | Port | Host Address (Internal) | Description |
|---|---|---|---|
| **Web** | `3000` / `80` | `10.5.5.2:80` | React Frontend Shell |
| **Curator** | `8001` | `10.5.5.2:8001` | Ingestion, Normalization, Deduplication |
| **Brain** | `8002` | `10.5.5.2:8002` | Knowledge Retrieval & LLM Gateway Proxy |
| **Statistics** | `8003` | `10.5.5.2:8003` | Event Metrics & Funnel Analytics |
| **Penta LLM** | `11434` | `10.5.5.x:11434` | Ollama / vLLM Qwen 3.8 27B Server |
| **Manager** | CLI / `8080` | Host `10.5.5.2` | Lifecycle, Updates, Hardware Relay |

---

## 1. Web Service (`web/`)

Provides static bundle serving and transparent reverse proxy to the backend services:

- `GET /` — System Overview dashboard.
- `GET /curator` — Ingestion queue, pending file approvals, pipeline control.
- `GET /brain` — Knowledge query interface and conversational AI.
- `GET /statistics` — Funnel visualization, corpus growth, token usage charts.
- `GET /admin` — System health, container statuses, update & power controls.

---

## 2. Curator API (`curator/`) — Port 8001

### Health & Version
- `GET /health`  
  Returns `{ "status": "ok", "service": "curator", "version": "0.1.0" }`.

### Pipeline Execution
- `GET /api/curator/status`  
  Returns current pipeline state (idle/running), number of items in `raw/inbox/`, and last run timestamp.
- `POST /api/curator/scan`  
  Triggers a directory scan of `raw/inbox/` and catalogs newly discovered files.
- `POST /api/curator/process`  
  Executes the deterministic normalization and curation pipeline. Moves processed sources to `raw/archive/`.
  - Body: `{ "batch_size": 50, "dry_run": false }`
  - Returns run summary: `{ "run_id": "...", "processed": 12, "errors": 0 }`.

---

## 3. Brain API (`brain/`) — Port 8002

### Search & Retrieval
- `GET /api/brain/search?q=<query>&limit=10`  
  Performs hybrid search (SQLite FTS5 + semantic embeddings) over the curated Obsidian vault.
- `GET /api/brain/graph`  
  Returns the link graph nodes and edges between notes in `processed/`.

### Inference & Proxy
- `POST /api/brain/query`  
  Dispatches a user query to the local LLM proxy.
  - Body: `{ "prompt": "...", "context_notes": ["topics/energy.md"], "stream": true }`
  - Response: Server-Sent Events (SSE) streaming token output from Qwen 27B.
- `GET /api/brain/queue`  
  Returns pending offline batch jobs waiting for Penta GPU power-on.

---

## 4. Statistics API (`statistics/`) — Port 8003

### Metrics & Funnels
- `GET /api/stats/overview`  
  Returns summary counts across all 4 stages:
  ```json
  {
    "raw": { "sources": 7, "items": 1072, "words": 15732 },
    "curated": { "notes": 370, "words": 12305, "storage_mb": 15.2 },
    "synthesized": { "entities": 143, "connections": 420 },
    "tokens": { "total_prompt": 128450, "total_completion": 43200 }
  }
  ```
- `GET /api/stats/growth?days=30`  
  Returns daily historical growth time series for notes, words, and storage.
- `GET /api/stats/runs`  
  Returns execution audit logs for pipeline and LLM inference runs.

---

## 5. Host Manager Interface (`manager/`)

The manager is a host-level system binary installed at `/usr/local/bin/second-brain` with an optional local-only administrative control socket/port.

### CLI Commands
- `second-brain status` — Displays Docker Compose service status, vault disk usage, and Penta GPU state.
- `second-brain update` — Requests temporary internet gateway access at `10.5.5.1`, pulls git repository and image updates, applies database migrations, and restarts services.
- `second-brain power [on|off|status]` — Controls Penta power state via Arduino USB serial.
- `second-brain backup` — Creates a verified compressed snapshot of `/mnt/memory` to external backup storage.
