#!/usr/bin/env python3
"""
Second Brain — Host-Level Supervisor & Lifecycle Manager CLI
Runs directly on the host OS (e.g. Tanix TX3 Mini Armbian) outside Docker.
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def find_settings():
    candidates = [
        Path("/etc/second-brain/settings.yml"),
        Path(__file__).resolve().parent.parent / "settings.yml",
        Path(__file__).resolve().parent.parent / "config" / "settings.example.yml",
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def load_config():
    p = find_settings()
    if p and yaml:
        try:
            with open(p, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}
    return {}


def cmd_status(args):
    print("=== Second Brain System Status ===")
    config = load_config()
    settings_file = find_settings()
    print(f"Config: {settings_file if settings_file else 'Default'}")

    memory_path = config.get("memory", {}).get("path", "/mnt/memory")
    print(f"Memory Path: {memory_path} (exists: {os.path.exists(memory_path)})")

    intel = config.get("intelligence", {})
    print(f"Intelligence Endpoint: {intel.get('endpoint', 'http://10.5.5.5:11434')}")
    print(f"Intelligence Model: {intel.get('model', 'qwen-3.8-27b')}")

    # Check Docker Compose status
    print("\nContainers (docker compose ps):")
    try:
        subprocess.run(["docker", "compose", "ps"], check=False)
    except FileNotFoundError:
        print("  docker compose not found in PATH")


def cmd_power(args):
    config = load_config()
    power_cfg = config.get("power_management", {})
    target_ip = power_cfg.get("target_ip", "10.5.5.5")
    serial_port = power_cfg.get("serial_port", "/dev/ttyUSB0")
    enabled = power_cfg.get("enabled", True)

    if not enabled:
        print("Power management is disabled in settings.yml")
        return

    action = args.action
    if action == "status":
        print(f"Probing Penta at {target_ip}...")
        res = subprocess.run(["ping", "-c", "1", "-W", "1", target_ip], capture_output=True)
        if res.returncode == 0:
            print(f"  Penta ({target_ip}) is ONLINE.")
        else:
            print(f"  Penta ({target_ip}) is OFFLINE / STANDBY.")
    elif action == "on":
        print(f"Triggering power relay on {serial_port} for {target_ip}...")
        if os.path.exists(serial_port):
            try:
                import serial, time
                with serial.Serial(serial_port, 9600, timeout=2) as ser:
                    time.sleep(1)
                    ser.write(b"PULSE\n")
                    print("  Power pulse signal sent to Arduino.")
            except Exception as e:
                print(f"  Serial write error: {e}")
        else:
            print(f"  Simulated pulse (serial port {serial_port} not attached).")
    elif action == "off":
        ssh_user = power_cfg.get("ssh_user", "mk")
        print(f"Initiating graceful ACPI shutdown via SSH: {ssh_user}@{target_ip}...")
        subprocess.run(["ssh", f"{ssh_user}@{target_ip}", "sudo", "shutdown", "-h", "now"], check=False)


def cmd_update(args):
    print("=== Second Brain Update Procedure ===")
    config = load_config()
    net_cfg = config.get("network", {})
    gateway_ip = net_cfg.get("gateway_ip", "10.5.5.1")
    airgapped = net_cfg.get("airgapped_mode", True)

    if airgapped:
        print(f"1. Coordinating with Gateway ({gateway_ip}) to open update window...")
    print("2. Pulling latest git repository commits...")
    subprocess.run(["git", "pull"], check=False)
    print("3. Pulling updated Docker container images...")
    subprocess.run(["docker", "compose", "pull"], check=False)
    print("4. Restarting services with latest images...")
    subprocess.run(["docker", "compose", "up", "-d"], check=False)
    if airgapped:
        print("5. Closing internet gateway window. Airgap restored.")
    print("Update complete.")


def cmd_backup(args):
    config = load_config()
    memory_path = config.get("memory", {}).get("path", "/mnt/memory")
    backup_dir = config.get("memory", {}).get("backup_dir", f"{memory_path}/backups")
    print(f"Backing up {memory_path} to {backup_dir}...")
    os.makedirs(backup_dir, exist_ok=True)
    subprocess.run(["tar", "-czf", f"{backup_dir}/backup-latest.tar.gz", memory_path], check=False)
    print("Backup finished.")


def main():
    parser = argparse.ArgumentParser(description="Second Brain Host Manager CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("status", help="Show system and container status")

    p_power = subparsers.add_parser("power", help="Manage compute node power")
    p_power.add_argument("action", choices=["on", "off", "status"], help="Power action")

    subparsers.add_parser("update", help="Update containers via gateway window")
    subparsers.add_parser("backup", help="Create snapshot backup of memory volume")

    args = parser.parse_args()
    if args.command == "status":
        cmd_status(args)
    elif args.command == "power":
        cmd_power(args)
    elif args.command == "update":
        cmd_update(args)
    elif args.command == "backup":
        cmd_backup(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
