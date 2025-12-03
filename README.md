# 🎙️ EchoOS - Cross-Platform Voice-Controlled Operating System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](https://github.com/Mishal-Projects/EchoOS-CrossPlatform)
[![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)](https://github.com/Mishal-Projects/EchoOS-CrossPlatform)
[![Enhanced](https://img.shields.io/badge/UI-Dark%20Mode%20%2B%20Waveform-purple)](https://github.com/Mishal-Projects/EchoOS-CrossPlatform)

**EchoOS** is a secure, privacy-first, offline voice-controlled operating system interface with integrated voice biometric authentication. Control your computer entirely through voice commands without internet dependency.

> 🎉 **Project Status**: **PRODUCTION READY** with **Enhanced UI** featuring Dark Mode & Animated Waveform!

## ✨ New: Enhanced Version Available!

### 🌙 Dark Mode + 📊 Animated Waveform

**EchoOS Enhanced** now includes:
- **Dark Mode Theme** - Eye-friendly design for extended use
- **Animated Waveform** - Real-time audio visualization
- **Modern UI** - Professional design with smooth animations
- **Theme Toggle** - Switch between dark and light modes instantly

**Quick Start Enhanced:**
```bash
python main_enhanced.py  # New enhanced version
python main.py           # Original version
```

See [ENHANCED_FEATURES.md](ENHANCED_FEATURES.md) for details!

## 🎯 Key Features

- 🔒 **Voice Biometric Authentication** - Secure user identification using Resemblyzer
- 🎤 **Offline Speech Recognition** - Powered by Vosk (no internet required)
- 🖥️ **Cross-Platform** - Works on Windows, macOS, and Linux
- 🗣️ **Text-to-Speech Feedback** - Real-time voice responses
- 🚀 **40+ Voice Commands** - Comprehensive OS control
- 🔐 **Session Management** - Secure multi-user access with encryption
- ♿ **Accessibility Features** - Screen reading and navigation
- 🎨 **Modern GUI** - Built with PySide6
- 🌙 **Dark Mode** - Eye-friendly theme (Enhanced version)
- 📊 **Waveform Visualization** - Real-time audio feedback (Enhanced version)

## 📊 Performance Metrics

- **Authentication Accuracy**: 92% TAR (4% FAR)
- **Speech Recognition**: 9.85% WER
- **Command Success Rate**: 93%
- **Response Latency**: 150ms average
- **Memory Footprint**: 315MB
- **Animation**: 20 FPS smooth waveform

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Microphone
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

### Installation (3 Simple Steps)

1. **Clone the repository**
```bash
git clone https://github.com/Mishal-Projects/EchoOS-CrossPlatform.git
cd EchoOS-CrossPlatform
```

2. **Create virtual environment and install**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

3. **Setup and run**
```bash
# Using the smart launcher (recommended)
python run.py

# Or run enhanced version directly
python main_enhanced.py

# Or standard version
python main.py
```

## 🎨 Choose Your Version

### Enhanced Version (Recommended)
```bash
python main_enhanced.py
```
**Features:**
- ✅ Dark mode theme
- ✅ Animated waveform
- ✅ Modern design
- ✅ Theme toggle
- ✅ Enhanced visual feedback

### Standard Version
```bash
python main.py
```
**Features:**
- ✅ Light theme
- ✅ Basic UI
- ✅ Faster startup
- ✅ Lower resource usage

## 🎯 Supported Commands

### System Control
- `shutdown` / `restart` / `sleep` / `lock screen`
- `volume up` / `volume down` / `mute`

### Application Management
- `open [app name]` - Launch applications
- `close [app name]` - Close applications
- `minimize` / `maximize`

### File Operations
- `open file [filename]`
- `create file [filename]`
- `delete file [filename]`
- `list files`

### Web Operations
- `open website [url]`
- `search google [query]`
- `search youtube [query]`

### System Information
- `system info` / `battery status`
- `disk space` / `memory usage`
- `network status` / `cpu usage`

### Accessibility
- `read screen` / `navigate` / `click`
- `scroll up` / `scroll down` / `zoom in` / `zoom out`

## 📖 Documentation

- **[Enhanced Features Guide](ENHANCED_FEATURES.md)** - Dark mode & waveform details
- **[Enhanced Quick Start](ENHANCED_QUICKSTART.md)** - Get started with enhanced version
- **[User Manual](docs/USER_MANUAL.md)** - Complete guide for end users
- **[API Documentation](docs/API.md)** - Detailed API reference
- **[Development Guide](docs/DEVELOPMENT.md)** - For contributors
- **[Installation Guide](INSTALLATION.md)** - Detailed setup instructions
- **[Quick Start Guide](QUICKSTART.md)** - 5-minute getting started
- **[Getting Started](GETTING_STARTED.md)** - Beginner-friendly guide

## 🎨 Enhanced UI Preview

### Dark Mode with Waveform
```
┌─────────────────────────────────────────┐
│  🎙️ EchoOS          [☀️ Light Mode]    │
│  Voice-Controlled Operating System      │
├─────────────────────────────────────────┤
│           🎤 Listening...               │
├─────────────────────────────────────────┤
│  Audio Visualization                    │
│  ╔═══════════════════════════════════╗  │
│  ║  ～～～～～～～～～～～～～～～～～  ║  │
│  ║ ～～～～～～～～～～～～～～～～～～ ║  │
│  ╚═══════════════════════════════════╝  │
├─────────────────────────────────────────┤
│  🔐 Authentication                      │
│  ✅ Logged in as: john_doe              │
└─────────────────────────────────────────┘
```

## 🏗️ Project Structure

```
EchoOS-CrossPlatform/
├── main.py                 # Standard version entry point
├── main_enhanced.py        # Enhanced version entry point
├── run.py                  # Smart launcher with checks
├── modules/
│   ├── ui.py              # Standard UI
│   ├── ui_enhanced.py     # Enhanced UI (Dark mode + Waveform)
│   ├── auth.py            # Voice authentication
│   ├── stt.py             # Speech-to-text
│   ├── tts.py             # Text-to-speech
│   ├── parser.py          # Command parsing
│   ├── executor.py        # Command execution
│   └── ...
├── docs/                  # Documentation
├── tests/                 # Unit tests
└── scripts/               # Utility scripts
```

## 🔧 Development

### Using Makefile

```bash
make help           # Show all commands
make install        # Install dependencies
make setup          # Run first-time setup
make test           # Run tests with coverage
make run            # Launch standard version
make run-enhanced   # Launch enhanced version
make clean          # Clean temporary files
```

## 🛡️ Security Features

- **Voice Biometric Authentication** - Unique voice signatures
- **Session Encryption** - Fernet encryption for session data
- **Session Timeout** - 30-minute automatic logout
- **Offline Processing** - No data sent to cloud
- **Local Storage** - All data stored locally

## 🐛 Troubleshooting

### Quick Diagnostics

```bash
# Test microphone
python scripts/test_microphone.py

# Discover applications
python scripts/discover_apps.py

# Setup configuration
python scripts/setup_config.py
```

### Common Issues

- **Waveform Not Animating**: Check microphone permissions and click "Start Listening"
- **Dark Mode Too Dark**: Click "☀️ Light Mode" button to switch themes
- **Microphone Not Detected**: Check permissions and default device
- **Voice Not Recognized**: Reduce background noise, speak clearly
- **Authentication Fails**: Re-register in quiet environment

See [User Manual](docs/USER_MANUAL.md) for detailed troubleshooting.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 🔮 Future Enhancements

- [ ] Natural Language Understanding (NLU)
- [ ] Multi-language support (Spanish, French, German)
- [ ] Continuous authentication
- [ ] Mobile deployment (iOS/Android)
- [ ] Plugin system for extensions
- [ ] Multiple color themes (Nord, Dracula, etc.)
- [ ] Spectrum analyzer view
- [ ] Custom waveform colors

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Author

**M A Mohammed Mishal**
- GitHub: [@Mishal-Projects](https://github.com/Mishal-Projects)

## 🙏 Acknowledgments

- **Vosk** - Offline speech recognition
- **Resemblyzer** - Voice biometric authentication
- **PySide6** - Modern GUI framework
- **pyttsx3** - Text-to-speech synthesis

## 📊 Project Stats

- **Total Files**: 40+
- **Lines of Code**: 5,000+
- **Test Coverage**: Comprehensive
- **Documentation**: 10+ detailed guides
- **Supported Commands**: 40+
- **Platforms**: 3 (Windows, macOS, Linux)
- **UI Versions**: 2 (Standard + Enhanced)

## 🎉 Project Status

✅ **Core Features**: Complete  
✅ **Testing Suite**: Complete  
✅ **Documentation**: Complete  
✅ **CI/CD Pipeline**: Complete  
✅ **Cross-Platform**: Complete  
✅ **Enhanced UI**: Complete  
✅ **Production Ready**: Yes  

---

**Ready to control your computer with your voice?**

### Standard Version
```bash
git clone https://github.com/Mishal-Projects/EchoOS-CrossPlatform.git
cd EchoOS-CrossPlatform
python main.py
```

### Enhanced Version (Dark Mode + Waveform)
```bash
git clone https://github.com/Mishal-Projects/EchoOS-CrossPlatform.git
cd EchoOS-CrossPlatform
python main_enhanced.py
```

For detailed instructions:
- **Enhanced Version**: See [ENHANCED_QUICKSTART.md](ENHANCED_QUICKSTART.md)
- **Standard Version**: See [QUICKSTART.md](QUICKSTART.md)
- **Full Setup**: See [INSTALLATION.md](INSTALLATION.md)

---

⭐ **Star this repo if you find it useful!**

🌙 **Try the new Enhanced version with Dark Mode!**
