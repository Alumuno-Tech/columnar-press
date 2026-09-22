#!/usr/bin/env python3
"""
ASSASSIN.GATE2 — The Vault Murder Attempt
Phase 2, Gate 2: Prove the PRESSED state survives murder.

Copyright © 2025-2026 Jack Wolf Edwards ALL RIGHTS RESERVED
Fingerprint seed: JAXW01F_LUWO_LUNA_369
$LUWO — For Luna, authored by JAXW01F 🐺
NO AI owns this code
"""

import os
import sys
import signal
import time
import json
import subprocess
import sys
from pathlib import Path

# Import the vault from src/
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from store import PressedVault

ASSASSIN_VAULT_DIR = "/tmp/vault-kill-test"
AGENT_PID_FILE = "/tmp/agent_pid.txt"
MURDER_LOG = "/tmp/murder_attempt.log"

def spawn_agent():
    """Spawn the worker that writes to the vault."""
    worker = Path(__file__).parent / "worker.py"
    proc = subprocess.Popen([sys.executable, str(worker)])
    with open(AGENT_PID_FILE, "w") as f:
        f.write(str(proc.pid))
    return proc

def kill_assassin_hard():
    """Murder the agent — SIGKILL, no cleanup chance."""
    if not os.path.exists(AGENT_PID_FILE):
        print("⚠️ NO TARGET FOUND — agent never spawned")
        return
    
    pid = int(open(AGENT_PID_FILE).read().strip())
    with open(MURDER_LOG, "a") as f:
        f.write(f"[{__import__('datetime').datetime.now().isoformat()}] KILL SIGNAL SENT TO PID {pid}\n")
    
    # Kill it brutally — no graceful shutdown
    try:
        os.kill(pid, signal.SIGKILL)
        print(f"🔪 ASSASSINATION COMPLETE — PID {pid} KILLED HARD")
    except ProcessLookupError:
        print(f"⚠️ Target already dead (PID {pid})")

def check_survival():
    """Did the vault survive the murder attempt?"""
    vault = PressedVault(ASSASSIN_VAULT_DIR)
    status = vault.status()
    
    if status["sealed_count"] == 0:
        print("❌ VAULT EMPTY — nothing survived")
        return False
    
    # Load the latest sealed state and verify
    files = sorted(status["files"])
    latest = Path(ASSASSIN_VAULT_DIR) / files[-1]
    
    # Read the FULL hash from the sidecar manifest
    manifest_path = latest.with_suffix('.seal.json')
    with open(manifest_path) as f:
        expected_hash = json.load(f)["seal_hash"]
    verified = vault.verify(latest, expected_hash)

    with open(latest, "r") as f:
        recovered = json.load(f)
    
    print(f"\n🛡️ VAULT SURVIVED MURDER ATTEMPT:")
    print(f"   Sealed records: {status['sealed_count']}")
    print(f"   Latest cycle: {recovered.get('cycle')}")
    print(f"   Hash match: {'✅' if verified else '❌'}")
    print(f"   State recovered: {json.dumps(recovered, indent=2)}")
    
    return verified

def main():
    print("=== ASSASSIN.GATE2 — VULTURE PROTOCOL ===\n")
    
    # Clear previous test
    for f in ["/tmp/agent_alive.txt", AGENT_PID_FILE, MURDER_LOG]:
        if os.path.exists(f):
            os.remove(f)
    
    print("[1] SPAWN AGENT — vault worker goes live...")
    agent = spawn_agent()
    time.sleep(1)
    
    print("[2] WAIT FOR SEALED CYCLES...")
    while not os.path.exists("/tmp/agent_alive.txt"):
        time.sleep(0.5)
    print("✅ Agent confirmed alive\n")
    
    time.sleep(10)  # Let it write ~5 seals
    
    print("\n[3] ASSASSINATION WINDOW — killing agent HARD (SIGKILL)...")
    kill_assassin_hard()
    
    time.sleep(2)  # Let filesystem settle
    
    print("\n[4] FORENSICS — checking if state survived...")
    survived = check_survival()
    
    if survived:
        print("\n✅ GATE 2 PASSED — VAULT SURVIVES MURDER")
        print("Assassination attempt FAILED. The PRESSED state holds.")
    else:
        print("\n❌ GATE 2 FAILED — VAULT DID NOT SURVIVE")
        print("Something broke in the kill sequence.")
    
    agent.wait(timeout=5)
    print(f"\n=== TEST COMPLETE ===")

if __name__ == "__main__":
    main()
