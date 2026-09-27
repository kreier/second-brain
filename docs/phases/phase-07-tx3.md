# Phase 7 — Tanix TX3 Mini Deployment & Host Integration

**Status:** Scheduled  
**Target Environment:** Tanix TX3 Mini (`10.5.5.2`) running Armbian  
**Prerequisites:** [Phase 5 — Compose & Packaging](phase-05-compose.md)

---

## 1. Objective
Deploy the Second Brain platform onto the target physical ARM64 hardware: the Tanix TX3 Mini TV box running Armbian Linux at static IP `10.5.5.2`. Connect and configure the external USB storage as `/mnt/memory`, verify low-power operation, and install the native `second-brain` Host Manager daemon.

---

## 2. Deliverables
- [ ] Armbian Linux provisioning guide and configuration scripts for the Tanix TX3 Mini (Amlogic S905W).
- [ ] Persistent storage automount configuration (fstab/systemd) for the external USB drive at `/mnt/memory`.
- [ ] Native Host Manager CLI (`second-brain`) installed at `/usr/local/bin/second-brain`.
- [ ] Host-level update script coordinating temporary network access with Gateway `10.5.5.1`.
- [ ] Hardware resource monitoring (CPU thermal throttling, RAM footprint under 2GB).

---

## 3. Acceptance Criteria
```text
[ ] TX3 Mini boots Armbian and connects with static IP 10.5.5.2 on subnet 10.5.5.0/24
[ ] External USB storage automounts reliably to /mnt/memory with write permissions
[ ] second-brain start launches all containers successfully via Docker Compose
[ ] System idle RAM remains under 1.2 GB of the available 2 GB
[ ] Web interface is accessible from any client on the 10.5.5.0/24 subnet at http://10.5.5.2
[ ] second-brain update successfully pulls latest images when gateway provides internet access
```
