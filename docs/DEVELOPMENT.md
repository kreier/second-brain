# Second Brain — Development Guide & Workflow

**Version:** 0.1.0-dev  
**Environments:** Dev Workstation → ARM64 Integration → Vault Production

---

## 1. Three-Tier Deployment Workflow

To maintain high development velocity while ensuring strict airgapped hardware reliability, the project uses three distinct execution tiers:

```
  TIER 1: DEVELOPMENT              TIER 2: INTEGRATION              TIER 3: PRODUCTION
   (Local Workstation)              (Tanix TX3 Mini)               (Vault White-Room)
┌───────────────────────┐        ┌───────────────────────┐       ┌───────────────────────┐
│ Host: x86_64 i7 64GB  │        │ Host: ARM64 TX3 Mini  │       │ Subnet: 10.5.5.0/24   │
│ Fast Docker builds    │───────►│ Armbian Linux         │──────►│ TX3 Mini Brain        │
│ Mock LLM / Ollama dev │        │ Real USB Memory Mount │       │ USB Storage Memory    │
│ Fast unit / e2e tests │        │ Compose verification  │       │ Penta 4x Pascal GPUs  │
└───────────────────────┘        └───────────────────────┘       │ Airgapped operation   │
                                                                 └───────────────────────┘
```

### Tier 1: Local Development Workstation
- **Purpose**: Rapid code-test loops, frontend development, pipeline iteration.
- **Characteristics**: Fast builds, instant reload, mock inference responses (bypassing heavy GPU requirements).
- **Execution**:
  ```bash
  # Start services in dev mode with live reload
  docker compose -f docker-compose.dev.yml up
  ```

### Tier 2: ARM64 Integration on Tanix TX3 Mini
- **Purpose**: Verifies multi-architecture container builds (ARM64 / `linux/arm64`), CPU/RAM constraints (2GB RAM), and physical USB filesystem I/O performance under Armbian.
- **Execution**:
  ```bash
  # Native compose deployment on TX3
  second-brain status
  second-brain update
  ```

### Tier 3: Airgapped Production Vault
- **Purpose**: Sovereign, offline personal knowledge processing.
- **Characteristics**: Subnet `10.5.5.0/24`, zero internet exposure during routine operation, hardware relay power management for the Penta GPU machine.

---

## 2. Coding Agent Operating Instructions

When developing Second Brain tasks (using Antigravity, Claude Code, or Codex):

1. **Consult Project Memory First**:
   - Always read `docs/STATUS.md` and the active phase specification in `docs/phases/` before starting work.
   - Read `docs/ARCHITECTURE.md` and related ADRs in `docs/decisions/`.
2. **Respect Architectural Boundaries**:
   - Never change architecture without documenting the decision in an ADR.
   - Do not bypass Docker isolation for application services.
   - Keep the host-level manager decoupled from application containers.
3. **Acceptance-Test Driven Execution**:
   - Implement the minimal code necessary to satisfy the current task's acceptance criteria.
   - Write and run automated tests before declaring a task complete.
4. **Post-Implementation Documentation**:
   - Update `docs/STATUS.md` with completed items and immediate next steps.
   - Log significant events or insights in `docs/journal/`.
   - Update phase checkboxes in `docs/phases/`.
