# EchoOS User Manual

## Table of Contents

1. [Getting Started](#getting-started)
2. [User Registration](#user-registration)
3. [Authentication](#authentication)
4. [Voice Commands](#voice-commands)
5. [Application Control](#application-control)
6. [File Management](#file-management)
7. [System Information](#system-information)
8. [Accessibility Features](#accessibility-features)
9. [Troubleshooting](#troubleshooting)

## Getting Started

### First Launch

1. **Start EchoOS**
   ```bash
   python main.py
   ```

2. **Main Window**
   - Status indicator (green = ready, red = not listening)
   - Activity log showing all actions
   - Manual command input field
   - Control buttons (Start/Stop listening)

### System Requirements

- **Microphone**: Required for voice input
- **Speakers**: Recommended for voice feedback
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB free space

## User Registration

### Creating Your Voice Profile

1. Click **"Register New User"** button
2. Enter your username
3. Click **"Start Recording"**
4. Speak clearly for 5-10 seconds:
   - Say your name
   - Count from 1 to 10
   - Speak naturally at normal pace
5. Click **"Stop Recording"**
6. System will create your voice profile

### Tips for Better Registration

- **Quiet Environment**: Minimize background noise
- **Consistent Distance**: Keep 6-12 inches from microphone
- **Natural Speech**: Speak normally, don't shout
- **Sufficient Duration**: Record for at least 5 seconds

## Authentication

### Voice Login

1. Click **"Authenticate"** button
2. Speak when prompted (3-5 seconds)
3. System compares your voice to stored profile
4. Green indicator = authenticated
5. Red indicator = authentication failed

### Session Management

- **Session Duration**: 30 minutes
- **Auto-Logout**: After timeout period
- **Manual Logout**: Click "Logout" button
- **Re-authentication**: Required after logout

### Security Features

- Voice biometric matching (92% accuracy)
- Encrypted session storage
- Automatic session cleanup
- Multi-user support

## Voice Commands

### System Control

| Command | Action |
|---------|--------|
| "shutdown" | Powers off computer |
| "restart" | Restarts computer |
| "sleep" | Puts computer to sleep |
| "lock screen" | Locks the screen |

### Volume Control

| Command | Action |
|---------|--------|
| "volume up" | Increases volume |
| "volume down" | Decreases volume |
| "mute" | Mutes audio |

### Control Commands

| Command | Action |
|---------|--------|
| "stop listening" | Pauses voice recognition |
| "wake up" | Resumes voice recognition |
| "hello echo" | Activates system |

## Application Control

### Opening Applications

**Syntax**: `"open [application name]"`

**Examples**:
- "open chrome"
- "open notepad"
- "launch calculator"
- "start firefox"

### Closing Applications

**Syntax**: `"close [application name]"`

**Examples**:
- "close chrome"
- "exit notepad"
- "quit calculator"

### Window Management

| Command | Action |
|---------|--------|
| "minimize" | Minimizes active window |
| "maximize" | Maximizes active window |
| "full screen" | Enters full screen mode |

### Supported Applications

EchoOS automatically discovers installed applications. Common apps:
- Web browsers (Chrome, Firefox, Edge)
- Text editors (Notepad, TextEdit)
- System utilities (Calculator, Terminal)
- Office applications (Word, Excel, PowerPoint)

## File Management

### Opening Files

**Syntax**: `"open file [filename]"`

**Examples**:
- "open file document.txt"
- "show file report.pdf"

### Creating Files

**Syntax**: `"create file [filename]"`

**Examples**:
- "create file notes.txt"
- "new file todo.md"
- "make file data.csv"

### Deleting Files

**Syntax**: `"delete file [filename]"`

**Examples**:
- "delete file old.txt"
- "remove file temp.log"

### Listing Files

**Command**: `"list files"`

Shows files in current directory with:
- File names
- File sizes
- File types

## System Information

### System Overview

**Command**: `"system info"`

Displays:
- Operating system
- Processor
- RAM
- Python version

### Battery Status

**Command**: `"battery status"`

Shows:
- Battery percentage
- Charging status
- Time remaining

### Disk Space

**Command**: `"disk space"`

Displays:
- Total disk space
- Used space
- Free space
- Usage percentage

### Memory Usage

**Command**: `"memory usage"`

Shows:
- Total RAM
- Used RAM
- Available RAM
- Usage percentage

### CPU Usage

**Command**: `"cpu usage"`

Displays:
- Current CPU usage
- Per-core usage
- CPU frequency

### Network Status

**Command**: `"network status"`

Shows:
- Connection status
- IP address
- Network name

## Web Operations

### Opening Websites

**Syntax**: `"open website [url]"`

**Examples**:
- "open website google.com"
- "go to github.com"
- "navigate to youtube.com"

### Google Search

**Syntax**: `"search google [query]"`

**Examples**:
- "search google python tutorials"
- "google search weather forecast"

### YouTube Search

**Syntax**: `"search youtube [query]"`

**Examples**:
- "search youtube music videos"
- "youtube search cooking recipes"

## Accessibility Features

### Screen Reading

**Command**: `"read screen"`

- Captures screen content
- Extracts text using OCR
- Reads text aloud

### Navigation

**Syntax**: `"navigate [direction]"`

**Examples**:
- "navigate up"
- "navigate down"
- "navigate left"
- "navigate right"

### Clicking

**Command**: `"click"`

Performs mouse click at current position

### Scrolling

| Command | Action |
|---------|--------|
| "scroll up" | Scrolls page up |
| "scroll down" | Scrolls page down |

### Zoom

| Command | Action |
|---------|--------|
| "zoom in" | Magnifies screen |
| "zoom out" | Reduces magnification |

## Troubleshooting

### Voice Not Recognized

**Problem**: Commands not being recognized

**Solutions**:
1. Check microphone connection
2. Verify microphone permissions
3. Reduce background noise
4. Speak clearly and at normal pace
5. Check microphone volume levels

### Authentication Fails

**Problem**: Voice authentication not working

**Solutions**:
1. Re-register voice profile
2. Use same microphone as registration
3. Maintain consistent distance
4. Ensure quiet environment
5. Speak naturally (don't whisper or shout)

### Application Not Opening

**Problem**: "open [app]" command fails

**Solutions**:
1. Run app discovery: `python scripts/discover_apps.py`
2. Check application is installed
3. Verify application path in `config/apps.json`
4. Try full application name
5. Check application permissions

### Low Audio Levels

**Problem**: System can't hear you

**Solutions**:
1. Test microphone: `python scripts/test_microphone.py`
2. Increase microphone volume in system settings
3. Move closer to microphone
4. Check microphone is not muted
5. Try different microphone

### High CPU Usage

**Problem**: EchoOS using too much CPU

**Solutions**:
1. Stop continuous listening when not needed
2. Close unnecessary applications
3. Restart EchoOS
4. Check for background processes
5. Update to latest version

### Session Timeout

**Problem**: Frequent session timeouts

**Solutions**:
1. Adjust timeout in `config/settings.json`
2. Re-authenticate when needed
3. Keep EchoOS window active
4. Check system time is correct

## Best Practices

### Voice Commands

1. **Speak Clearly**: Enunciate words properly
2. **Normal Pace**: Don't rush or speak too slowly
3. **Consistent Volume**: Maintain steady voice level
4. **Quiet Environment**: Minimize background noise
5. **Natural Speech**: Speak as you normally would

### Security

1. **Unique Voice**: Register in quiet environment
2. **Regular Re-authentication**: Don't stay logged in indefinitely
3. **Logout**: When leaving computer
4. **Secure Storage**: Protect config directory
5. **Regular Updates**: Keep EchoOS updated

### Performance

1. **Close Unused Apps**: Free up system resources
2. **Regular Cleanup**: Clear old logs and sessions
3. **Update Models**: Keep Vosk model updated
4. **Monitor Resources**: Check CPU and memory usage
5. **Restart Periodically**: Refresh system state

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+L` | Start/Stop listening |
| `Ctrl+R` | Register new user |
| `Ctrl+A` | Authenticate |
| `Ctrl+Q` | Quit EchoOS |
| `Ctrl+M` | Manual command input |

## Advanced Features

### Custom Commands

Edit `config/commands.json` to add custom voice commands:

```json
{
  "custom_category": {
    "custom_command": ["phrase 1", "phrase 2"]
  }
}
```

### Application Aliases

Add aliases in `config/apps.json`:

```json
{
  "name": "MyApp",
  "path": "/path/to/app",
  "aliases": ["my app", "myapp", "app"]
}
```

### Settings Customization

Modify `config/settings.json`:

```json
{
  "tts": {
    "rate": 150,
    "volume": 0.9
  },
  "auth": {
    "similarity_threshold": 0.75,
    "session_timeout": 1800
  }
}
```

## Support

For issues and questions:
- Check logs: `echoos.log`
- Review documentation
- Submit GitHub issue
- Contact support

---

**Version**: 2.0  
**Last Updated**: December 2025
