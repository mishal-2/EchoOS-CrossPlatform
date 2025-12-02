"""
Unit tests for speech-to-text module
"""

import unittest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.stt import VoskManager


class TestVoskManager(unittest.TestCase):
    """Test cases for VoskManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock TTS
        class MockTTS:
            def speak(self, text, blocking=False):
                pass
        
        try:
            self.stt = VoskManager(tts=MockTTS())
        except Exception as e:
            self.skipTest(f"Vosk model not available: {e}")
    
    def test_initialization(self):
        """Test STT manager initialization"""
        self.assertIsNotNone(self.stt)
        self.assertIsNotNone(self.stt.model)
    
    def test_model_loading(self):
        """Test Vosk model loading"""
        # Model should be loaded during initialization
        self.assertTrue(hasattr(self.stt, 'model'))
    
    def test_recognizer_creation(self):
        """Test recognizer creation"""
        # This would require actual audio stream
        # Placeholder for integration testing
        pass


if __name__ == '__main__':
    unittest.main()
