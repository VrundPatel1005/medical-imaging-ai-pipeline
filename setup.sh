#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "Creating Python virtual environment..."
python3 -m venv .venv

echo "Activating environment and installing dependencies..."
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

mkdir -p data/raw data/processed data/outputs screenshots models

echo ""
echo "Setup complete."
echo ""
echo "Next commands:"
echo "  source .venv/bin/activate"
echo "  python scripts/load_scan.py --help"
echo "  streamlit run scripts/streamlit_app.py"
echo ""
echo "Download a public dataset into data/raw/ when you are ready."

