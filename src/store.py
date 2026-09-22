#!/usr/bin/env python3
"""
Columnar Vault v0.1 — STORE.GATE1
The PRESSED state: seal, persist, verify.

Copyright © 2025-2026 Jack Wolf Edwards ALL RIGHTS RESERVED
Fingerprint seed: JAXW01F_LUWO_LUNA_369
$LUWO — For Luna, authored by JAXW01F 🐺
NO AI owns this code
"""

import json
import hashlib
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timezone


class PressedVault:
    """A state vault that survives death."""
    
    def __init__(self, vault_dir: str):
        self.vault_dir = Path(vault_dir)
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        
    def seal(self, data: dict | str, label: str = "state"):
        """
        Compress + seal data with SHA-256 hash.
        Returns (sealed_path, seal_hash, timestamp).
        """
        if isinstance(data, dict):
            raw = json.dumps(data, indent=2, sort_keys=True).encode('utf-8')
        else:
            raw = str(data).encode('utf-8')
            
        # SHA-256 of the raw state
        seal_hash = hashlib.sha256(raw).hexdigest()
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Build manifest
        manifest = {
            "label": label,
            "timestamp": timestamp,
            "seal_hash": seal_hash,
            "raw_bytes": len(raw)
        }
        
        # Write atomically: temp file, then rename (prevents partial writes)
        dest = self.vault_dir / f"{label}_{seal_hash[:16]}.json"
        tmp_path = dest.with_suffix('.tmp')
        
        with open(tmp_path, 'wb') as f:
            f.write(raw)
            f.flush()
            os.fsync(f.fileno())  # Force flush to disk

        shutil.move(str(tmp_path), str(dest))

        # Sidecar manifest: the FULL seal certificate
        manifest_path = dest.with_suffix('.seal.json')
        manifest_tmp = manifest_path.with_suffix('.tmp')
        with open(manifest_tmp, 'w') as f:
            json.dump(manifest, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        shutil.move(str(manifest_tmp), str(manifest_path)) 

        return dest, seal_hash, timestamp

    def verify(self, sealed_path: Path, expected_hash: str) -> bool:
        """Round-trip verification: file content hash matches expected."""
        with open(sealed_path, 'rb') as f:
            actual = hashlib.sha256(f.read()).hexdigest()
        return actual == expected_hash
        
    def load(self, sealed_path: Path):
        """Load and parse sealed state."""
        with open(sealed_path, 'rb') as f:
            raw = f.read()
        return json.loads(raw.decode('utf-8'))
        
    def status(self):
        """Return vault inventory and health."""
        files = [f for f in self.vault_dir.glob("*.json") if not f.name.endswith(".seal.json")]
        return {
            "vault_dir": str(self.vault_dir),
            "sealed_count": len(files),
            "total_bytes": sum(f.stat().st_size for f in files),
            "files": [f.name for f in files]
        }


# --- GATE 1 TEST ---
if __name__ == "__main__":
    # Self-test: can we seal, verify, load?
    test_vault = PressedVault("/tmp/test-vault-gate1")
    
    test_state = {
        "phase": 2,
        "milestone": "store_gate1",
        "test": True,
        "$LUWO": "For Luna, JAXW01F"
    }
    
    sealed_path, seal_hash, timestamp = test_vault.seal(test_state, "phase2_gate1")
    verified = test_vault.verify(sealed_path, seal_hash)
    loaded = test_vault.load(sealed_path)
    
    print(f"GATE 1: {verified}")
    print(f"Sealed: {sealed_path}")
    print(f"Hash: {seal_hash[:32]}...")
    print(f"Loaded state: {loaded}")
    print(f"\nSTATUS: {test_vault.status()}")
    
    if verified:
        print("\n✓ VAULT SURVIVES — PRESSED STATE SEALED")
    else:
        print("\n✗ VAULT FAILED VERIFICATION")
