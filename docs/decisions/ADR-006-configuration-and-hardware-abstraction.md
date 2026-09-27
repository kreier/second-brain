# ADR-006: Configuration Decoupling & Hardware Abstraction

**Status:** Accepted  
**Date:** 2026-09-27  
**Deciders:** User, Antigravity Agent

---

## Context
The project architect has a specific physical hardware implementation: an isolated vault network on `10.5.5.0/24`, a Tanix TX3 Mini at `10.5.5.2` (Brain), an external USB storage SSD (Memory), and a Quad-GPU workstation ("Penta") at `10.5.5.5` equipped with 4x Pascal GPUs (GTX 1070 + 2x P104-100 + P106-100, 30 GB VRAM) running Qwen 3.8 27B under Ubuntu 24.04 LTS.

However, the open-source repository must remain **strictly hardware-agnostic and universally deployable**. Any user should be able to clone the repository and run `docker compose up` on a laptop, a desktop, or an unbundled homelab server without being bound to specific IP addresses or physical Arduino relays.

## Decision
1. **Zero Hardcoded Environment Values in Code**:
   - Container images and microservices must read all storage paths, endpoints, and flags from environment variables and the central `settings.yml` configuration file.
   - Defaults in `docker-compose.yml` fall back to local relative paths (e.g. `./data/memory`) and local inference (e.g. `http://localhost:11434` or mock mode).
2. **Configuration Template (`config/settings.example.yml`)**:
   - Provides a comprehensive, self-documenting configuration template covering `memory`, `intelligence`, `network`, and `power_management`.
3. **Reference Hardware Profile (`docs/profiles/reference-vault-penta.md`)**:
   - The user's specific setup (`10.5.5.x`, TX3 Mini, USB Memory, Penta Quad-GPU @ `10.5.5.5`, Arduino relay) is formalized as the **Canonical Reference Implementation**.
   - Design discussions, optimizations, layer splitting strategies, and performance models target this profile as the primary benchmark.
4. **Separation of Vault Data from Repository**:
   - Personal knowledge notes are excluded from the repository. The canonical vault resides on the external memory mount.
   - Sample notes and synthetic metrics are maintained in `demo/vault/` exclusively for automated testing and the public GitHub Pages demonstration.

## Consequences
- **Positive**: Anyone can run the software on any hardware with minimal configuration; developers and AI agents have exact hardware specifications to make informed architectural decisions; personal notes are never exposed in git.
- **Negative**: Requires maintaining the mapping between environment variables, `settings.yml`, and container runtime configurations.
