# PRESS»SEAL — Rumuno Vault

**Provably survivable state for autonomous agents. Kill the process. The state doesn't die.**

Copyright © 2025-2026 Jack Wolf Edwards ALL RIGHTS RESERVED
Fingerprint seed: JAXW01F_LUWO_LUNA_369
$LUWO — For Luna, authored by JAXW01F 🐺 — ALUMUNO Technologies Inc.
NO AI owns this code.

---

## What this is

A columnar vault for machine-generated state — built for the era of 24/7 autonomous agents that never stop writing data. This repo demonstrates the proof layer of the LUWO stack:

- **PRESS** — state is compressed via columnar LUWO geometry (engine: https://github.com/Alumuno-Tech/luwo-compression)
- **SEAL** — every cycle is sealed with a SHA-256 digest
- **RECEIPT** — sealed state hashes are stamped on Solana mainnet as immutable receipts
- **RESTORE** — sealed state survives the death of the process that wrote it

## The Vulture Protocol — prove it yourself

Don't take our word for it. Kill our agent yourself:

    pip install -r requirements.txt
    python3 assassin.py

The assassin spawns a vault worker, lets it seal cycles, then murders it with SIGKILL — no cleanup, no warning, no mercy. The vault state survives. The seals verify. That's the whole test.

## On-chain receipt

Sealed state hashes are stamped to Solana mainnet:

https://explorer.solana.com/tx/547cRfHaieS5q7B3W2nKFS1eAhNSBkMD8AWTUZBeHsPy7J6LctdFaoBTtYVXBAMyehyfoYKdi7Kt3MF5UsE2ZiEa?cluster=mainnet-beta

## Sample telemetry

`data/sample/telemetry_sample.jsonl` contains sanitized real telemetry from an autonomous trading node (Raspberry Pi 5, 24/7 operation). API keys, secrets, tokens, passphrases, and wallet addresses removed.

## Repository layout

| File | Purpose |
|------|---------|
| `assassin.py` | Vulture Protocol — kill test harness |
| `worker.py` | Agent that writes sealed state to the vault |
| `solana_receipt.py` | Mainnet receipt stamper (requires funded keypair) |
| `src/store.py` | PressedVault — the columnar sealed store |
| `data/sample/` | Sanitized real telemetry corpus |

## License

See LICENSE. Math private, benchmarks public.
