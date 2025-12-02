# 🎙️ EchoOS - Cross-Platform Voice-Controlled Operating System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey)](https://github.com/mishal-2/EchoOS-CrossPlatform)

**EchoOS** is a secure, privacy-first, offline voice-controlled operating system interface with integrated voice biometric authentication. Control your computer entirely through voice commands without internet dependency.

## ✨ Key Features

- 🔒 **Voice Biometric Authentication** - Secure user identification using Resemblyzer
- 🎤 **Offline Speech Recognition** - Powered by Vosk (no internet required)
- 🖥️ **Cross-Platform** - Works on Windows and macOS
- 🗣️ **Text-to-Speech Feedback** - Real-time voice responses
- 🚀 **40+ Voice Commands** - Comprehensive OS control
- 🔐 **Session Management** - Secure multi-user access with encryption
- ♿ **Accessibility Features** - Screen reading and navigation
- 🎨 **Modern GUI** - Built with PySide6

## 📊 Performance Metrics

- **Authentication Accuracy**: 92% TAR (4% FAR)
- **Speech Recognition**: 9.85% WER
- **Command Success Rate**: 93%
- **Response Latency**: 150ms average
- **Memory Footprint**: 315MB

## 🎯 Supported Commands

### System Control
- `shutdown` / `restart` / `sleep` / `lock screen`
- `volume up` / `volume down` / `mute`
- `brightness up` / `brightness down`

### Application Management
- `open [app name]` - Launch applications
- `close [app name]` - Close applications
- `minimize` / `maximize` / `switch window`

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

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Microphone
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/mishal-2/EchoOS-CrossPlatform.git
cd EchoOS-CrossPlatform
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download Vosk model**
```bash
python scripts/download_vosk_model.py
```

5. **Run EchoOS**
```bash
python main.py
```

## 📖 First Time Setup

1. **Launch EchoOS** - Run `python main.py`
2. **Register User** - Click "Register New User"
3. **Record Voice Sample** - Speak clearly for 5-10 seconds
4. **Authenticate** - Use voice authentication to login
5. **Start Using** - Begin giving voice commands!

## 🏗️ Architecture

```
EchoOS/
├── main.py                 # Application entry point
├── config/                 # Configuration files
│   ├── commands.json      # Command mappings
│   ├── apps.json          # Discovered applications
│   └── settings.json      # User preferences
├── modules/
│   ├── auth.py            # Voice authentication (Resemblyzer)
│   ├── stt.py             # Speech-to-text (Vosk)
│   ├── tts.py             # Text-to-speech (pyttsx3)
│   ├── parser.py          # Command parsing
│   ├── executor.py        # Command execution
│   ├── app_discovery.py   # Application discovery
│   ├── accessibility.py   # Accessibility features
│   └── ui.py              # GUI interface (PySide6)
├── models/                # Voice models and data
├── scripts/               # Utility scripts
└── tests/                 # Unit tests
```

## 🔧 Configuration

### Custom Commands

Edit `config/commands.json` to add custom voice commands:

```json
{
  "open": ["open", "launch", "start"],
  "close": ["close", "exit", "quit"],
  "custom_command": ["my custom phrase"]
}
```

### Application Discovery

EchoOS automatically discovers installed applications. To manually add apps:

```json
{
  "apps": [
    {
      "name": "MyApp",
      "path": "/path/to/app",
      "aliases": ["my app", "myapp"]
    }
  ]
}
```

## 🛡️ Security Features

- **Voice Biometric Authentication** - Unique voice signatures
- **Session Encryption** - Fernet encryption for session data
- **Session Timeout** - 30-minute automatic logout
- **Offline Processing** - No data sent to cloud
- **Local Storage** - All data stored locally

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_auth.py

# Run with coverage
python -m pytest --cov=modules tests/
```

## 📝 Development

### Adding New Commands

1. Add command pattern to `config/commands.json`
2. Implement handler in `modules/executor.py`
3. Add tests in `tests/test_executor.py`
4. Update documentation

### Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 🐛 Troubleshooting

### Microphone Not Detected
- Check microphone permissions in system settings
- Verify microphone is set as default input device

### Voice Recognition Issues
- Speak clearly and at normal pace
- Reduce background noise
- Check microphone volume levels

### Authentication Failures
- Re-register voice sample in quiet environment
- Ensure consistent microphone distance
- Speak naturally during authentication

### Application Not Opening
- Run app discovery: `python scripts/discover_apps.py`
- Check application path in `config/apps.json`
- Verify application is installed

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [User Manual](docs/USER_MANUAL.md)
- [API Documentation](docs/API.md)
- [Development Guide](docs/DEVELOPMENT.md)

## 🔮 Future Enhancements

- [ ] Natural Language Understanding (NLU)
- [ ] Multi-language support
- [ ] Continuous authentication
- [ ] Mobile deployment (iOS/Android)
- [ ] Plugin system for extensions
- [ ] Cloud sync (optional)
- [ ] Voice command macros
- [ ] Advanced accessibility features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

**M A Mohammed Mishal** - *Initial work* - [Mishal2004](https://github.com/Mishal2004)

## 🙏 Acknowledgments

- **Vosk** - Offline speech recognition
- **Resemblyzer** - Voice biometric authentication
- **PySide6** - Modern GUI framework
- **pyttsx3** - Text-to-speech engine

## 📧 Contact

For questions or support:
- Email: 1by22is076@bmsit.in
- GitHub: [@Mishal2004](https://github.com/Mishal2004)

## ⭐ Star History

If you find EchoOS useful, please consider giving it a star!

---

**Built with ❤️ for accessibility, privacy, and hands-free computing**
