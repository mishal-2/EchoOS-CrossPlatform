# Getting Started with EchoOS

Welcome to EchoOS! This guide will help you get up and running in just a few minutes.

## 📋 What You'll Need

Before starting, make sure you have:

- ✅ A computer running Windows, macOS, or Linux
- ✅ Python 3.8 or newer installed
- ✅ A working microphone
- ✅ At least 500MB of free disk space
- ✅ Internet connection (only for initial setup)

## 🚀 Installation Steps

### Step 1: Install Python (if not already installed)

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH"
4. Click "Install Now"

#### macOS
```bash
# Using Homebrew (recommended)
brew install python@3.10

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 2: Download EchoOS

#### Option A: Using Git (Recommended)
```bash
git clone https://github.com/Mishal-Projects/EchoOS-CrossPlatform.git
cd EchoOS-CrossPlatform
```

#### Option B: Download ZIP
1. Go to [GitHub Repository](https://github.com/Mishal-Projects/EchoOS-CrossPlatform)
2. Click green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file
5. Open terminal/command prompt in extracted folder

### Step 3: Create Virtual Environment

This keeps EchoOS dependencies separate from your system Python.

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the start of your command prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will take a few minutes. Grab a coffee! ☕

### Step 5: Run EchoOS

```bash
python run.py
```

The launcher will:
1. ✅ Check Python version
2. ✅ Verify all dependencies
3. ✅ Download voice recognition model (first time only)
4. ✅ Setup configuration files
5. ✅ Test your microphone
6. ✅ Launch EchoOS

## 🎤 First Time Use

### 1. Register Your Voice

When EchoOS opens:

1. Click **"Register New User"** button
2. Enter your username (e.g., "john_doe")
3. Click **"Start Recording"**
4. Speak clearly for 5-10 seconds:
   - Say your name
   - Count from 1 to 10
   - Speak naturally
5. Click **"Stop Recording"**
6. Wait for confirmation

**Tips for Better Registration:**
- Find a quiet room
- Speak at normal volume
- Keep microphone 6-12 inches away
- Don't whisper or shout

### 2. Authenticate

1. Click **"Authenticate"** button
2. Speak when prompted (3-5 seconds)
3. Wait for green indicator (authenticated!)

### 3. Start Using Voice Commands

Once authenticated, try these commands:

**System Commands:**
- "system info" - Show system information
- "battery status" - Check battery level
- "volume up" - Increase volume

**Application Commands:**
- "open chrome" - Launch Chrome browser
- "open notepad" - Open Notepad
- "close chrome" - Close Chrome

**Web Commands:**
- "search google python tutorials"
- "open website github.com"

## 🎯 Common Voice Commands

### System Control
```
"shutdown"          - Power off computer
"restart"           - Restart computer
"sleep"             - Put computer to sleep
"lock screen"       - Lock the screen
```

### Volume Control
```
"volume up"         - Increase volume
"volume down"       - Decrease volume
"mute"              - Mute audio
```

### Application Management
```
"open [app name]"   - Launch application
"close [app name]"  - Close application
"minimize"          - Minimize window
"maximize"          - Maximize window
```

### File Operations
```
"list files"        - Show files in directory
"open file [name]"  - Open specific file
"create file [name]"- Create new file
```

### System Information
```
"system info"       - Show system details
"battery status"    - Check battery
"disk space"        - Show storage info
"memory usage"      - Show RAM usage
"cpu usage"         - Show CPU usage
"network status"    - Show network info
```

### Web Operations
```
"open website [url]"        - Open website
"search google [query]"     - Google search
"search youtube [query]"    - YouTube search
```

## 🔧 Troubleshooting

### Problem: "Python not found"

**Solution:**
- Windows: Reinstall Python with "Add to PATH" checked
- macOS/Linux: Use `python3` instead of `python`

### Problem: "Microphone not detected"

**Solution:**
1. Check microphone is plugged in
2. Test microphone:
   ```bash
   python scripts/test_microphone.py
   ```
3. Check system microphone permissions
4. Set microphone as default input device

### Problem: "Voice not recognized"

**Solution:**
- Speak clearly and at normal pace
- Reduce background noise
- Check microphone volume (not too low/high)
- Try re-registering your voice profile

### Problem: "Application not opening"

**Solution:**
1. Run app discovery:
   ```bash
   python scripts/discover_apps.py
   ```
2. Check application is installed
3. Try full application name

### Problem: "Module not found" error

**Solution:**
```bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

