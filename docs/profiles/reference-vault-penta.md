# Reference Hardware Profile: "White Room Vault & Penta"

**Status:** Canonical Reference Profile  
**Subnet:** `10.5.5.0/24` (Isolated Airgapped Vault)  
**Primary Architect:** User (`kreier`)

---

## 1. Overview & Purpose

This document defines the **Canonical Reference Hardware Profile** for the Second Brain project. While the Second Brain software codebase is strictly hardware-agnostic and deployable on any standard machine via `docker-compose.yml` and `settings.yml`, all optimization, performance profiling, and design decisions are validated against this specific physical topology.

When discussing hardware constraints, latency, layer splitting, and power orchestration in conversations with AI assistants, reference this document.

---

## 2. Network Topology & Node Allocation

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
     │  Tanix TX3 Mini   │   (Pulsed power header)     │  "Penta" Workst.  │
     │  ARM64 / Armbian  │                             │  4x Pascal GPUs   │
     │  IP: 10.5.5.2     │                             │  30 GB VRAM       │
     │                   │◄───────────────────────────►│  IP: 10.5.5.5     │
     │  Docker Compose   │       REST / HTTP API       │  Qwen 3.8 27B     │
     │  Services         │       (Port 11434)          │  Ubuntu 24.04 LTS │
     └─────────┬─────────┘                             └───────────────────┘
               │
               │ USB 3.0 High-Speed Mount
               ▼
     ┌───────────────────┐
     │  "MEMORY" STORE   │
     │  External USB SSD │
     │  - /mnt/memory    │
     │  - second_brain.db│
     └───────────────────┘
```

---

## 3. Node Specifications

### Node 1: Gateway (`10.5.5.1`)
- **Role**: Vault perimeter security & network routing.
- **Function**: Default-blocks all internet ingress/egress. Controlled gateway switches internet access on temporarily during scheduled `second-brain update` windows to pull Git commits and container images.

### Node 2: "Brain" (`10.5.5.2` — Tanix TX3 Mini)
- **Role**: 24/7 Always-On Vault Controller & Web Server.
- **Hardware**: Tanix TX3 Mini TV Box.
- **SoC**: Amlogic S905W (Quad-core ARM Cortex-A53 @ 1.2 GHz).
- **RAM**: 2 GB DDR3.
- **OS**: Armbian Linux (Debian/Ubuntu ARM64).
- **Software**: Docker Engine + Docker Compose + `second-brain` host manager.
- **Hosted Services**:
  - `web` (React UI on port 80)
  - `curator` (pipeline engine on port 8001)
  - `brain` (retrieval & proxy on port 8002)
  - `statistics` (SQLite analytics on port 8003)

### Node 3: "Memory" (External USB Storage)
- **Role**: Canonical Persistent Knowledge Store.
- **Mount Point**: `/mnt/memory` on the TX3 Mini.
- **Hardware**: External USB 3.0 SSD formatted with ext4.
- **Contents**:
  - `raw/inbox/` (incoming data)
  - `raw/archive/` (immutable cryptographic source archive)
  - `processed/` (curated Obsidian vault)
  - `second_brain.db` (operational SQLite database)
  - `backups/` (versioned tarballs)

### Node 4: "Intelligence" ("Penta" Workstation @ `10.5.5.5`)
- **Role**: High-Performance Local LLM Inference Engine.
- **OS**: Ubuntu 24.04 LTS (x86_64).
- **CPU**: Intel Core i3-6100 (2 cores / 4 threads @ 3.70 GHz).
- **System Memory**: 16 GB DDR4 RAM.
- **Storage**: 256 GB NVMe SSD.
- **GPU Subsystem (Quad-GPU Pascal Architecture — 30 GB Total VRAM)**:
  | Slot / GPU | Model | Architecture | VRAM | Bus / Notes |
  |---|---|---|---|---|
  | **GPU 0** | NVIDIA GeForce GTX 1070 | Pascal (GP104) | 8 GB GDDR5 | PCIe x16 (Display capable) |
  | **GPU 1** | NVIDIA P104-100 | Pascal (GP104) | 8 GB GDDR5X | Dedicated compute / headless |
  | **GPU 2** | NVIDIA P104-100 | Pascal (GP104) | 8 GB GDDR5X | Dedicated compute / headless |
  | **GPU 3** | NVIDIA P106-100 | Pascal (GP106) | 6 GB GDDR5 | Dedicated compute / headless |
  | **TOTAL** | **4x Pascal GPUs** | | **30 GB VRAM** | High-throughput tensor parallelism |
- **Inference Stack**:
  - Ollama or llama.cpp multi-GPU layer split (`-ngl` offloaded across all 4 devices).
  - Primary Model: **Qwen 3.8 27B** (or Qwen 2.5 27B quantized to Q4_K_M / Q5_K_M, taking ~18–22 GB VRAM plus KV cache).
  - Port: `10.5.5.5:11434`.

---

## 4. Hardware Power Orchestration Link

Due to the idle power draw of four GPUs, a desktop power supply, and cooling fans, Penta is powered **only on-demand**:

1. **Physical Link**:
   - The TX3 Mini has a USB-attached Arduino Uno/Nano.
   - An optical-isolated relay module on the Arduino connects directly across the `POWER_SW` pins of Penta's motherboard header.
2. **On-Demand Cycle**:
   - TX3 `second-brain` manager detects pending inference jobs or receives a UI trigger.
   - Manager sends serial pulse command to Arduino (`PULSE_500MS`).
   - Relay contact closes momentarily, simulating a power button press.
   - Penta boots Ubuntu 24.04 and starts the Ollama systemd service.
   - TX3 polls `http://10.5.5.5:11434/api/tags` until HTTP 200 is returned.
   - Queued inference jobs are processed.
   - When idle for 15 minutes, TX3 issues `ssh mk@10.5.5.5 sudo shutdown -h now` for clean ACPI shutdown.
