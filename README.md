# Realtime Dictation + TTS

A Python app for real-time speech recognition and text-to-speech (TTS) with voice, speed, and volume controls. Speak into your microphone and hear your text read aloud instantly.

## Features

* Real-time speech-to-text dictation.
* Text-to-speech playback with voice selection, speed, and volume controls.
* Pause, resume, and stop playback controls.
* Works with multiple English voices (US, GB, IN).
* Cross-platform (Windows, Linux, macOS).
* Uses `edge-tts` for high-quality neural TTS.
* **Optional Build Scripts** to generate standalone executables on Windows and Linux.

---

## Installation

1. **Clone or download the project**

```bash
git clone https://github.com/A56-A5/TTS
cd TTS
```

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Running the App

```bash
python app.py
```

* Use the text box to type text.
* Press **🎤 Speak** to dictate via microphone.
* Press **🗣️ Speak Text** to read text aloud.
* Use pause/resume/stop buttons for playback control.
* Adjust speed, volume, and voice in settings.

---

## Building Executables

Standalone executables can be built for Windows and Linux using the included build scripts.
This allows you to distribute the app without requiring Python.

### 🔧 Windows Build

1. Ensure Python 3.11+ is installed and added to PATH.
2. Place an icon file named `icon.ico` in the project folder.
3. Double-click `build.bat` or run it in a terminal:

```bat
build.bat
```

The Windows executable will be located in the `dist/` folder as `app.exe`.

---

### 🐧 Linux Build

1. Ensure Python 3.11+ and `python3-venv` are installed.
2. Make the build script executable:

```bash
chmod +x build.sh
```

3. Run the script:

```bash
./build.sh
```

The Linux binary will be generated in `dist/app`.

---

## Build Script Overview

**build.bat (Windows)**

* Creates a virtual environment
* Installs dependencies
* Uses PyInstaller to build `app.exe` with a custom icon

**build.sh (Linux)**

* Same process as Windows, but produces a native Linux binary

---

## Requirements

* Python 3.11+
* Internet connection for TTS
* Microphone access

---

## Dependencies (`requirements.txt`)

```text
pygame>=2.5.2
edge-tts>=0.3.2
SpeechRecognition>=3.9.0
PyAudio>=0.2.13
pyinstaller>=6.0.0
```

---

## Usage Notes

* Say **"stop recording"** to end dictation.
* Volume slider controls playback volume (0–200%).
* Speed slider changes TTS speed (-50% to +50%).
* Ensure microphone is accessible and working.
* Executables built with PyInstaller will run without needing Python installed.

---

## License

MIT License – free to use and modify.
