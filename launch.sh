#!/usr/bin/env bash
set -e

VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then

	echo "[*] Installing system packages..."
	sudo apt update && apt install python3.11-venv

	echo "[*] Creating virtual environment..."
	python3 -m venv "$VENV_DIR"
	source "$VENV_DIR/bin/activate"

	echo "[*] Installing dependencies..."
	pip install --upgrade pip
	pip install -r deps.txt
else
	source "$VENV_DIR/bin/activate"
fi

exec python3 IntentLimit.py "$@"
