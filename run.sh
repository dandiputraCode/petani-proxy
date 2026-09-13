#!/usr/bin/env bash
set -e

# Change directory to script location
cd "$(dirname "$0")"

echo "========================================================"
echo " 🚀 Starting OmniProxy Harvester...                     "
echo "========================================================"

if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "[ERROR] Python 3 tidak ditemukan di sistem Anda!"
    exit 1
fi

PYTHON_CMD="python3"
if ! command -v python3 &>/dev/null; then
    PYTHON_CMD="python"
fi

# Run Harvester Interactive Menu
$PYTHON_CMD main.py
