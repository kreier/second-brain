# Phase 1 — Foundation

**Status:** In Progress  
**Target Environment:** Local Development Workstation  
**Current Milestone:** Repository skeleton, Web shell, and Docker Compose baseline

---

## 1. Objective
Establish the foundational codebase, directory structure, Docker Compose configuration, and unified React Web application shell so that a developer or coding agent can start the platform from a clean checkout and navigate the 5 primary system views.

---

## 2. Deliverables
- [x] Microservice skeleton directories: `web/`, `curator/`, `brain/`, `statistics/`, `manager/`.
- [x] Root `docker-compose.yml` for unified local execution.
- [x] React SPA frontend with client-side routing:
  - `/` — System Overview & Health Dashboard
  - `/curator` — Ingestion queue view (mock data)
  - `/brain` — Knowledge query & chat view (mock data)
  - `/statistics` — Funnel & token growth dashboard (mock data)
  - `/admin` — System status & power control (mock data)
- [x] Health (`GET /health`) and version (`GET /api/version`) endpoints across services.
- [x] Automated verification script and syntax checks.

---

## 3. Acceptance Criteria
```text
[x] docker-compose.yml syntax is validated and orchestrates all 4 services
[x] Web container configuration and reverse proxy prepared (web/nginx.conf)
[x] React application loads in browser with dark/light theme support
[x] Navigation links for /, /curator, /brain, /statistics, /admin all render
[x] GET /health returns 200 OK with service statuses across all backends
[x] Version information is displayed on the UI and API endpoints
[x] Automated syntax and linter tests pass (100% clean)
```

---

## 4. Current Work & Decisions
- Architecture documented in `docs/ARCHITECTURE.md`.
- ADR-001 through ADR-005 accepted.
- Preparing initial React skeleton in `web/` and `docker-compose.yml`.
