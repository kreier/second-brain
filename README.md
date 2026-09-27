![GitHub License](https://img.shields.io/github/license/kreier/second-brain)
![GitHub Release](https://img.shields.io/github/v/release/kreier/second-brain)

# Second Brain

A sovereign, airgapped personal knowledge vault and local AI intelligence platform. Ingests heterogeneous personal data (notes, emails, chat exports, databases, voice transcripts), normalizes them into an Obsidian-compatible markdown knowledge graph, and provides local, offline LLM synthesis.

> **Core Principle:** Containers contain software; persistent volumes contain knowledge; the Host Manager controls software lifecycle; Web provides the user interface.

---

## Architecture & Topology

The platform operates inside an isolated "white room" vault subnet (`10.5.5.0/24`):

```text
                                  [ INTERNET ]
                                        │ (Toggled on-demand for updates only)
                         ┌──────────────▼──────────────┐
                         │   Gateway / Router          │
                         │   10.5.5.1 (Default: blocked)
                         └──────────────┬──────────────┘
                                        │ Vault Subnet: 10.5.5.0/24
               ┌────────────────────────┴────────────────────────┐
               ▼                                                 ▼
     ┌───────────────────┐     USB Arduino Relay       ┌───────────────────┐
     │  "BRAIN" NODE     │────────────────────────────►│ "INTELLIGENCE"    │
     │  Tanix TX3 Mini   │   (Pulsed power header)     │  "Penta" Machine  │
     │  ARM64 / Armbian  │                             │  4x Pascal GPUs   │
     │  IP: 10.5.5.2     │                             │  30 GB VRAM       │
     │                   │◄───────────────────────────►│  Qwen 3.8 27B     │
     │  Docker Compose   │       REST / HTTP API       │  Ollama / vLLM    │
     └─────────┬─────────┘        (Port 11434)         └───────────────────┘
               │
               │ USB 3.0 High-Speed Mount
               ▼
     ┌───────────────────┐
     │  "MEMORY" STORE   │
     │  External USB SSD │
     │  - raw/ sources   │
     │  - processed/     │
     │  - second_brain.db│
     └───────────────────┘
```

- **Brain (`10.5.5.2`)**: Tanix TX3 Mini (ARM64 quad-core, 2 GB RAM) running Armbian, Docker Compose services, and the host-level manager.
- **Memory**: Dedicated external USB SSD storage mounted at `/mnt/memory` holding the Obsidian markdown vault and SQLite database.
- **Intelligence ("Penta")**: Dedicated compute rig with 4x Pascal Nvidia GPUs (30 GB VRAM) running **Qwen 3.8 27B** local inference completely offline.
- **Power Automation**: TX3 Mini controls an Arduino via USB serial to pulse a relay connected to Penta's motherboard power pins, booting the GPU workstation only when batch inference jobs are queued and cleanly shutting it down when finished.
- **Gateway (`10.5.5.1`)**: Firewall switch that permits temporary outbound access to update Docker containers and Git commits, then returns to strictly airgapped operation.

---

## The Four-Stage Data Lifecycle

```text
RAW                  NORMALIZED               CURATED                SYNTHESIZED
(raw/inbox/)   ──►   (Clean Atoms)    ──►    (processed/)    ──►    (Deep Insights)
Sources: Bildr,      Uniform schemas,         Obsidian vault:        Entity graphs,
emails, chats,       canonical UUIDs,         logs, facts,           embeddings,
transcripts          provenance links         projects, ideas        LLM briefings
```

- **`raw/inbox/`**: Incoming unprocessed captures.
- **`raw/archive/`**: Permanent, verbatim archive of all ingested sources (**cryptographically immutable**).
- **`processed/`**: Derived, structured notes organized by type per [`frontmatter.md`](frontmatter.md).
- **`moc/`**: Maps of Content — curated hub notes.

---

## Software Services

1. **`web/`**: Unified React SPA providing:
   - `/`: System Overview & Health Dashboard
   - `/curator`: Ingestion queue, source review, pipeline execution
   - `/brain`: Knowledge search, conversational AI with Qwen 27B, topic graph
   - `/statistics`: Source-vs-item funnels, corpus growth velocity, GPU token accounting
   - `/admin`: Container statuses, Penta power state toggle, update controls
2. **`curator/`**: Python pipeline service for scanning, normalizing, deduplicating, and archiving.
3. **`brain/`**: SQLite FTS5 and vector search service, LLM proxy gateway.
4. **`statistics/`**: Event-driven SQLite metrics recorder and analytics engine.
5. **`manager/`**: Native host-level supervisor (`second-brain` CLI) running directly on the TX3 Mini host.

---

## Nine-Phase Roadmap

| Phase | Milestone | Focus |
|---|---|---|
| [**Phase 1**](docs/phases/phase-01-foundation.md) | **Foundation** | Repository skeleton, unified React UI shell, initial Compose, version/health APIs |
| [**Phase 2**](docs/phases/phase-02-curator.md) | **Curator** | Deterministic RAW → NORMALIZED → CURATED pipeline, multi-format scanners |
| [**Phase 3**](docs/phases/phase-03-brain.md) | **Brain** | SQLite FTS5/vector indexing, semantic search, prompt engine, mock LLM proxy |
| [**Phase 4**](docs/phases/phase-04-statistics.md) | **Statistics** | Funnel metrics, source vs item accounting, growth time-series, token tracking |
| [**Phase 5**](docs/phases/phase-05-compose.md) | **Packaging** | Multi-architecture Docker Compose packaging, persistent `/memory` volumes |
| [**Phase 6**](docs/phases/phase-06-github-demo.md) | **GitHub Demo** | Public interactive React demo on GitHub Pages using safe synthetic data |
| [**Phase 7**](docs/phases/phase-07-tx3.md) | **TX3 Deployment** | Physical ARM64 Armbian deployment on Tanix TX3 Mini (`10.5.5.2`) + USB storage |
| [**Phase 8**](docs/phases/phase-08-penta.md) | **Penta GPU Integration** | 4x Pascal GPUs (30GB VRAM), Qwen 3.8 27B local LLM, Ollama API, batch queues |
| [**Phase 9**](docs/phases/phase-09-power-management.md) | **Power Management** | TX3 → Arduino → Relay automated Penta boot/run/shutdown lifecycle |

---

## Documentation System

- **[System Architecture](docs/ARCHITECTURE.md)**: Hardware topology, network design, component boundaries.
- **[Development Roadmap](docs/ROADMAP.md)**: Master phase descriptions and progression rules.
- **[Current Status](docs/STATUS.md)**: Living tracker of active milestones and immediate tasks.
- **[Data Model](docs/DATA_MODEL.md)**: Lifecycle stages, note schemas, and SQLite database tables.
- **[Service APIs](docs/API.md)**: HTTP REST contracts, ports, and CLI commands.
- **[Development Guide](docs/DEVELOPMENT.md)**: 3-tier workflow (workstation → TX3 integration → airgapped vault).
- **[Architectural Decision Records (ADRs)](docs/decisions/)**: Complete historical record of design choices.
- **[Agent Operating Instructions](AGENT.md)**: Rules for AI pair programmers operating on this repository.

---

## License

Content and code in this repository are licensed under the Apache 2.0 License — see [LICENSE](LICENSE).
