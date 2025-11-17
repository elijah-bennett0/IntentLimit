#!/usr/bin/env bash
set -e

VENV_DIR="venv"

if [ ! -d "$VENV_DIR" ]; then

	echo "[*] Installing system packages..."
	sudo apt update && sudo apt install python3-venv

	echo "[*] Creating virtual environment..."
	python3 -m venv "$VENV_DIR"
	source "$VENV_DIR/bin/activate"

	echo "[*] Installing dependencies..."
	pip install --upgrade pip
	pip install -r deps.txt
else
	source "$VENV_DIR/bin/activate"
fi

shopt -s expand_aliases
alias intentlimit='exec python3 IntentLimit.py "$@"'


read -p "[+] IntentLimit installed. Run with command `intentlimit`. Press enter to continue..."
intentlimit
