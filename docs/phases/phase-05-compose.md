# Phase 5 — Multi-Container Compose & Packaging

**Status:** Scheduled  
**Target Environment:** Local Development Workstation  
**Prerequisites:** [Phase 1](phase-01-foundation.md), [Phase 2](phase-02-curator.md), [Phase 3](phase-03-brain.md), [Phase 4](phase-04-statistics.md)

---

## 1. Objective
Package all services (`web`, `curator`, `brain`, `statistics`) into production-grade multi-architecture Docker images (`linux/amd64`, `linux/arm64`). Define robust Docker Compose orchestration with health checks, restart policies, resource limits, and persistent volume bindings for `/memory`.

---

## 2. Deliverables
- [ ] Optimized, minimal Dockerfiles for each service using multi-stage builds.
- [ ] Multi-architecture container build pipeline (supporting AMD64 and ARM64).
- [ ] Production `docker-compose.yml` with:
  - Persistent volume mounts for `/memory` (`raw/`, `processed/`, `data/`).
  - Container resource constraints suitable for low-spec hosts (TX3 Mini RAM budget).
  - Health checks and automatic service restart policies.
- [ ] Clean environment configuration via `.env.example`.
- [ ] Initial Host Manager setup script (`scripts/install-manager.sh`).

---

## 3. Acceptance Criteria
```text
[ ] docker compose up -d launches all 4 containers cleanly on an empty system
[ ] All containers report 'healthy' status via docker compose ps
[ ] Stopping and restarting containers preserves all SQLite records and notes on the mounted volume
[ ] Container memory limits prevent out-of-memory crashes on systems with <=2GB RAM
[ ] Automated CI builds verify both linux/amd64 and linux/arm64 image compilation
```
