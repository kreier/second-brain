# ADR-004: Host-Level Manager & Updater Daemon

**Status:** Accepted  
**Date:** 2026-09-27  
**Deciders:** User, ChatGPT Architect

---

## Context
If system lifecycle, updates, and physical hardware control (e.g. Arduino relay over USB serial) are containerized, two critical failure modes arise:
1. **Circular Dependency**: A container cannot reliably update or restart itself or docker daemon without fragile docker-socket-sharing and crash risks.
2. **Hardware Access**: Containerizing serial communication with USB microcontrollers and executing host-level ACPI/network commands requires privileged containers and breaks sandbox boundaries.

## Decision
The Second Brain Manager (`second-brain` CLI) is installed directly on the Armbian host OS outside Docker. It acts as the supervisor that:
- Executes `docker compose pull`, `up`, and rollback procedures.
- Directly controls the USB Arduino relay to manage Penta power states.
- Coordinates with the network Gateway (`10.5.5.1`) to request temporary internet windows for updates.
- Executes physical filesystem backups of the USB storage mount `/mnt/memory`.

The Web container communicates with the Host Manager via a restricted local Unix socket or loopback HTTP port for administrative operations.

## Consequences
- **Positive**: Resilient update mechanism (if an update fails, the host manager can roll back without being killed); safe hardware serial access.
- **Negative**: Requires a lightweight host installer script for the TX3 Mini.