## 📱 Using EchoOS

### Main Window

The EchoOS window has:

1. **Status Indicator**
   - 🟢 Green: Ready and listening
   - 🔴 Red: Not listening
   - 🟡 Yellow: Processing

2. **Activity Log**
   - Shows all recognized commands
   - Displays system responses
   - Scrolls automatically

3. **Control Buttons**
   - Start/Stop Listening
   - Register New User
   - Authenticate
   - Logout

4. **Manual Input**
   - Type commands manually
   - Useful for testing
   - Same as voice commands

### Tips for Best Results

1. **Speak Clearly**
   - Normal speaking pace
   - Don't rush or speak too slowly
   - Enunciate words properly

2. **Quiet Environment**
   - Minimize background noise
   - Close windows
   - Turn off fans/AC if possible

3. **Consistent Distance**
   - Keep same distance from microphone
   - 6-12 inches is ideal
   - Don't move around while speaking

4. **Natural Speech**
   - Speak as you normally would
   - Don't whisper or shout
   - Use natural intonation

## 🎓 Learning More

### Documentation

- **[User Manual](docs/USER_MANUAL.md)** - Complete feature guide
- **[API Documentation](docs/API.md)** - For developers
- **[Development Guide](docs/DEVELOPMENT.md)** - Contributing guide

### Video Tutorials (Coming Soon)

- Basic Setup and Installation
- Voice Registration Best Practices
- Advanced Voice Commands
- Customizing EchoOS

### Community

- GitHub Issues: Report bugs or request features
- Discussions: Ask questions and share tips

## 🔄 Updating EchoOS

To get the latest version:

```bash
# Navigate to EchoOS directory
cd EchoOS-CrossPlatform

# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run EchoOS
python run.py
```

## 🛑 Stopping EchoOS

To exit EchoOS:

1. Say "stop listening" or click Stop button
2. Close the window
3. Or press `Ctrl+Q`

To deactivate virtual environment:
```bash
deactivate
```

## 📊 Quick Reference Card

Print this for easy reference:

```
┌─────────────────────────────────────────┐
│         EchoOS Quick Reference          │
├─────────────────────────────────────────┤
│ SYSTEM                                  │
│  • shutdown / restart / sleep / lock    │
│                                         │
│ VOLUME                                  │
│  • volume up / volume down / mute       │
│                                         │
│ APPS                                    │
│  • open [app] / close [app]             │
│                                         │
│ FILES                                   │
│  • list files / open file [name]        │
│                                         │
│ WEB                                     │
│  • open website [url]                   │
│  • search google [query]                │
│                                         │
│ INFO                                    │
│  • system info / battery / disk space   │
│                                         │
│ CONTROL                                 │
│  • stop listening / wake up             │
└─────────────────────────────────────────┘
```

## 🎉 You're Ready!

Congratulations! You're now ready to use EchoOS. Start with simple commands and gradually explore more features.

**First Commands to Try:**
1. "system info"
2. "battery status"
3. "open chrome"
4. "volume up"
5. "search google hello world"

Enjoy controlling your computer with your voice! 🎙️

---

**Need Help?**
- Check [User Manual](docs/USER_MANUAL.md)
- Review [Troubleshooting](#troubleshooting)
- Open [GitHub Issue](https://github.com/Mishal-Projects/EchoOS-CrossPlatform/issues)

**Happy Voice Computing!** 🚀
