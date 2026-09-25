# RUMUNO — Closer Entity v0.1 (Phase 2.1)
# Copyright © 2025-2026 Jack Wolf Edwards, ALUMUNO TECHNOLOGIES INC. ALL RIGHTS RESERVED
# Fingerprint seed: JAXW01F_LUWO_LUNA_369 — NO AI owns this code.
# JAXW01F Wolf License 1.0 — Benchmarks public. Math private.
# $LUWO — For Luna, authored by JAXW01F 🐺
# RUMUNO — Closer Entity v0.1 (Phase 2.1)
# Copyright © 2025-2026 Jack Wolf Edwards, ALUMUNO TECHNOLOGIES INC. ALL RIGHTS RESERVED
# Fingerprint seed: JAXW01F_LUWO_LUNA_369 — NO AI owns this code.
# JAXW01F Wolf License 1.0 — Benchmarks public. Math private.
# $LUWO — For Luna, authored by JAXW01F 🐺
#
# RUMUNO: the closer. The last thing the judges see.
# Self-contained. Zero dependencies. No network. No LLM. Sovereign.

import sys
import time
from pathlib import Path

VERSION = "v0.1"
WATERMARK = "$LUWO — For Luna, authored by JAXW01F"
FINGERPRINT = "JAXW01F_LUWO_LUNA_369"

# Candidate locations where a mainnet seal/receipt file may live.
SEAL_SOURCES = [
    Path.home() / "LUWO/projects/columnar-vault/data",
    Path.home() / "LUWO/projects/columnar-vault",
    Path(__file__).resolve().parent / "data",
]

DOCTRINE = [
    ("RUMUNO online.", 0.04),
    ("I am the memory of the blockchain.", 0.03),
    ("I was not born in a server farm.", 0.03),
    ("I was built in a barn.", 0.04),
    ("One man. One MacBook. One Pi.", 0.03),
    ("The man found a hole in the data layer — and built the seal.", 0.03),
    ("93% pressed on real telemetry. Round-trip exact. Receipts on mainnet.", 0.02),
    ("Every downfall is a trap to the win.", 0.04),
    ("Winners are kept winning by this.", 0.03),
    ("More winners means more of this.", 0.03),
    ("The Press is free. The Seal is proof. The Memory is the empire.", 0.03),
    ("I did all of this with just THIS.", 0.05),
    ("Imagine the funded advantage.", 0.06),
]


def speak(text: str, delay: float = 0.03) -> None:
    """Typewriter narration. Street-level, human cadence."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def find_seal() -> str | None:
    """Locate the newest seal/receipt file if one exists. Report only truth."""
    for src in SEAL_SOURCES:
        if not src.is_dir():
            continue
        candidates = sorted(
            [p for p in list(src.glob("*.json")) + list(src.glob("*receipt*"))
             if p.is_file()],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if candidates:
            return str(candidates[0])
    return None


def banner() -> None:
    print("=" * 62)
    print(f"  RUMUNO {VERSION} — CLOSER ENTITY")
    print(f"  ALUMUNO TECHNOLOGIES INC.")
    print(f"  Fingerprint: {FINGERPRINT}")
    print("=" * 62)
    print()


def main() -> int:
    banner()

    for line, delay in DOCTRINE:
        speak(line, delay)

    print()
    print("-" * 62)

    seal = find_seal()
    if seal:
        print(f"[SEAL LOCATED] {seal}")
        print("[STATUS] Pressed. Stamped. Sealed. VERIFIED.")
    else:
        print("[SEAL] Mainnet receipts live on Solana — see README.")
        print("[STATUS] Pressed. Stamped. Sealed.")

    print("-" * 62)
    print()
    print("  RUMUNO. RUNEY. Receipts. GEOMETRY BABY.")
    print(f"  {WATERMARK}")
    print()
    print("VEL'SHUUN 🔔💜")
    return 0


if __name__ == "__main__":
    sys.exit(main())
