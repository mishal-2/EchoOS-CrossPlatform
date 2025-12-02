"""
Setup script for EchoOS
Allows installation as a Python package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="echoos",
    version="2.0.0",
    author="M A Mohammed Mishal",
    author_email="1by22is076@bmsit.in",
    description="Secure offline voice-controlled operating system with biometric authentication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mishal-2/EchoOS-CrossPlatform",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: System :: Shells",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PySide6>=6.5.0",
        "vosk>=0.3.45",
        "sounddevice>=0.4.6",
        "pyaudio>=0.2.13",
        "pyttsx3>=2.90",
        "resemblyzer>=0.1.1.dev0",
        "librosa>=0.10.0",
        "python_speech_features>=0.6",
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "scikit-learn>=1.3.0",
        "rapidfuzz>=3.0.0",
        "psutil>=5.9.0",
        "cryptography>=41.0.0",
        "pyyaml>=6.0.1",
        "colorlog>=6.7.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
        ],
        "accessibility": [
            "pyautogui>=0.9.54",
            "opencv-python>=4.8.0",
            "pytesseract>=0.3.10",
            "Pillow>=10.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "echoos=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md"],
    },
    keywords="voice-control speech-recognition biometric-authentication offline accessibility",
    project_urls={
        "Bug Reports": "https://github.com/mishal-2/EchoOS-CrossPlatform/issues",
        "Source": "https://github.com/mishal-2/EchoOS-CrossPlatform",
        "Documentation": "https://github.com/mishal-2/EchoOS-CrossPlatform#readme",
    },
)
