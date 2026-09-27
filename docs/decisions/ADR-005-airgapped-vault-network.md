# ADR-005: Airgapped "White Room" Network Subnet (10.5.5.0/24)

**Status:** Accepted  
**Date:** 2026-09-27  
**Deciders:** User, ChatGPT Architect

---

## Context
Personal knowledge vaults contain private, sensitive data: personal reflections, unreleased projects, credentials, correspondence, and medical/financial records. Connecting an AI system directly to the internet or commercial cloud APIs creates persistent data leakage risks and privacy exposure.

## Decision
The Second Brain hardware operates on a physically or logically isolated subnet `10.5.5.0/24`:
- **Gateway (`10.5.5.1`)**: Firewall default-deny; blocks all outbound/inbound traffic. It can be temporarily toggled open exclusively by administrative command during software update windows.
- **Brain Node (`10.5.5.2`)**: Tanix TX3 Mini running Armbian.
- **Intelligence Node ("Penta")**: Compute workstation with 4x Pascal GPUs (30 GB VRAM) running local weights (Qwen 3.8 27B) offline.
- **Memory Store**: Physical USB storage attached to TX3 Mini.

All model inference, vector embedding, and text analysis happen 100% locally on the Penta workstation without leaving the subnet.

## Consequences
- **Positive**: Total privacy, sovereign execution, immunity to cloud service outages or terms-of-service changes.
- **Negative**: Updating software requires an explicit temporary gateway unlock step; models must fit into local GPU VRAM.
