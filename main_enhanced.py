#!/usr/bin/env python3
"""
EchoOS Enhanced Main Entry Point
Features: Dark Mode, Animated Waveform, Modern UI
Cross-platform voice-controlled operating system
"""

import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('echoos.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if all required dependencies are available"""
    missing = []
    
    try:
        import PySide6
    except ImportError:
        missing.append("PySide6")
    
    try:
        import vosk
    except ImportError:
        missing.append("vosk")
    
    try:
        import resemblyzer
    except ImportError:
        missing.append("resemblyzer")
    
    try:
        import pyttsx3
    except ImportError:
        missing.append("pyttsx3")
    
    try:
        import sounddevice
    except ImportError:
        missing.append("sounddevice")
    
    try:
        import psutil
    except ImportError:
        missing.append("psutil")
    
    if missing:
        logger.error(f"Missing dependencies: {', '.join(missing)}")
        return False
    
    return True


def check_vosk_model():
    """Check if Vosk model is available"""
    models_dir = Path("models")
    if not models_dir.exists():
        logger.error("Models directory not found")
        return False
    
    # Check for any vosk model
    for item in models_dir.iterdir():
        if item.is_dir() and item.name.startswith('vosk-model'):
            logger.info(f"Found Vosk model: {item.name}")
            return True
    
    logger.error("No Vosk model found")
    return False


def check_config():
    """Check if configuration files exist"""
    config_dir = Path("config")
    if not config_dir.exists():
        logger.info("Creating config directory")
        config_dir.mkdir(exist_ok=True)
    
    required_files = {
        'commands.json': '{}',
        'apps.json': '{"apps": []}',
        'users.pkl': None,
        'sessions.pkl': None
    }
    
    import json
    import pickle
    
    for filename, default_content in required_files.items():
        filepath = config_dir / filename
        if not filepath.exists():
            logger.info(f"Creating {filename}")
            if filename.endswith('.json'):
                with open(filepath, 'w') as f:
                    f.write(default_content)
            elif filename.endswith('.pkl'):
                with open(filepath, 'wb') as f:
                    pickle.dump({}, f)
    
    return True


def main():
    """Main application entry point"""
    logger.info("=" * 60)
    logger.info("EchoOS Enhanced - Starting...")
    logger.info("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Missing dependencies!")
        print("Please install required packages:")
        print("  pip install -r requirements.txt")
        return 1
    
    # Check Vosk model
    if not check_vosk_model():
        print("\n❌ Vosk model not found!")
        print("Please download the model:")
        print("  python scripts/download_vosk_model.py")
        return 1
    
    # Check/create config
    check_config()
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("EchoOS Enhanced")
    app.setOrganizationName("EchoOS")
    
    try:
        # Import modules
        from modules.auth import Authenticator
        from modules.stt import VoskManager
        from modules.tts import TTS
        from modules.parser import CommandParser
        from modules.executor import Executor
        from modules.app_discovery import AppDiscovery
        from modules.accessibility import AccessibilityManager
        from modules.ui_enhanced import EchoMainWindowEnhanced
        
        logger.info("Initializing components...")
        
        # Initialize TTS first (for feedback)
        tts = TTS()
        logger.info("✓ TTS initialized")
        
        # Initialize authentication
        auth = Authenticator(tts=tts)
        logger.info("✓ Authentication initialized")
        
        # Initialize STT
        stt_manager = VoskManager(tts=tts)
        logger.info("✓ STT initialized")
        
        # Initialize app discovery
        app_discovery = AppDiscovery()
        logger.info("✓ App discovery initialized")
        
        # Initialize parser
        parser = CommandParser(tts=tts)
        logger.info("✓ Command parser initialized")
        
        # Initialize executor
        executor = Executor(tts=tts, auth=auth)
        logger.info("✓ Command executor initialized")
        
        # Initialize accessibility
        accessibility = AccessibilityManager(tts=tts)
        logger.info("✓ Accessibility initialized")
        
        # Create and show main window
        logger.info("Creating enhanced main window...")
        window = EchoMainWindowEnhanced(
            auth=auth,
            stt_manager=stt_manager,
            app_discovery=app_discovery,
            parser=parser,
            executor=executor,
            tts=tts,
            accessibility=accessibility
        )
        
        window.show()
        logger.info("✓ Enhanced UI displayed")
        
        logger.info("=" * 60)
        logger.info("EchoOS Enhanced is ready!")
        logger.info("=" * 60)
        
        # Run application
        return app.exec()
        
    except Exception as e:
        logger.exception(f"Fatal error: {e}")
        QMessageBox.critical(
            None,
            "Fatal Error",
            f"Failed to start EchoOS:\n{str(e)}\n\nCheck echoos.log for details."
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
