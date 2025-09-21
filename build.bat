@echo off
REM ============================
REM Build Script for Windows
REM ============================

set SCRIPT_NAME=app.py
set ICON_FILE=icon.ico

echo.
echo [*] Creating Virtual Environment...
python -m venv venv
call venv\Scripts\activate

echo.
echo [*] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [*] Installing Dependencies...
pip install pyinstaller edge-tts pygame SpeechRecognition pyaudio

echo.
echo [*] Building Windows EXE...
pyinstaller --noconfirm --onefile --windowed ^
  --icon=%ICON_FILE% ^
  %SCRIPT_NAME%

echo.
echo [*] Windows Build Finished!
echo Your EXE is located in the "dist" folder.
pause
