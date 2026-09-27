# ADR-002: Multi-Container Microservices Orchestrated via Docker Compose

**Status:** Accepted  
**Date:** 2026-09-27  
**Deciders:** User, ChatGPT Architect

---

## Context
The system consists of several distinct functional concerns: web UI delivery, file ingestion/curation, semantic search and LLM proxying, and event statistics collection. Packing all concerns into a single monolithic binary or container creates dependency bloat (e.g. Node.js + Python ML packages + SQLite tools), slows down updates, and makes fault isolation difficult on low-resource ARM64 devices (Tanix TX3 Mini).

## Decision
We decouple the backend into independent microservices orchestrated via standard `docker-compose.yml`:
- `web`: React frontend SPA (static nginx or Node server).
- `curator`: Python pipeline service for scanning and archiving.
- `brain`: Python service for indexing and Ollama/Penta proxying.
- `statistics`: Lightweight service reading SQLite operational tables.

Each service has its own `Dockerfile` and independent semantic versioning. All services mount the shared `/memory` persistent volume.

## Consequences
- **Positive**: Clean separation of concerns; failures in the Curator or Brain do not crash the Web UI; individual services can be rebuilt and updated independently.
- **Negative**: Requires inter-service network communication configuration and slightly higher idle RAM overhead than a monolith.
