# ADR-001: Deterministic Layered Data Pipeline (RAW → NORMALIZED → CURATED → SYNTHESIZED)

**Status:** Accepted  
**Date:** 2026-09-27  
**Deciders:** User, ChatGPT Architect

---

## Context
A personal second brain ingests heterogeneous, messy inputs: chat exports, emails, SQLite database snapshots (e.g. Bildr), voice transcripts, and manual notes. Allowing raw data to directly alter the knowledge graph without strict validation leads to corrupted metadata, broken links, duplicate entities, and lost provenance.

## Decision
We enforce a strict 4-stage unidirectional pipeline:
1. **RAW**: Files land in `raw/inbox/`. Once extracted, the original source is moved verbatim to `raw/archive/` and is strictly **immutable**.
2. **NORMALIZED**: Scanners extract clean text, validate YAML frontmatter, and generate canonical UUIDs.
3. **CURATED**: Obsidian-compatible markdown notes in `processed/` organized by type (`log`, `fact`, `project`, `idea`, `travel`, `moc`).
4. **SYNTHESIZED**: LLM-derived insights, entity triples, and embeddings.

## Consequences
- **Positive**: Complete provenance tracking (any note can trace back to its raw file), no data loss, human-readable file structure.
- **Negative**: Requires dedicated parser logic for each distinct source format.
