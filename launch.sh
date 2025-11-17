#!/usr/bin/env bash
set -e
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
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
fi

BASHRC="$HOME/.bashrc"
[ -f "$BASHRC" ] || touch "$BASHRC"

if ! grep -q "alias intentlimit=" "$BASHRC"; then
	echo "[*] Adding IntentLimit alias to $BASHRC..."
	{
		echo ""
		echo "# IntentLimit Alias"
		echo "alias intentlimit='( source \"$SCRIPT_DIR/venv/bin/activate\" && python3 \"$SCRIPT_DIR/IntentLimit.py\" )'"
	} >> "$BASHRC"
else
	echo "[*] IntentLimit alias found..."
fi

echo "[*] Alias created. Run source ~/.bashrc to load it."
read -p "[+] IntentLimit installed. Press enter to continue..."
exec python3 IntentLimit.py "$@"
