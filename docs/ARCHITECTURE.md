# Second Brain — System Architecture

**Version:** 0.1.0-dev  
**Status:** Approved Architecture  
**Network Domain:** `10.5.5.0/24` (Isolated White-Room Vault)

---

## 1. Vision & Core Philosophy

The **Second Brain** is a sovereign, self-hosted, airgapped personal knowledge and intelligence system. It ingests diverse personal data sources (notes, emails, chat exports, databases, voice transcripts), normalizes and organizes them into an Obsidian-compatible markdown knowledge graph, and provides local, offline AI intelligence for synthesis, retrieval, and decision support.

### The Core Architectural Tenet
> **Containers contain software; persistent volumes contain knowledge; the Host Manager controls software lifecycle; Web provides the user interface.**

- **Software Sovereignty**: Application logic is containerized and independently versioned.
- **Knowledge Permanence**: All data resides on standard filesystems (Markdown + SQLite), ensuring total portability and human readability without lock-in.
- **Airgapped Security**: Inference runs strictly on local GPU hardware inside an isolated vault network.

---

## 2. Network & Hardware Topology

The entire system operates inside an isolated, private "white room" network (`10.5.5.0/24`):

```
                                  [ INTERNET ]
                                        │
                                (switched gateway)
                                        │
                         ┌──────────────▼──────────────┐
                         │   Gateway / Router          │
                         │   10.5.5.1                  │
                         │   (Internet toggled on-     │
                         │    demand for updates only) │
                         └──────────────┬──────────────┘
                                        │
               ┌────────────────────────┴────────────────────────┐
               │ Isolated Vault Subnet: 10.5.5.0/24              │
               │                                                 │
               ▼                                                 ▼
     ┌───────────────────┐                             ┌───────────────────┐
     │  "BRAIN" NODE     │     USB Arduino Relay       │ "INTELLIGENCE"    │
     │  Tanix TX3 Mini   │────────────────────────────►│  "Penta" Node     │
     │  ARM64 / Armbian  │   (Power pin trigger)       │  x86_64 Host      │
     │  IP: 10.5.5.2     │                             │  4x Pascal GPUs   │
     │                   │                             │  30 GB VRAM       │
     │  Docker Compose   │◄───────────────────────────►│  Qwen 3.8 27B     │
     │  Services         │       REST / HTTP API       │  Ollama / vLLM    │
     └─────────┬─────────┘        (Port 11434)         └───────────────────┘
               │
               │ USB 3.0 / High-Speed Storage
               ▼
     ┌───────────────────┐
     │  "MEMORY" STORE   │
     │  External USB SSD │
     │  - raw/ sources   │
     │  - processed/     │
     │  - sqlite/ data   │
     │  - backups/       │
     └───────────────────┘
```

### Node Roles

1. **Gateway (`10.5.5.1`)**:
   - Manages the local vault subnet `10.5.5.0/24`.
   - Normal operation: **strictly airgapped** (no external routing or DNS).
   - Maintenance mode: Gateway temporarily enables outbound internet access when triggered by the Host Manager to pull Docker container updates or Git commits from `github.com/kreier/second-brain`, then severs access immediately.

2. **Brain Node (`10.5.5.2` — Tanix TX3 Mini)**:
   - Compact, low-power ARM64 quad-core device running Armbian Linux.
   - Always-on controller running Docker and the host-level `second-brain` manager daemon.
   - Hosts the Web UI, Curator ingestion pipeline, Brain knowledge retrieval layer, and Statistics service.

3. **Memory Store (USB External Storage)**:
   - Dedicated external high-reliability storage directly mounted to `/mnt/memory` on the Brain node.
   - Houses the canonical Obsidian vault (`raw/`, `processed/`, `templates/`, `moc/`), SQLite indices, vector embeddings, and operational logs.

4. **Intelligence Node ("Penta" — High-Performance GPU Rig)**:
   - Dedicated compute workstation featuring **four Pascal Nvidia GPUs** with **30 GB aggregate VRAM**.
   - Runs **Qwen 3.8 27B** quantized weights (via Ollama or llama.cpp / vLLM).
   - High power draw: powered on **only on-demand** via the TX3 Mini.

5. **Power Management Link (TX3 Mini → Arduino → Relay → Penta)**:
   - An Arduino microcontroller connected via USB to the TX3 Mini controls a mechanical/solid-state relay wired directly to Penta's motherboard `POWER_SW` header pins.
   - When batch inference or complex queries are scheduled, TX3 pulses the relay to boot Penta, waits for the health check endpoint, executes queued inference jobs, and issues a clean ACPI shutdown before disconnecting standby power if needed.

---

## 3. Software Architecture & Components

The software architecture is decoupled into lightweight, independently deployable services managed by Docker Compose, with a host-level supervisor.

