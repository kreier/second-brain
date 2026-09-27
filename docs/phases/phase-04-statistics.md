# Phase 4 — Statistics & Growth Analytics

**Status:** Scheduled  
**Target Environment:** Local Development Workstation  
**Prerequisites:** [Phase 2 — Curator](phase-02-curator.md), [Phase 3 — Brain](phase-03-brain.md)

---

## 1. Objective
Implement the Statistics service (`statistics/`) and dashboard at `/statistics`. The service reads SQLite audit tables and markdown files to produce real-time metrics across data funnels (Raw → Normalized → Curated → Synthesized), source vs. item accounting, corpus growth velocity, and GPU token consumption.

---

## 2. Deliverables
- [ ] Pipeline funnel aggregator (computing conversion rates and drop-offs between stages).
- [ ] Source vs. Item registry analytics (e.g. 7 sources → 2,232 items → 15,732 words).
- [ ] Historical corpus growth time-series engine (tracking notes, words, and storage over 30d/90d).
- [ ] LLM token accounting engine (prompt tokens, completion tokens, latency, cost avoided).
- [ ] Rich data visualization in React at `/statistics` (funnel charts, time-series graphs, source breakdown tables).

---

## 3. Acceptance Criteria
```text
[ ] GET /api/stats/overview returns correct real-time numbers matching actual filesystem and SQLite state
[ ] Funnel visualization on /statistics cleanly displays Raw -> Normalized -> Curated -> Synthesized progression
[ ] Source table accurately lists external sources (Bildr, Emails, Chats) separate from atomic item counts
[ ] Token usage counters correctly track mock/real LLM requests
[ ] Automated tests verify statistical calculation accuracy against seeded test databases
```
