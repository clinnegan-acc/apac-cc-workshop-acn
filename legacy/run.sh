#!/bin/bash
# FactorySoft IMS - Startup Script
# Usage:
#   ./run.sh          - Launch terminal UI
#   ./run.sh --api    - Launch Flask API server

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "First run - setting up environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

if [ "$1" = "--api" ]; then
    echo "Starting Flask API on port 8001..."
    python app.py
else
    python terminal_ui.py
fi
