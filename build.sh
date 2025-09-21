#!/bin/bash
# ============================
# Build Script for Linux
# ============================

SCRIPT_NAME="app.py"
ICON_FILE="icon.ico"

echo
echo "[*] Creating Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

echo
echo "[*] Upgrading pip..."
python3 -m pip install --upgrade pip

echo
echo "[*] Installing Dependencies..."
pip install pyinstaller edge-tts pygame SpeechRecognition pyaudio

echo
echo "[*] Building Linux Binary..."
pyinstaller --noconfirm --onefile --windowed \
  --icon=$ICON_FILE \
  $SCRIPT_NAME

echo
echo "[*] Linux Build Finished!"
echo "Your binary is located in the dist/ folder."
