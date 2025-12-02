"""
Unit tests for text-to-speech module
"""

import unittest
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.tts import TTS


class TestTTS(unittest.TestCase):
    """Test cases for TTS class"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            self.tts = TTS()
        except Exception as e:
            self.skipTest(f"TTS engine not available: {e}")
    
    def test_initialization(self):
        """Test TTS initialization"""
        self.assertIsNotNone(self.tts)
        self.assertIsNotNone(self.tts.engine)
    
    def test_speak_method(self):
        """Test speak method"""
        # This will actually speak in test environment
        # In production, mock pyttsx3 engine
        try:
            self.tts.speak("Test message", blocking=False)
        except Exception as e:
            self.fail(f"Speak method failed: {e}")
    
    def test_voice_properties(self):
        """Test voice property getters"""
        rate = self.tts.get_rate()
        volume = self.tts.get_volume()
        
        self.assertIsInstance(rate, (int, float))
        self.assertIsInstance(volume, (int, float))
        self.assertGreaterEqual(volume, 0.0)
        self.assertLessEqual(volume, 1.0)
    
    def test_voice_property_setters(self):
        """Test voice property setters"""
        original_rate = self.tts.get_rate()
        original_volume = self.tts.get_volume()
        
        # Test rate
        self.tts.set_rate(150)
        self.assertEqual(self.tts.get_rate(), 150)
        
        # Test volume
        self.tts.set_volume(0.8)
        self.assertAlmostEqual(self.tts.get_volume(), 0.8, places=1)
        
        # Restore original values
        self.tts.set_rate(original_rate)
        self.tts.set_volume(original_volume)


if __name__ == '__main__':
    unittest.main()
