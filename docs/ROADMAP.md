# Second Brain — Development Roadmap

**Current Version:** `0.1.0-dev`  
**Current Phase:** [Phase 1 — Foundation](phases/phase-01-foundation.md)  
**Methodology:** Acceptance-Test-Driven, Incremental Phase Delivery

---

## The Nine Phases Overview

Development proceeds along a 9-phase path from foundational software architecture to fully airgapped hardware deployment and automated GPU power orchestration:

```
┌────────────────────────────────────────────────────────────────────────┐
│ SOFTWARE DEVELOPMENT & VALIDATION (i7 Workstation)                     │
├─────────────────┬─────────────────┬─────────────────┬──────────────────┤
│ Phase 1         │ Phase 2         │ Phase 3         │ Phase 4          │
│ Foundation      │ Curator         │ Brain           │ Statistics       │
│ Web UI Skeleton │ Ingestion &     │ Knowledge &     │ Funnels &        │
│ & Docker Compose│ Pipeline        │ LLM Abstraction │ Token Metrics    │
└────────┬────────┴────────┬────────┴────────┬────────┴────────┬─────────┘
         │                 │                 │                 │
         └─────────────────┼─────────────────┼─────────────────┘
                           ▼
┌────────────────────────────────────────────────────────────────────────┐
│ PACKAGING & PORTABILITY                                                │
├───────────────────────────────────┬────────────────────────────────────┤
│ Phase 5                           │ Phase 6                            │
│ Multi-Container Packaging         │ Public GitHub Demo                 │
│ Volume mounts, versioning, health │ GitHub Pages mock interactive demo │
└─────────────────┬─────────────────┴──────────────────┬─────────────────┘
                  │                                    │
                  └──────────────────┬─────────────────┘
                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│ AIRGAPPED VAULT HARDWARE DEPLOYMENT (Vault Subnet 10.5.5.0/24)         │
├───────────────────┬───────────────────────────┬────────────────────────┤
│ Phase 7           │ Phase 8                   │ Phase 9                │
│ TX3 Mini Brain    │ Penta GPU Intelligence    │ Penta Power Management │
│ ARM64 / Armbian   │ 4x Pascal GPUs (30GB)     │ TX3 → Arduino → Relay  │
│ USB Memory Mount  │ Qwen 3.8 27B local LLM    │ Automated Power Cycle  │
└───────────────────┴───────────────────────────┴────────────────────────┘
```

---

## Phase Summary Table

| Phase | Title | Target Environment | Primary Objective |
|---|---|---|---|
| [**1**](phases/phase-01-foundation.md) | **Foundation** | Dev Workstation | Repository skeleton, single React frontend shell, initial Compose, version/health APIs. |
| [**2**](phases/phase-02-curator.md) | **Curator** | Dev Workstation | Deterministic RAW → NORMALIZED → CURATED pipeline, multi-format scanners, Curator UI. |
| [**3**](phases/phase-03-brain.md) | **Brain** | Dev Workstation | SQLite FTS5/vector indexing, search API, prompt engineering, mock LLM proxy. |
| [**4**](phases/phase-04-statistics.md) | **Statistics** | Dev Workstation | Event-driven SQLite metrics, source-vs-item counts, pipeline funnels, token accounting. |
| [**5**](phases/phase-05-compose.md) | **Packaging** | Dev Workstation | Independent versioning, persistent volume mapping, reproducible multi-container compose. |
| [**6**](phases/phase-06-github-demo.md) | **GitHub Demo** | GitHub Pages | Static/mock public demonstration with safe synthetic data showcasing UI & funnels. |
| [**7**](phases/phase-07-tx3.md) | **TX3 Deployment** | Tanix TX3 (`10.5.5.2`) | Real ARM64 Armbian deployment, USB memory storage mount, host manager daemon. |
| [**8**](phases/phase-08-penta.md) | **Penta GPU Integration** | Penta GPU Node | 4x Pascal GPUs (30GB VRAM), Qwen 3.8 27B local inference, Ollama proxy, batch queue. |
| [**9**](phases/phase-09-power-management.md) | **Power Management** | Airgapped Vault | TX3 → USB Arduino → Relay → Penta power switch lifecycle: on-demand boot, run, shutdown. |

---

## Cross-Cutting Capability: Host Manager (`manager/`)

The **Host Manager** (`second-brain` CLI) is developed incrementally across phases:
- **Phase 1**: Basic CLI wrapper for starting/stopping services.
- **Phase 5**: Service lifecycle management and health check validation.
- **Phase 7**: Gateway network coordination (`10.5.5.1`) for updates and rollback protection on Armbian.
- **Phase 9**: Arduino serial power orchestration for the Penta GPU node.

---

## Rules of Progression

1. **Test-Driven Acceptance**: A phase is only considered complete when all acceptance criteria in its dedicated specification document (`docs/phases/phase-XX-*.md`) pass.
2. **Preserve Architectural Memory**: No architectural modification may be committed without an accompanying Architectural Decision Record in `docs/decisions/`.
3. **Small Slices**: The coding agent implements individual tasks within the current active phase, runs automated verifications, and updates `docs/STATUS.md` after every change.
