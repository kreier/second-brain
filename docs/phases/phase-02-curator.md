# Phase 2 — Curator Pipeline & Service

**Status:** Scheduled  
**Target Environment:** Local Development Workstation  
**Prerequisites:** [Phase 1 — Foundation](phase-01-foundation.md)

---

## 1. Objective
Implement the deterministic data ingestion and curation pipeline (`curator/`). The service scans raw data in `raw/inbox/`, strips noise, validates YAML frontmatter, deduplicates entities, extracts structured notes into `processed/`, and safely archives source files into immutable `raw/archive/` while recording provenance in SQLite.

---

## 2. Deliverables
- [ ] Multi-source file scanner supporting:
  - Markdown notes & audio transcripts
  - Email exports (mbox / .eml / JSON)
  - WhatsApp & Viber chat export logs
  - SQLite table dumps (e.g. Bildr database)
- [ ] YAML frontmatter schema validator adhering to `frontmatter.md`.
- [ ] Entity resolution & deduplication engine (detecting near-duplicate titles and aliases).
- [ ] Archival mover: moves ingested source files to `raw/archive/` verbatim.
- [ ] Curator HTTP API (`curator/`) exposing status and manual trigger endpoints.
- [ ] Curator UI integration in React at `/curator`.

---

## 3. Acceptance Criteria
```text
[ ] Placing sample files in raw/inbox/ and calling POST /api/curator/process extracts notes to processed/
[ ] Source files in raw/inbox/ are moved unchanged to raw/archive/
[ ] Ingested notes have complete YAML frontmatter linking back to source raw_id
[ ] SQLite tables (sources, raw_items, pipeline_runs) accurately record all actions
[ ] Duplicate files are detected via SHA256 checksum and prevented from duplicate processing
[ ] Web UI at /curator displays pending inbox items and triggers processing runs
[ ] Automated unit tests pass with >85% code coverage for the normalizer
```
