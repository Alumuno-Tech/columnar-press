#!/bin/bash
# RUMUNO VAULT — judge demo. Press, Seal, Chain, Recall.
set -e

echo "=== RUMUNO DEMO — press, seal, kill, recall ==="

# Use the centralized venv
source ~/.venvs/columnar-vault/bin/activate

# Run the Vulture Protocol test
python3 assassin.py

echo ""
echo "=== Vault survived. Verify the receipt yourself: ==="
echo "https://explorer.solana.com/tx/547cRfHaieS5q7B3W2nKFS1eAhNSBkMD8AWTUZBeHsPy7J6LctdFaoBTtYVXBAMyehyfoYKdi7Kt3MF5UsE2ZiEa?cluster=mainnet-beta"

deactivate
