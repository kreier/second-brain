# Phase 9 — Automated Penta Power Management (TX3 → Arduino → Relay)

**Status:** Scheduled  
**Target Environment:** Airgapped Vault Subnet (`10.5.5.0/24`)  
**Prerequisites:** [Phase 7](phase-07-tx3.md), [Phase 8](phase-08-penta.md)

---

## 1. Objective
Automate the physical power lifecycle of the heavy Penta GPU workstation to conserve electricity and minimize heat. The TX3 Mini controls an Arduino microcontroller via USB serial, which energizes a relay connected to Penta's motherboard power header pins. When batch inference or intensive tasks are queued, TX3 powers on Penta, waits for health readiness, drains the job queue, requests a clean operating system shutdown via ACPI/SSH, and disconnects standby power.

---

## 2. Deliverables
- [ ] Arduino firmware (`scripts/power-relay/firmware.ino`) to receive serial pulse commands and safely toggle relay contacts.
- [ ] Host Manager power module (`manager/power.py` / CLI `second-brain power`):
  - Serial communication protocol with Arduino.
  - Motherboard power switch momentary contact simulation (pulsing for 500ms).
- [ ] Penta boot watcher and health probe (polling `http://penta:11434/api/tags` until ready).
- [ ] Safe shutdown orchestrator:
  - Issues clean OS shutdown command over SSH (`sudo shutdown -h now`).
  - Monitors ping/network loss to confirm machine is fully off.
- [ ] Automated queue trigger: wakes Penta on scheduled cron batch or manual Web UI button press, then shuts down when queue is empty.

---

## 3. Power Lifecycle State Machine

```
              ┌────────────────────────────────────────┐
              ▼                                        │
        [ PENTA OFF ]                                  │
              │                                        │
              │ Queue threshold reached OR User click  │
              ▼                                        │
        [ RELAY PULSE ] (Arduino closes contact 500ms) │
              │                                        │
              ▼                                        │
        [ BOOTING ] (TX3 polls health port 11434)      │
              │                                        │
              ▼                                        │
        [ READY & PROCESSING ] (Executing batch tasks) │
              │                                        │
              │ Queue drained & idle timeout expires   │
              ▼                                        │
        [ SHUTDOWN SIGNAL ] (SSH 'shutdown -h now')    │
              │                                        │
              ▼                                        │
        [ POWER CUT / IDLE ] ──────────────────────────┘
```

---

## 4. Acceptance Criteria
```text
[ ] second-brain power on sends pulse via Arduino and powers on the Penta machine
[ ] TX3 Mini detects when Penta becomes responsive and begins batch job dispatch
[ ] second-brain power off triggers graceful Linux shutdown on Penta
[ ] In case of inference hang, watchdog timer forces safe shutdown after configurable timeout
[ ] Power events (boot, duration, shutdown, reason) are logged in SQLite power_events table
[ ] Web UI at /admin displays real-time Penta power status and provides manual on/off override
```
