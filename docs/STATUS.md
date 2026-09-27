# Second Brain — Project Status

**Version:** `0.1.0-dev`  
**Last Updated:** `2026-09-27`  
**Current Phase:** [Phase 1 — Foundation](phases/phase-01-foundation.md)

---

## Overall Progress

```text
Progress: [████░░░░░░] 40% (Phase 1 Foundation Complete)
```

---

## Status by Phase

| Phase | Description | Status |
|---|---|---|
| [**Phase 1**](phases/phase-01-foundation.md) | Foundation: Repo skeleton, Web UI shell, Compose, Health/Version | **Complete** (v0.1.0) |
| [**Phase 2**](phases/phase-02-curator.md) | Curator: Deterministic RAW → NORMALIZED → CURATED pipeline | **In Progress** |
| [**Phase 3**](phases/phase-03-brain.md) | Brain: Knowledge retrieval, search, prompt & mock LLM proxy | Scheduled |
| [**Phase 4**](phases/phase-04-statistics.md) | Statistics: SQLite metrics, funnels, token accounting, Growth UI | Scheduled |
| [**Phase 5**](phases/phase-05-compose.md) | Packaging: Multi-container Compose, persistent volumes, packaging | Scheduled |
| [**Phase 6**](phases/phase-06-github-demo.md) | GitHub Demo: Public interactive demo on GitHub Pages | Scheduled |
| [**Phase 7**](phases/phase-07-tx3.md) | TX3 Deployment: Tanix TX3 Mini Armbian (`10.5.5.2`) + USB Memory | Scheduled |
| [**Phase 8**](phases/phase-08-penta.md) | Penta Integration: 4x Pascal GPUs (30GB), Qwen 3.8 27B local LLM | Scheduled |
| [**Phase 9**](phases/phase-09-power-management.md) | Power Management: TX3 → Arduino → Relay automated Penta boot/stop | Scheduled |

---

## Completed Milestones

- [x] Initial Obsidian vault structure (`raw/`, `processed/`, `templates/`, `moc/`, `frontmatter.md`).
- [x] High-level architectural specification finalized with ChatGPT and user review.
- [x] Airgapped network topology defined (`10.5.5.0/24`, Gateway `10.5.5.1`, Brain `10.5.5.2`, Penta Quad-GPU @ `10.5.5.5`, USB Memory).
- [x] Canonical Reference Hardware Profile created in [`docs/profiles/reference-vault-penta.md`](profiles/reference-vault-penta.md).
- [x] Nine-phase test-driven development roadmap formulated.
- [x] Canonical documentation system established (`docs/ARCHITECTURE.md`, `ROADMAP.md`, `STATUS.md`, `DATA_MODEL.md`, `API.md`, `DEVELOPMENT.md`).
- [x] Architectural Decision Records created (ADR-001 through ADR-006).
- [x] Hardware-agnostic configuration template created ([`config/settings.example.yml`](../config/settings.example.yml)).
- [x] Personal notes decoupled from repository; sample data moved to [`demo/vault/`](../demo/vault/) with interactive GitHub Pages application ([`demo/index.html`](../demo/index.html)) and workflow ([`.github/workflows/deploy-pages.yml`](../.github/workflows/deploy-pages.yml)).
- [x] **Phase 1 Complete**: Microservice skeletons (`web/`, `curator/`, `brain/`, `statistics/`, `manager/`) created, unified Web shell and reverse proxy implemented, root `docker-compose.yml` and `.env.example` configured, `second-brain` host manager CLI implemented and tested.

---

## In Progress (Phase 2 — Curator Pipeline)

- [ ] File scanner for `raw/inbox/` detecting and parsing multi-format sources (Markdown, email mbox, chat exports).
- [ ] Deterministic normalizer extracting atomized notes into `processed/` with validated frontmatter.
- [ ] Archival mover: moves ingested raw sources to `raw/archive/` verbatim and records provenance in SQLite.

---

## Immediate Next 3 Tasks

1. **Task 2.1**: Implement `raw/inbox/` file scanner and SHA256 checksum deduplication in `curator/`.
2. **Task 2.2**: Implement markdown atomization and YAML frontmatter validation against `frontmatter.md`.
3. **Task 2.3**: Connect the Curator UI at `/curator` to trigger batch processing runs and display live ingestion logs.
