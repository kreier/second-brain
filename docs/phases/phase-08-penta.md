# Phase 8 — Penta GPU Intelligence & LLM Integration

**Status:** Scheduled  
**Target Environment:** Airgapped Vault Subnet (`10.5.5.0/24`)  
**Prerequisites:** [Phase 3](phase-03-brain.md), [Phase 7](phase-07-tx3.md)

---

## 1. Objective
Integrate the dedicated "Penta" intelligence workstation equipped with **four Pascal Nvidia GPUs** (30 GB total VRAM) into the airgapped vault network. Configure local inference serving for **Qwen 3.8 27B** via Ollama or vLLM / llama.cpp, connect the TX3 Brain proxy to Penta over HTTP, and implement offline batch processing queues.

---

## 2. Deliverables
- [ ] Penta workstation inference configuration:
  - Multi-GPU driver & CUDA setup for 4x Pascal GPUs.
  - Model weights deployment for Qwen 3.8 27B quantized to fit comfortably inside 30 GB VRAM.
  - Local Ollama or llama.cpp multi-GPU server exposing port 11434.
- [ ] Network integration on vault subnet `10.5.5.0/24`.
- [ ] Brain service proxy routing to Penta with connection pooling and timeouts.
- [ ] Offline batch inference queue (accumulating synthesis jobs while Penta is powered off).
- [ ] Token accounting recorder logging prompt/completion metrics to SQLite.

---

## 3. Acceptance Criteria
```text
[ ] Penta boots and runs Qwen 3.8 27B inference across 4 Pascal GPUs without out-of-memory errors
[ ] TX3 Brain node connects to Penta API over vault network and receives streaming completions
[ ] Batch inference tasks queued while Penta is offline are processed upon connection
[ ] Inference metrics (latency, tokens/sec, prompt/completion counts) are recorded in SQLite
[ ] Entire inference cycle executes completely offline with zero external network traffic
```