```
                          USER BROWSER / CLIENT
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      WEB (React)    │
                         │   Port 80 / 3000    │
                         │                     │
                         │  - / (Overview)     │
                         │  - /curator         │
                         │  - /brain           │
                         │  - /statistics      │
                         │  - /admin           │
                         └──────────┬──────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌──────────────┐             ┌──────────────┐             ┌──────────────┐
│   CURATOR    │             │    BRAIN     │             │  STATISTICS  │
│  Port 8001   │             │  Port 8002   │             │  Port 8003   │
│              │             │              │             │              │
│ - Ingestion  │             │ - Knowledge  │             │ - Metrics    │
│ - Scanner    │             │   Graph      │             │ - Funnels    │
│ - Normalizer │             │ - Semantic   │             │ - Token      │
│ - Deduplicat.│             │   Search     │             │   Accounting │
│ - Archiver   │             │ - LLM Proxy  │             │ - Growth     │
└──────┬───────┘             └──────┬───────┘             └──────┬───────┘
       │                            │                            │
       └────────────────────────────┼────────────────────────────┘
                                    │
                                    ▼
                      ┌───────────────────────────┐
                      │    CANONICAL KNOWLEDGE    │
                      │     (Mounted /memory)     │
                      │                           │
                      │  - raw/inbox & archive/   │
                      │  - processed/ vault       │
                      │  - second_brain.db        │
                      └───────────────────────────┘
                                    ▲
                                    │
                      ┌─────────────┴─────────────┐
                      │   HOST MANAGER & UPDATER  │
                      │   (Native Armbian Daemon) │
                      │                           │
                      │  - docker-compose control │
                      │  - updates & migrations   │
                      │  - backup automation      │
                      │  - Arduino relay power    │
                      └───────────────────────────┘
```

### Component Breakdown

#### A. Web Frontend (`web/`)
- A single, responsive React single-page application (SPA).
- Acts as the unified glass pane for the entire system:
  - `/`: System Overview, health monitors, quick links, active queues.
  - `/curator`: Data ingestion review, pending inbox items, entity resolutions, pipeline trigger.
  - `/brain`: Conversation with Qwen 27B, semantic note lookup, topic graph explorer.
  - `/statistics`: Growth funnels (Raw → Normalized → Curated → Synthesized), word counts, storage graphs, GPU token consumption.
  - `/admin`: Container versions, update trigger, restart controls, Penta power state toggle.

#### B. Curator Service (`curator/`)
- Pure Python deterministic data pipeline.
- Scans `raw/inbox/` for new files (Markdown, JSON, DB dumps, emails, chat exports).
- Normalizes content, validates YAML frontmatter against schemas, generates canonical IDs, detects duplicates.
- Moves extracted material into `processed/` and moves source files to immutable `raw/archive/`.
- Maintains full provenance links from source to atomized note.

#### C. Brain Service (`brain/`)
- Semantic reasoning and retrieval engine.
- Indexes notes into SQLite FTS5 (Full-Text Search) and vector embeddings (ChromaDB / sqlite-vec).
- Acts as an intelligent proxy to the Penta GPU node (Ollama API), formatting prompts, managing context windows, and queuing requests.

#### D. Statistics Service (`statistics/`)
- Event-driven metrics recorder.
- Aggregates database queries across SQLite:
  - Source metrics: number of sources (e.g. 1 Bildr DB, 3 email accounts, 2 chat exports) vs raw items (e.g. 1,072 items, 15,732 words).
  - Pipeline metrics: conversion rates through the 4 stages.
  - LLM metrics: prompt tokens, completion tokens, inference latency, power runtimes.

#### E. Host Manager (`manager/`)
- Runs directly on the Tanix TX3 Mini Armbian host (not inside a container).
- Prevents the circular dependency of containers attempting to update themselves.
- Provides CLI command `second-brain`:
  - `second-brain update`: Coordinates with Gateway `10.5.5.1`, pulls git/docker images, runs migrations, verifies health, rolls back on error.
  - `second-brain power on|off|status`: Communicates via serial with the Arduino to boot/stop Penta.
  - `second-brain backup`: Creates timestamped archive snapshots of `/mnt/memory`.

---

## 4. Architectural Boundaries & Data Isolation

| Layer | Responsibility | Storage / State |
|---|---|---|
| **Raw Ingest** | Incoming data captures | `raw/inbox/` (Ephemeral until processed) |
| **Raw Archive** | Cryptographic & historical provenance | `raw/archive/` (**Immutable**) |
| **Normalized** | Atomized, schema-compliant Markdown | `processed/` (**Obsidian Vault**) |
| **Synthesized** | Machine insights, graph edges, summaries | `processed/`, SQLite, Embeddings |
| **Application State** | System logs, run metrics, job queues | SQLite (`data/second_brain.db`) |
| **Software Binaries** | Executables, dependencies, web bundles | Docker Images (Stateless) |
