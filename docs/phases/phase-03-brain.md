# Phase 3 — Brain Service & LLM Abstraction

**Status:** Scheduled  
**Target Environment:** Local Development Workstation  
**Prerequisites:** [Phase 2 — Curator](phase-02-curator.md)

---

## 1. Objective
Build the Brain service (`brain/`), which acts as the intelligent retrieval, search, and local LLM interface. It indexes notes in `processed/` using SQLite FTS5 and vector embeddings, constructs retrieval-augmented context windows, and provides an OpenAI-compatible / Ollama client abstraction to talk to either a local mock LLM or the remote GPU node.

---

## 2. Deliverables
- [ ] SQLite FTS5 full-text indexing engine over all markdown files in `processed/`.
- [ ] Local embedding generator (lightweight ONNX or sentence-transformers model).
- [ ] Hybrid search engine (combining keyword BM25 with cosine vector similarity).
- [ ] Context assembly engine (retrieving relevant notes, wikilinks, and metadata for a query).
- [ ] LLM Proxy Gateway with mock fallback for local testing without GPUs.
- [ ] Interactive Chat & Knowledge Query interface in the React Web shell at `/brain`.

---

## 3. Acceptance Criteria
```text
[ ] Searching for keywords returns ranked matching notes within <50ms
[ ] Vector similarity search successfully finds conceptual matches without exact keywords
[ ] Context builder formats relevant notes within token budgets
[ ] Querying POST /api/brain/query streams responses via SSE from the LLM proxy (or mock provider)
[ ] Interactive UI at /brain allows submitting questions and inspecting retrieved source notes
[ ] Unit tests verify search ranking and context extraction
```
