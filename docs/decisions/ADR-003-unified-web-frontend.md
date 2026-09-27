# ADR-003: Unified React Web Frontend Shell

**Status:** Accepted  
**Date:** 2026-09-27  
**Deciders:** User, ChatGPT Architect

---

## Context
Initial brainstorming considered running separate web interfaces or ports for the Curator, Brain, and Statistics services. However, running multiple web servers consumes redundant memory on the Tanix TX3 Mini (which has only 2GB RAM) and fragments the user experience across multiple browser tabs and port numbers.

## Decision
Second Brain uses a single unified React frontend container serving all views under standard client-side routes:
- `/` — System Overview & Health Dashboard
- `/curator` — Ingestion queue, pending file approvals, pipeline control
- `/brain` — Knowledge query, chat with local LLM, topic graph
- `/statistics` — Growth funnels, word counts, token accounting
- `/admin` — Container statuses, hardware power toggle, update triggers

The backend microservices remain headless HTTP APIs accessed through the unified Web container's reverse proxy.

## Consequences
- **Positive**: Low memory footprint on the TX3; single intuitive entry point; cohesive design language; enables a seamless public demo on GitHub Pages using client-side mock data.
- **Negative**: Client router must handle proxying to multiple backend endpoints.
