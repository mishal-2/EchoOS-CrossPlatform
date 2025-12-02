# EchoOS Installation Guide

Complete installation instructions for Windows and macOS.

## Prerequisites

### System Requirements

- **Operating System**: Windows 10/11 or macOS 10.15+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 500MB free space
- **Microphone**: Required for voice input

### Check Python Version

```bash
python --version
# or
python3 --version
```

If Python is not installed, download from [python.org](https://www.python.org/downloads/)

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/mishal-2/EchoOS-CrossPlatform.git
cd EchoOS-CrossPlatform
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This may take 5-10 minutes depending on your internet speed.

### 4. Download Vosk Model

```bash
python scripts/download_vosk_model.py
```

This downloads the ~40MB speech recognition model.

### 5. Platform-Specific Setup

#### Windows

**Install PyAudio** (if not installed automatically):
```bash
pip install pipwin
pipwin install pyaudio
```

**Optional - For volume control:**
- Download [NirCmd](https://www.nirsoft.net/utils/nircmd.html)
- Extract to `C:\Windows\System32\` or add to PATH

#### macOS

**Install PortAudio** (required for PyAudio):
```bash
brew install portaudio
pip install pyaudio
```

**Grant Microphone Permission:**
1. System Preferences → Security & Privacy → Privacy
2. Select "Microphone"
3. Check the box for Terminal/Python

### 6. Verify Installation

```bash
python main.py
```

If the GUI opens, installation is successful!

## Troubleshooting

### PyAudio Installation Issues

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### Vosk Model Not Found

If you see "Vosk model not found":
```bash
python scripts/download_vosk_model.py
```

Ensure the model is in: `models/vosk-model-small-en-us-0.15/`

### Microphone Not Detected

**Windows:**
1. Settings → Privacy → Microphone
2. Enable microphone access for apps

**macOS:**
1. System Preferences → Security & Privacy → Microphone
2. Grant permission to Terminal/Python

### Import Errors

If you get import errors:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Permission Errors (macOS)

Some system commands require sudo:
```bash
# For shutdown/restart commands
sudo python main.py
```

## Optional Features

### Full Accessibility Features

For screen reading and automation:
```bash
pip install pyautogui opencv-python pytesseract Pillow
```

**macOS additional:**
```bash
brew install tesseract
```

**Windows additional:**
- Download [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- Add to PATH

### Development Tools

For development and testing:
```bash
pip install pytest pytest-cov black flake8
```

## Updating

To update to the latest version:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove project directory
cd ..
rm -rf EchoOS-CrossPlatform  # macOS/Linux
# or
rmdir /s EchoOS-CrossPlatform  # Windows
```

## Next Steps

After installation:
1. Run `python main.py`
2. Register a new user with voice sample
3. Authenticate using voice
4. Start giving voice commands!

See [USER_MANUAL.md](USER_MANUAL.md) for usage instructions.

## Support

If you encounter issues:
1. Check [Troubleshooting](#troubleshooting) section
2. Review `echoos.log` for error details
3. Open an issue on GitHub with:
   - Operating system and version
   - Python version
   - Error message
   - Log file contents

## System-Specific Notes

### Windows 11

- Windows Defender may flag the app - add exception if needed
- UAC prompts may appear for system commands

### macOS Monterey/Ventura

- Gatekeeper may block unsigned apps
- Grant all required permissions in System Preferences

### Linux

- Tested on Ubuntu 20.04+ and Fedora 35+
- May require additional audio libraries
