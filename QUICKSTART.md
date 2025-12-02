# EchoOS Quick Start Guide

Get up and running with EchoOS in 5 minutes!

## 🚀 Quick Installation

```bash
# 1. Clone and enter directory
git clone https://github.com/mishal-2/EchoOS-CrossPlatform.git
cd EchoOS-CrossPlatform

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download speech model
python scripts/download_vosk_model.py

# 6. Run EchoOS
python main.py
```

## 🎤 First Time Setup

### 1. Register Your Voice

1. Click **"Register New User"**
2. Enter your name
3. Speak clearly for 5 seconds when prompted
4. Wait for confirmation

### 2. Login with Voice

1. Click **"Voice Login"**
2. Speak for 3 seconds when prompted
3. System will recognize your voice

### 3. Start Using Voice Commands

1. Click **"🎤 Start Listening"**
2. Speak commands naturally
3. System will execute and provide feedback

## 🗣️ Try These Commands

### System Control
- "shutdown" - Shut down computer
- "restart" - Restart computer
- "sleep" - Put computer to sleep
- "lock screen" - Lock your screen

### Open Applications
- "open chrome" - Open Chrome browser
- "open notepad" - Open Notepad
- "open calculator" - Open Calculator

### Web Browsing
- "open website google" - Open Google
- "search google artificial intelligence" - Search Google
- "search youtube music videos" - Search YouTube

### System Information
- "system info" - Get system information
- "battery status" - Check battery level
- "disk space" - Check disk space
- "memory usage" - Check RAM usage

### Volume Control
- "volume up" - Increase volume
- "volume down" - Decrease volume
- "mute" - Mute audio

### File Operations
- "list files" - List files in current directory
- "create file test.txt" - Create a new file
- "open file document.pdf" - Open a file

## 💡 Tips for Best Results

### Voice Recognition
- **Speak clearly** at normal pace
- **Reduce background noise** for better accuracy
- **Use natural language** - no need to be robotic
- **Wait for feedback** before next command

### Microphone Setup
- Position microphone 6-12 inches from mouth
- Use a quality microphone for better results
- Check microphone levels in system settings
- Test with "Start Listening" before important use

### Command Structure
- Start with action verb: "open", "search", "close"
- Be specific: "open chrome" not just "chrome"
- For searches: "search google [your query]"
- For websites: "open website [domain name]"

## 🔧 Common Issues

### "Model not loaded"
```bash
python scripts/download_vosk_model.py
```

### "Microphone not detected"
- Check system microphone permissions
- Ensure microphone is set as default input
- Test microphone in system settings

### "Authentication failed"
- Re-register in a quiet environment
- Speak naturally, not too loud or soft
- Maintain consistent distance from microphone

### Commands not recognized
- Check `config/commands.json` for available commands
- Speak clearly and at normal pace
- Try manual command input to test

## 📚 Learn More

- **Full Documentation**: See [README.md](README.md)
- **Installation Guide**: See [INSTALLATION.md](INSTALLATION.md)
- **All Commands**: Check `config/commands.json`
- **Troubleshooting**: See installation guide

## 🎯 Next Steps

1. **Explore Commands**: Try different voice commands
2. **Customize**: Edit `config/commands.json` to add your own
3. **Discover Apps**: Let system discover your installed apps
4. **Accessibility**: Enable screen reading features

## 🆘 Need Help?

- Check `echoos.log` for error details
- Review documentation in `docs/` folder
- Open an issue on GitHub
- Email: 1by22is076@bmsit.in

---

**Happy voice controlling! 🎙️**
