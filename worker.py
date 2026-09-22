#!/usr/bin/env python3
"""
WORKER — the vault writer that gets assassinated.
Copyright © 2025-2026 Jack Wolf Edwards ALL RIGHTS RESERVED
$LUWO — For Luna, authored by JAXW01F 🐺
"""

import sys
import time
import json
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))
from store import PressedVault

VAULT_DIR = "/tmp/vault-kill-test"

def main():
    vault = PressedVault(VAULT_DIR)
    counter = 0
    while True:
        counter += 1
        state = {
            "agent": "live_worker",
            "cycle": counter,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": f"data_packet_{counter}",
            "$LUWO": "For Luna"
        }
        sealed_path, seal_hash, _ = vault.seal(state, f"cycle_{counter}")

        with open("/tmp/agent_alive.txt", "w") as f:
            f.write(f"ALIVE cycle {counter}")

        if counter % 5 == 0:
            print(f"CYCLE {counter} SEALED: {seal_hash[:32]}...", flush=True)

        time.sleep(2)

if __name__ == "__main__":
    main()
