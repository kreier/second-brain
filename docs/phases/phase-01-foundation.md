# Phase 1 — Foundation

**Status:** In Progress  
**Target Environment:** Local Development Workstation  
**Current Milestone:** Repository skeleton, Web shell, and Docker Compose baseline

---

## 1. Objective
Establish the foundational codebase, directory structure, Docker Compose configuration, and unified React Web application shell so that a developer or coding agent can start the platform from a clean checkout and navigate the 5 primary system views.

---

## 2. Deliverables
- [ ] Microservice skeleton directories: `web/`, `curator/`, `brain/`, `statistics/`, `manager/`.
- [ ] Root `docker-compose.yml` for unified local execution.
- [ ] React SPA frontend with client-side routing:
  - `/` — System Overview & Health Dashboard
  - `/curator` — Ingestion queue view (mock data)
  - `/brain` — Knowledge query & chat view (mock data)
  - `/statistics` — Funnel & token growth dashboard (mock data)
  - `/admin` — System status & power control (mock data)
- [ ] Health (`GET /api/health`) and version (`GET /api/version`) endpoints.
- [ ] Automated verification script or test harness.

---

## 3. Acceptance Criteria
```text
[ ] docker compose up starts without error from a clean checkout
[ ] Web container is accessible at http://localhost:3000 (or port 80)
[ ] React application loads in browser with dark/light theme support
[ ] Navigation links for /, /curator, /brain, /statistics, /admin all render
[ ] GET /api/health returns 200 OK with service statuses
[ ] Version information is displayed on the UI
[ ] Unit/build tests pass (npm run build / docker compose config)
```

---

## 4. Current Work & Decisions
- Architecture documented in `docs/ARCHITECTURE.md`.
- ADR-001 through ADR-005 accepted.
- Preparing initial React skeleton in `web/` and `docker-compose.yml`.
