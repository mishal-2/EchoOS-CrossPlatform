# EchoOS Development Guide

## Table of Contents

1. [Development Setup](#development-setup)
2. [Project Structure](#project-structure)
3. [Architecture](#architecture)
4. [Adding Features](#adding-features)
5. [Testing](#testing)
6. [Code Style](#code-style)
7. [Contributing](#contributing)

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment tool
- Code editor (VS Code recommended)

### Setup Steps

1. **Clone Repository**
   ```bash
   git clone https://github.com/Mishal-Projects/EchoOS-CrossPlatform.git
   cd EchoOS-CrossPlatform
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Setup Configuration**
   ```bash
   python scripts/setup_config.py
   python scripts/download_vosk_model.py
   ```

5. **Run Tests**
   ```bash
   pytest tests/
   ```

### Development Dependencies

Create `requirements-dev.txt`:

```
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
black>=22.0.0
flake8>=5.0.0
mypy>=0.990
sphinx>=5.0.0
```

## Project Structure

```
EchoOS-CrossPlatform/
├── main.py                    # Application entry point
├── setup.py                   # Package installation
├── requirements.txt           # Production dependencies
├── requirements-dev.txt       # Development dependencies
│
├── modules/                   # Core modules
│   ├── __init__.py
│   ├── auth.py               # Authentication
│   ├── stt.py                # Speech-to-text
│   ├── tts.py                # Text-to-speech
│   ├── parser.py             # Command parsing
│   ├── executor.py           # Command execution
│   ├── app_discovery.py      # App discovery
│   ├── accessibility.py      # Accessibility
│   ├── ui.py                 # User interface
│   └── config.py             # Configuration
│
├── scripts/                   # Utility scripts
│   ├── download_vosk_model.py
│   ├── discover_apps.py
│   ├── setup_config.py
│   └── test_microphone.py
│
├── tests/                     # Unit tests
│   ├── test_auth.py
│   ├── test_parser.py
│   ├── test_executor.py
│   ├── test_stt.py
│   └── test_tts.py
│
├── docs/                      # Documentation
│   ├── API.md
│   ├── USER_MANUAL.md
│   └── DEVELOPMENT.md
│
├── config/                    # Configuration files
│   ├── commands.json
│   ├── apps.json
│   ├── settings.json
│   ├── users.pkl
│   └── sessions.pkl
│
└── models/                    # Voice models
    └── vosk-model-small-en-us-0.15/
```

## Architecture

### Module Dependencies

```
main.py
  ├── modules.ui (EchoMainWindow)
  │   ├── modules.auth (Authenticator)
  │   ├── modules.stt (VoskManager)
  │   ├── modules.tts (TTS)
  │   ├── modules.parser (CommandParser)
  │   ├── modules.executor (Executor)
  │   ├── modules.app_discovery (AppDiscovery)
  │   └── modules.accessibility (AccessibilityManager)
  └── modules.config (ConfigManager)
```

### Data Flow

```
Voice Input → STT → Parser → Executor → System Action
                                ↓
                              TTS Feedback
```

### Authentication Flow

```
User Registration:
Audio Sample → Resemblyzer → Voice Embedding → Storage

User Authentication:
Audio Sample → Resemblyzer → Compare Embeddings → Session Creation
```

## Adding Features

### Adding New Voice Commands

1. **Update Commands Configuration**

Edit `config/commands.json`:

```json
{
  "new_category": {
    "new_intent": ["phrase 1", "phrase 2", "phrase 3"]
  }
}
```

2. **Add Parser Logic**

In `modules/parser.py`:

```python
def _parse_new_category(self, text: str) -> Optional[Dict]:
    """Parse new category commands"""
    # Implementation
    pass
```

3. **Add Executor Logic**

In `modules/executor.py`:

```python
def _execute_new_category(self, intent: str, params: Dict) -> bool:
    """Execute new category commands"""
    if intent == 'new_intent':
        # Implementation
        return True
    return False
```

4. **Add Tests**

In `tests/test_executor.py`:

```python
def test_new_category_commands(self):
    """Test new category commands"""
    cmd = {
        'category': 'new_category',
        'intent': 'new_intent',
        'parameters': {}
    }
    result = self.executor.execute(cmd)
    self.assertTrue(result)
```

5. **Update Documentation**

Add to `docs/USER_MANUAL.md` and `docs/API.md`

### Adding New Module

1. **Create Module File**

```python
# modules/new_module.py
"""
New Module Description
"""

import logging

logger = logging.getLogger(__name__)


class NewModule:
    """New module class"""
    
    def __init__(self):
        """Initialize module"""
        logger.info("NewModule initialized")
    
    def method(self):
        """Module method"""
        pass
```

2. **Add to __init__.py**

```python
# modules/__init__.py
from .new_module import NewModule

__all__ = ['NewModule', ...]
```

3. **Integrate in main.py**

```python
from modules.new_module import NewModule

# In main()
new_module = NewModule()
```

4. **Add Tests**

```python
# tests/test_new_module.py
import unittest
from modules.new_module import NewModule

class TestNewModule(unittest.TestCase):
    def test_initialization(self):
        module = NewModule()
        self.assertIsNotNone(module)
```

## Testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_parser.py

# Run with coverage
pytest --cov=modules tests/

# Run with verbose output
pytest -v tests/

# Run specific test
pytest tests/test_parser.py::TestCommandParser::test_parse_system_commands
```

### Writing Tests

```python
import unittest
from modules.parser import CommandParser

class TestCommandParser(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = CommandParser()
    
    def tearDown(self):
        """Clean up after tests"""
        pass
    
    def test_feature(self):
        """Test specific feature"""
        result = self.parser.parse("test command")
        self.assertIsNotNone(result)
        self.assertEqual(result['category'], 'expected')
```

### Test Coverage

Aim for:
- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Key workflows
- **Edge Cases**: Error handling

## Code Style

### Python Style Guide

Follow PEP 8 with these specifics:

```python
# Imports
import standard_library
import third_party
from local_module import Class

# Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# Classes
class MyClass:
    """Class docstring"""
    
    def __init__(self):
        """Constructor docstring"""
        self.attribute = value
    
    def method(self, param: str) -> bool:
        """
        Method docstring
        
        Args:
            param: Parameter description
            
        Returns:
            Return value description
        """
        pass

# Functions
def function_name(param: str) -> str:
    """Function docstring"""
    return result
```

### Formatting

Use Black for code formatting:

```bash
black modules/ tests/
```

### Linting

Use flake8 for linting:

```bash
flake8 modules/ tests/
```

### Type Hints

Use type hints for better code clarity:

```python
from typing import Optional, List, Dict

def process_data(data: List[str]) -> Optional[Dict]:
    """Process data with type hints"""
    pass
```

## Debugging

### Logging

Use Python's logging module:

```python
import logging

logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.exception("Exception with traceback")
```

### Debug Mode

Enable debug logging:

```python
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

1. **Import Errors**: Check PYTHONPATH
2. **Module Not Found**: Install dependencies
3. **Audio Issues**: Test microphone
4. **Model Loading**: Verify model path

## Performance Optimization

### Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats()
```

### Memory Profiling

```python
from memory_profiler import profile

@profile
def function_to_profile():
    pass
```

## Contributing

### Workflow

1. **Fork Repository**
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-feature
   ```

3. **Make Changes**
   - Write code
   - Add tests
   - Update documentation

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Add new feature"
   ```

5. **Push to Fork**
   ```bash
   git push origin feature/new-feature
   ```

6. **Create Pull Request**

### Commit Messages

Format:
```
<type>: <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

Example:
```
feat: Add multi-language support

- Add language detection
- Implement translation system
- Update UI for language selection

Closes #123
```

### Code Review

Checklist:
- [ ] Code follows style guide
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] Performance acceptable

## Release Process

1. **Update Version**
   - `setup.py`
   - `main.py`
   - `CHANGELOG.md`

2. **Run Tests**
   ```bash
   pytest tests/
   ```

3. **Build Package**
   ```bash
   python setup.py sdist bdist_wheel
   ```

4. **Tag Release**
   ```bash
   git tag -a v2.0.0 -m "Release version 2.0.0"
   git push origin v2.0.0
   ```

5. **Create GitHub Release**

## Resources

- [Python Documentation](https://docs.python.org/)
- [PySide6 Documentation](https://doc.qt.io/qtforpython/)
- [Vosk Documentation](https://alphacephei.com/vosk/)
- [Resemblyzer Documentation](https://github.com/resemble-ai/Resemblyzer)

---

**Version**: 2.0  
**Last Updated**: December 2025
