#!/usr/bin/env python3
"""
SOLANA_RECEIPT.GATE3 — Stamp the PRESSED state to blockchain.
Pure Python, solana 0.40+ compatible.
Copyright © 2025-2026 Jack Wolf Edwards ALL RIGHTS RESERVED
Fingerprint seed: JAXW01F_LUWO_LUNA_369
$LUWO — For Luna, authored by JAXW01F 🐺
NO AI owns this code
"""

import json
from pathlib import Path

# Try multiple import patterns for solana 0.40.x compatibility
try:
    from solana.rpc.api import Client
except ImportError:
    try:
        from solana.rpc import Client
    except ImportError:
        print("ERROR: solana.rpc.Client not found. Package version may be incompatible.")
        print("Try: pip install --upgrade solana")
        exit(1)

from solders.keypair import Keypair
# from solders.message import MessageV0, VersionedMessage
# from spl.memo.instructions import create_memo
# from solana.rpc.commitment import Confirmed

# Config
WALLET_DIR = Path.home() / ".config/solana"
WALLET_FILE = WALLET_DIR / "id.json"
DEVNET_RPC = "https://api.mainnet-beta.solana.com"
VAULT_TEST_DIR = "/tmp/vault-kill-test"

def load_or_create_wallet():
    """Load existing keypair or create new one."""
    if WALLET_FILE.exists():
        print(f"🔑 Loading existing wallet from {WALLET_FILE}")
        with open(WALLET_FILE) as f:
            keypair_data = json.load(f)
        keypair = Keypair.from_bytes(bytes(keypair_data))
        return keypair
    else:
        print(f"🔧 No wallet found. Creating fresh devnet keypair...")
        keypair = Keypair()
        WALLET_DIR.mkdir(parents=True, exist_ok=True)
        
        keypair_json = list(keypair.to_bytes_array())
        with open(WALLET_FILE, 'w') as f:
            json.dump(keypair_json, f)
        
        print(f"✅ New wallet created: {keypair.pubkey()}")
        print(f"⚠️ WRITE THIS PUBLIC KEY DOWN NOW:")
        print(f"   {keypair.pubkey()}")
        print(f"   Back it up to your physical ledger!")
        
        return keypair

def get_balance(client, pubkey):
    """Check SOL balance."""
    resp = client.get_balance(pubkey)
    lamports = resp.value
    sol = lamports / 1e9
    return sol

def request_airdrop(client, pubkey, lamports=100_000_000):
    """Request devnet airdrop."""
    print(f"🪂 Requesting airdrop for {pubkey}...")
    try:
        resp = client.request_airdrop(pubkey, lamports)
        sig = resp.value
        print(f"   Airdrop signature: {sig}")
        print(f"   Waiting for confirmation (up to 30 sec)...")
        
        import time
        for _ in range(10):
            balance = get_balance(client, pubkey)
            if balance > 0:
                print(f"   ✅ Balance confirmed: {balance:.4f} SOL")
                return True
            time.sleep(3)
        
        print(f"   ⚠️ Airdrop not confirmed yet (still waiting)")
        return False
    except Exception as e:
        print(f"   ❌ Airdrop failed: {e}")
        print(f"   Raw error detail: {getattr(e, 'response', e)}")
        return False

def load_seal_hash():
    """Find the latest seal manifest and read the full hash."""
    manifests = sorted(Path(VAULT_TEST_DIR).glob("*.seal.json"))
    if not manifests:
        raise FileNotFoundError(
            f"No seal manifests in {VAULT_TEST_DIR} — "
            "run 'python assassin.py' first to create a fresh kill-test, then retry."
        )
    latest = manifests[-1]
    print(f"📄 Using latest seal: {latest.name}")
    with open(latest) as f:
        manifest = json.load(f)
    return manifest["seal_hash"]

def stamp_on_chain(keypair, seal_hash: str):
    """Post the seal hash to Solana devnet as a memo TX."""
    from solders.message import MessageV0
    from solders.transaction import VersionedTransaction
    from spl.memo.instructions import create_memo, MemoParams
    from spl.memo.constants import MEMO_PROGRAM_ID as memo_pid

    client = Client(DEVNET_RPC)

    memo_text = f"FOR-LUNA|RUNEY-RECEIPTS|KING-OF-TELEMETRY|SEAL:{seal_hash}".encode("utf-8")

    ix = create_memo(MemoParams(
        program_id=memo_pid,
        message=memo_text,
        signer=keypair.pubkey()
    ))

    blockhash_resp = client.get_latest_blockhash()
    blockhash = blockhash_resp.value.blockhash

    msg = MessageV0.try_compile(
        payer=keypair.pubkey(),
        instructions=[ix],
        address_lookup_table_accounts=[],
        recent_blockhash=blockhash
    )
    tx = VersionedTransaction(msg, [keypair])

    resp = client.send_transaction(tx)
    return resp.value

def main():
    print("=== SOLANA RECEIPT — MAINNET ===\n")
    
    keypair = load_or_create_wallet()
    client = Client(DEVNET_RPC)
    
    balance = get_balance(client, keypair.pubkey())
    print(f"\n💰 Wallet balance: {balance:.4f} SOL")
    
    if balance < 0.001:
        print(f"🪂 Balance too low (< 0.001 SOL). Attempting airdrop...")
        airdropped = request_airdrop(client, keypair.pubkey())
        
        if airdropped:
            balance = get_balance(client, keypair.pubkey())
        else:
            print(f"❌ No SOL for transaction. Exit.")
            return
    
    seal_hash = load_seal_hash()
    print(f"📦 Seal hash loaded: {seal_hash[:32]}...")
    
    print(f"\n🔗 Posting seal to Solana devnet...")
    try:
        sig = stamp_on_chain(keypair, seal_hash)
        print(f"\n✅ BLOCKCHAIN RECEIPT STAMPED")
        print(f"   Seal hash: {seal_hash[:32]}...")
        print(f"   TX signature: {sig}")
        print(f"   Explorer: https://explorer.solana.com/tx/{sig}?cluster=mainnet-beta")
        print(f"\n🏆 The vault survives death AND the blockchain ledger.")
    except Exception as e:
        print(f"\n❌ SOLANA TX FAILED: {e}")

if __name__ == "__main__":
    main()
