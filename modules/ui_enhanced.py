"""
Enhanced User Interface Module for EchoOS
Features: Dark Mode, Animated Waveform, Modern Design
Cross-platform support for Windows, macOS, and Linux
"""

import logging
import threading
import numpy as np
from collections import deque
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QGroupBox, QLineEdit,
    QMessageBox, QStatusBar, QFrame
)
from PySide6.QtCore import Qt, Signal, QObject, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QPainter, QPen, QColor, QLinearGradient

logger = logging.getLogger(__name__)


class SignalEmitter(QObject):
    """Signal emitter for thread-safe GUI updates"""
    update_status = Signal(str)
    update_log = Signal(str)
    command_recognized = Signal(str)
    audio_data = Signal(object)  # For waveform visualization


class WaveformWidget(QWidget):
    """Animated waveform visualization widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(120)
        self.setMaximumHeight(120)
        
        # Audio data buffer
        self.buffer_size = 100
        self.audio_buffer = deque([0] * self.buffer_size, maxlen=self.buffer_size)
        
        # Animation state
        self.is_active = False
        self.animation_phase = 0
        
        # Colors for dark mode
        self.bg_color = QColor(30, 30, 30)
        self.wave_color = QColor(76, 175, 80)  # Green
        self.grid_color = QColor(50, 50, 50)
        
        # Setup animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_animation)
        self.timer.setInterval(50)  # 20 FPS
    
    def start_animation(self):
        """Start waveform animation"""
        self.is_active = True
        self.timer.start()
    
    def stop_animation(self):
        """Stop waveform animation"""
        self.is_active = False
        self.timer.stop()
        self.audio_buffer = deque([0] * self.buffer_size, maxlen=self.buffer_size)
        self.update()
    
    def add_audio_data(self, data):
        """Add audio data to buffer"""
        if isinstance(data, np.ndarray):
            # Normalize and downsample
            if len(data) > 0:
                avg = np.mean(np.abs(data))
                self.audio_buffer.append(float(avg))
        self.update()
    
    def _update_animation(self):
        """Update animation phase"""
        self.animation_phase = (self.animation_phase + 1) % 360
        
        # Add simulated data if no real audio
        if self.is_active and len(self.audio_buffer) > 0:
            if max(self.audio_buffer) < 0.01:  # No real audio
                # Generate smooth sine wave
                import math
                value = 0.3 * math.sin(math.radians(self.animation_phase * 3))
                self.audio_buffer.append(value)
        
        self.update()
    
    def paintEvent(self, event):
        """Paint waveform"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), self.bg_color)
        
        # Draw grid
        self._draw_grid(painter)
        
        # Draw waveform
        self._draw_waveform(painter)
        
        # Draw center line
        painter.setPen(QPen(self.grid_color, 2))
        mid_y = self.height() // 2
        painter.drawLine(0, mid_y, self.width(), mid_y)
    
    def _draw_grid(self, painter):
        """Draw background grid"""
        painter.setPen(QPen(self.grid_color, 1))
        
        # Horizontal lines
        for i in range(5):
            y = int(self.height() * i / 4)
            painter.drawLine(0, y, self.width(), y)
        
        # Vertical lines
        for i in range(10):
            x = int(self.width() * i / 9)
            painter.drawLine(x, 0, x, self.height())
    
    def _draw_waveform(self, painter):
        """Draw animated waveform"""
        if len(self.audio_buffer) < 2:
            return
        
        width = self.width()
        height = self.height()
        mid_y = height // 2
        
        # Create gradient
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0, QColor(76, 175, 80, 200))
        gradient.setColorAt(0.5, QColor(76, 175, 80, 255))
        gradient.setColorAt(1, QColor(76, 175, 80, 200))
        
        # Draw waveform
        painter.setPen(QPen(gradient, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        
        points = []
        buffer_list = list(self.audio_buffer)
        
        for i, value in enumerate(buffer_list):
            x = int(width * i / len(buffer_list))
            
            # Scale value to widget height
            scaled_value = value * (height * 0.4)
            y = int(mid_y - scaled_value)
            
            points.append((x, y))
        
        # Draw smooth curve through points
        if len(points) > 1:
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                painter.drawLine(x1, y1, x2, y2)
        
        # Draw glow effect when active
        if self.is_active:
            painter.setPen(QPen(QColor(76, 175, 80, 100), 6))
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                painter.drawLine(x1, y1, x2, y2)


class EchoMainWindowEnhanced(QMainWindow):
    """Enhanced main window with dark mode and animations"""
    
    def __init__(self, auth, stt_manager, app_discovery, parser, executor, tts, accessibility):
        super().__init__()
        
        # Store components
        self.auth = auth
        self.stt_manager = stt_manager
        self.app_discovery = app_discovery
        self.parser = parser
        self.executor = executor
        self.tts = tts
        self.accessibility = accessibility
        
        # State
        self.is_listening = False
        self.is_authenticated = False
        self.dark_mode = True  # Default to dark mode
        
        # Signal emitter for thread-safe updates
        self.signals = SignalEmitter()
        self.signals.update_status.connect(self._update_status_label)
        self.signals.update_log.connect(self._append_log)
        self.signals.command_recognized.connect(self._handle_command)
        self.signals.audio_data.connect(self._update_waveform)
        
        # Setup UI
        self._setup_ui()
        self._apply_dark_theme()
        
        logger.info("Enhanced main window initialized")
    
    def _setup_ui(self):
        """Setup enhanced user interface"""
        self.setWindowTitle("EchoOS - Voice-Controlled Operating System")
        self.setMinimumSize(900, 700)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Title section
        title_container = QVBoxLayout()
        title_label = QLabel("🎙️ EchoOS")
        title_font = QFont()
        title_font.setPointSize(28)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_container.addWidget(title_label)
        
        subtitle_label = QLabel("Voice-Controlled Operating System")
        subtitle_font = QFont()
        subtitle_font.setPointSize(12)
        subtitle_label.setFont(subtitle_font)
        title_container.addWidget(subtitle_label)
        
        header_layout.addLayout(title_container)
        header_layout.addStretch()
        
        # Theme toggle button
        self.theme_btn = QPushButton("☀️ Light Mode")
        self.theme_btn.clicked.connect(self._toggle_theme)
        self.theme_btn.setFixedSize(120, 40)
        header_layout.addWidget(self.theme_btn)
        
        main_layout.addLayout(header_layout)
        
        # Status indicator
        self.status_label = QLabel("Ready")
        status_font = QFont()
        status_font.setPointSize(14)
        status_font.setBold(True)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setMinimumHeight(50)
        main_layout.addWidget(self.status_label)
        
        # Waveform visualization
        waveform_group = QGroupBox("Audio Visualization")
        waveform_layout = QVBoxLayout()
        self.waveform = WaveformWidget()
        waveform_layout.addWidget(self.waveform)
        waveform_group.setLayout(waveform_layout)
        main_layout.addWidget(waveform_group)
        
        # Authentication Group
        auth_group = QGroupBox("🔐 Authentication")
        auth_layout = QVBoxLayout()
        
        # User info with icon
        self.user_label = QLabel("❌ Not authenticated")
        self.user_label.setFont(QFont("", 11, QFont.Bold))
        auth_layout.addWidget(self.user_label)
        
        # Auth buttons
        auth_buttons_layout = QHBoxLayout()
        
        self.register_btn = QPushButton("📝 Register New User")
        self.register_btn.clicked.connect(self._register_user)
        self.register_btn.setMinimumHeight(40)
        auth_buttons_layout.addWidget(self.register_btn)
        
        self.login_btn = QPushButton("🔑 Voice Login")
        self.login_btn.clicked.connect(self._authenticate_user)
        self.login_btn.setMinimumHeight(40)
        auth_buttons_layout.addWidget(self.login_btn)
        
        self.logout_btn = QPushButton("🚪 Logout")
        self.logout_btn.clicked.connect(self._logout_user)
        self.logout_btn.setEnabled(False)
        self.logout_btn.setMinimumHeight(40)
        auth_buttons_layout.addWidget(self.logout_btn)
        
        auth_layout.addLayout(auth_buttons_layout)
        auth_group.setLayout(auth_layout)
        main_layout.addWidget(auth_group)
        
        # Voice Control Group
        control_group = QGroupBox("🎤 Voice Control")
        control_layout = QVBoxLayout()
        
        # Control buttons
        control_buttons_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶️ Start Listening")
        self.start_btn.clicked.connect(self._start_listening)
        self.start_btn.setEnabled(False)
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setFont(QFont("", 12, QFont.Bold))
        control_buttons_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Stop Listening")
        self.stop_btn.clicked.connect(self._stop_listening)
        self.stop_btn.setEnabled(False)
        self.stop_btn.setMinimumHeight(50)
        self.stop_btn.setFont(QFont("", 12, QFont.Bold))
        control_buttons_layout.addWidget(self.stop_btn)
        
        control_layout.addLayout(control_buttons_layout)
        
        # Command input (manual)
        manual_layout = QHBoxLayout()
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("💬 Or type a command manually...")
        self.command_input.returnPressed.connect(self._execute_manual_command)
        self.command_input.setMinimumHeight(40)
        manual_layout.addWidget(self.command_input)
        
        self.execute_btn = QPushButton("⚡ Execute")
        self.execute_btn.clicked.connect(self._execute_manual_command)
        self.execute_btn.setMinimumHeight(40)
        manual_layout.addWidget(self.execute_btn)
        
        control_layout.addLayout(manual_layout)
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)
        
        # Log Group
        log_group = QGroupBox("📋 Activity Log")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(180)
        self.log_text.setFont(QFont("Consolas", 9))
        log_layout.addWidget(self.log_text)
        
        # Clear log button
        clear_log_btn = QPushButton("🗑️ Clear Log")
        clear_log_btn.clicked.connect(lambda: self.log_text.clear())
        clear_log_btn.setMaximumWidth(150)
        log_layout.addWidget(clear_log_btn)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🟢 Ready")
        
        # Add initial log message
        self._append_log("🎙️ EchoOS initialized. Please authenticate to start.")
    
    def _apply_dark_theme(self):
        """Apply dark mode theme"""
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #1e1e1e;
                }
                QWidget {
                    background-color: #1e1e1e;
                    color: #e0e0e0;
                }
                QGroupBox {
                    border: 2px solid #3d3d3d;
                    border-radius: 8px;
                    margin-top: 12px;
                    padding-top: 15px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 15px;
                    padding: 0 5px;
                }
                QPushButton {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 2px solid #3d3d3d;
                    border-radius: 6px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3d3d3d;
                    border: 2px solid #4caf50;
                }
                QPushButton:pressed {
                    background-color: #4caf50;
                }
                QPushButton:disabled {
                    background-color: #252525;
                    color: #666666;
                    border: 2px solid #2d2d2d;
                }
                QLineEdit {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border: 2px solid #3d3d3d;
                    border-radius: 6px;
                    padding: 8px;
                    font-size: 11px;
                }
                QLineEdit:focus {
                    border: 2px solid #4caf50;
                }
                QTextEdit {
                    background-color: #252525;
                    color: #e0e0e0;
                    border: 2px solid #3d3d3d;
                    border-radius: 6px;
                    padding: 8px;
                }
                QLabel {
                    color: #e0e0e0;
                }
                QStatusBar {
                    background-color: #252525;
                    color: #e0e0e0;
                }
            """)
            self.theme_btn.setText("☀️ Light Mode")
        else:
            self._apply_light_theme()
    
    def _apply_light_theme(self):
        """Apply light mode theme"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                background-color: #f5f5f5;
                color: #212121;
            }
            QGroupBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 15px;
                font-weight: bold;
                font-size: 13px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #ffffff;
                color: #212121;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                border: 2px solid #4caf50;
            }
            QPushButton:pressed {
                background-color: #4caf50;
                color: white;
            }
            QPushButton:disabled {
                background-color: #fafafa;
                color: #9e9e9e;
                border: 2px solid #e0e0e0;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #212121;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid #4caf50;
            }
            QTextEdit {
                background-color: #ffffff;
                color: #212121;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px;
            }
            QLabel {
                color: #212121;
            }
            QStatusBar {
                background-color: #ffffff;
                color: #212121;
            }
        """)
        self.theme_btn.setText("🌙 Dark Mode")
        
        # Update waveform colors for light mode
        self.waveform.bg_color = QColor(255, 255, 255)
        self.waveform.grid_color = QColor(230, 230, 230)
        self.waveform.update()
    
    def _toggle_theme(self):
        """Toggle between dark and light mode"""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self._apply_dark_theme()
            self.waveform.bg_color = QColor(30, 30, 30)
            self.waveform.grid_color = QColor(50, 50, 50)
        else:
            self._apply_light_theme()
        self.waveform.update()
    
    def _update_status_label(self, text: str):
        """Update status label (thread-safe)"""
        self.status_label.setText(text)
        
        # Color based on status
        if "listening" in text.lower():
            if self.dark_mode:
                self.status_label.setStyleSheet("""
                    background-color: #1b5e20;
                    color: #a5d6a7;
                    border-radius: 8px;
                    padding: 10px;
                """)
            else:
                self.status_label.setStyleSheet("""
                    background-color: #c8e6c9;
                    color: #1b5e20;
                    border-radius: 8px;
                    padding: 10px;
                """)
        elif "error" in text.lower() or "failed" in text.lower():
            if self.dark_mode:
                self.status_label.setStyleSheet("""
                    background-color: #b71c1c;
                    color: #ffcdd2;
                    border-radius: 8px;
                    padding: 10px;
                """)
            else:
                self.status_label.setStyleSheet("""
                    background-color: #ffcdd2;
                    color: #b71c1c;
                    border-radius: 8px;
                    padding: 10px;
                """)
        else:
            if self.dark_mode:
                self.status_label.setStyleSheet("""
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    border-radius: 8px;
                    padding: 10px;
                """)
            else:
                self.status_label.setStyleSheet("""
                    background-color: #e8f5e9;
                    color: #2e7d32;
                    border-radius: 8px;
                    padding: 10px;
                """)
    
    def _append_log(self, text: str):
        """Append to log (thread-safe)"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {text}")
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def _update_waveform(self, data):
        """Update waveform with audio data"""
        self.waveform.add_audio_data(data)
    
    def _register_user(self):
        """Register new user"""
        from PySide6.QtWidgets import QInputDialog
        
        username, ok = QInputDialog.getText(
            self, "Register User", "Enter username:"
        )
        
        if ok and username:
            self._append_log(f"📝 Registering user: {username}")
            self.signals.update_status.emit("🎤 Recording voice sample...")
            
            def register():
                success = self.auth.register_user(username, duration=5)
                if success:
                    self.signals.update_status.emit(f"✅ User {username} registered!")
                    self.signals.update_log.emit(f"✅ User {username} registered successfully")
                else:
                    self.signals.update_status.emit("❌ Registration failed")
                    self.signals.update_log.emit("❌ Registration failed")
            
            thread = threading.Thread(target=register)
            thread.start()
    
    def _authenticate_user(self):
        """Authenticate user by voice"""
        self._append_log("🔑 Starting voice authentication...")
        self.signals.update_status.emit("🎤 Authenticating...")
        
        def authenticate():
            username = self.auth.authenticate(duration=3, threshold=0.75)
            if username:
                self.is_authenticated = True
                self.signals.update_status.emit(f"✅ Authenticated as {username}")
                self.signals.update_log.emit(f"✅ Authenticated as {username}")
                
                # Update UI
                self.user_label.setText(f"✅ Logged in as: {username}")
                self.start_btn.setEnabled(True)
                self.logout_btn.setEnabled(True)
                self.login_btn.setEnabled(False)
                self.register_btn.setEnabled(False)
            else:
                self.signals.update_status.emit("❌ Authentication failed")
                self.signals.update_log.emit("❌ Authentication failed")
        
        thread = threading.Thread(target=authenticate)
        thread.start()
    
    def _logout_user(self):
        """Logout current user"""
        self.auth.logout()
        self.is_authenticated = False
        
        self.user_label.setText("❌ Not authenticated")
        self.start_btn.setEnabled(False)
        self.logout_btn.setEnabled(False)
        self.login_btn.setEnabled(True)
        self.register_btn.setEnabled(True)
        
        self._append_log("🚪 Logged out")
        self.signals.update_status.emit("Logged out")
    
    def _start_listening(self):
        """Start voice recognition"""
        if not self.is_authenticated:
            QMessageBox.warning(self, "Not Authenticated", "Please authenticate first")
            return
        
        if not self.stt_manager.is_model_loaded():
            QMessageBox.critical(self, "Model Not Loaded", 
                               "Vosk model not loaded. Please download the model first.")
            return
        
        self.is_listening = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        # Start waveform animation
        self.waveform.start_animation()
        
        self._append_log("🎤 Started listening for voice commands")
        self.signals.update_status.emit("🎤 Listening...")
        self.status_bar.showMessage("🔴 Recording...")
        
        # Start listening in thread
        def listen():
            self.stt_manager.start_listening(self._on_speech_recognized)
        
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
    
    def _stop_listening(self):
        """Stop voice recognition"""
        self.is_listening = False
        self.stt_manager.stop_listening()
        
        # Stop waveform animation
        self.waveform.stop_animation()
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        self._append_log("⏹️ Stopped listening")
        self.signals.update_status.emit("Ready")
        self.status_bar.showMessage("🟢 Ready")
    
    def _on_speech_recognized(self, text: str):
        """Handle recognized speech"""
        self.signals.command_recognized.emit(text)
    
    def _handle_command(self, text: str):
        """Handle recognized command"""
        self._append_log(f"🗣️ Recognized: {text}")
        
        # Parse command
        command = self.parser.parse(text)
        
        if command:
            self._append_log(f"⚙️ Command: {command['category']}.{command['intent']}")
            
            # Execute command
            success = self.executor.execute(command)
            
            if success:
                self._append_log("✅ Command executed successfully")
            else:
                self._append_log("❌ Command execution failed")
        else:
            self._append_log("❌ Command not recognized")
            if self.tts:
                self.tts.speak("Command not recognized")
    
    def _execute_manual_command(self):
        """Execute manually typed command"""
        text = self.command_input.text().strip()
        if text:
            self._handle_command(text)
            self.command_input.clear()
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.is_listening:
            self._stop_listening()
        
        logger.info("Enhanced main window closed")
        event.accept()
