"""
Enhanced UI Module for EchoOS with Dark Mode and Waveform Visualization
"""

import sys
import threading
import numpy as np
from collections import deque
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QGroupBox, QLineEdit,
    QInputDialog, QMessageBox
)
from PySide6.QtCore import QTimer, Signal, QObject, Qt
from PySide6.QtGui import QPainter, QColor, QPen


class SignalEmitter(QObject):
    """Signal emitter for thread-safe GUI updates"""
    update_status = Signal(str)
    update_log = Signal(str)
    audio_data = Signal(object)
    show_message = Signal(str, str)  # title, message


class WaveformWidget(QWidget):
    """Animated waveform visualization widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.buffer_size = 100
        self.audio_buffer = deque(maxlen=self.buffer_size)
        self.wave_color = QColor(76, 175, 80)  # Green
        self.is_active = False
        
        # Initialize with zeros
        for _ in range(self.buffer_size):
            self.audio_buffer.append(0.0)
        
        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(50)  # 20 FPS
        
        # Idle animation
        self.idle_phase = 0
    
    def start_animation(self):
        """Start waveform animation"""
        self.is_active = True
        self.timer.start()
    
    def stop_animation(self):
        """Stop waveform animation"""
        self.is_active = False
        self.timer.stop()
    
    def add_audio_data(self, data):
        """Add audio data to buffer"""
        if isinstance(data, (list, np.ndarray)):
            for value in data[-10:]:  # Add last 10 samples
                self.audio_buffer.append(float(value))
    
    def paintEvent(self, event):
        """Paint the waveform"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QColor(30, 30, 30))
        
        # Grid lines
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        for i in range(0, self.height(), 30):
            painter.drawLine(0, i, self.width(), i)
        
        # Waveform
        if not self.audio_buffer:
            return
        
        width = self.width()
        height = self.height()
        center_y = height // 2
        
        # Draw waveform
        painter.setPen(QPen(self.wave_color, 2))
        
        points = []
        for i, value in enumerate(self.audio_buffer):
            x = int((i / self.buffer_size) * width)
            
            if self.is_active and abs(value) > 0.001:
                # Active: use real audio data
                y = center_y - int(value * center_y * 0.8)
            else:
                # Idle: sine wave animation
                phase = (i / self.buffer_size) * 2 * np.pi + self.idle_phase
                y = center_y - int(np.sin(phase) * 20)
            
            points.append((x, y))
        
        # Draw lines between points
        for i in range(len(points) - 1):
            painter.drawLine(points[i][0], points[i][1], 
                           points[i+1][0], points[i+1][1])
        
        # Update idle animation phase
        if not self.is_active:
            self.idle_phase += 0.1
            if self.idle_phase > 2 * np.pi:
                self.idle_phase = 0


class EchoMainWindowEnhanced(QMainWindow):
    """Enhanced main window with dark mode and waveform"""
    
    def __init__(self, auth, stt_manager, tts, accessibility, command_parser, executor, parent=None):
        super().__init__()
        
        self.stt_manager = stt_manager
        self.command_parser = command_parser
        self.executor = executor
        self.auth = auth
        self.tts = tts
        
        self.is_listening = False
        self.is_authenticated = False
        self.dark_mode = True
        
        # Signal emitter for thread-safe updates
        self.signals = SignalEmitter()
        self.signals.update_status.connect(self._update_status)
        self.signals.update_log.connect(self._append_log)
        self.signals.audio_data.connect(self._update_waveform)
        self.signals.show_message.connect(self._show_message)
        
        self.setWindowTitle("EchoOS Enhanced - Voice Controlled OS")
        self.setGeometry(100, 100, 900, 700)
        
        self._init_ui()
        self._apply_dark_theme()
    
    def _init_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Header with theme toggle
        header_layout = QHBoxLayout()
        title_label = QLabel("🎙️ EchoOS Enhanced")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.theme_btn = QPushButton("☀️ Light Mode")
        self.theme_btn.clicked.connect(self._toggle_theme)
        self.theme_btn.setMaximumWidth(120)
        header_layout.addWidget(self.theme_btn)
        
        main_layout.addLayout(header_layout)
        
        # Waveform visualization
        waveform_group = QGroupBox("📊 Audio Visualization")
        waveform_layout = QVBoxLayout()
        self.waveform = WaveformWidget()
        waveform_layout.addWidget(self.waveform)
        waveform_group.setLayout(waveform_layout)
        main_layout.addWidget(waveform_group)
        
        # Authentication section
        auth_group = QGroupBox("🔐 Authentication")
        auth_layout = QVBoxLayout()
        
        self.user_label = QLabel("❌ Not authenticated")
        self.user_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        auth_layout.addWidget(self.user_label)
        
        auth_buttons = QHBoxLayout()
        self.register_btn = QPushButton("📝 Register New User")
        self.register_btn.clicked.connect(self._register_user)
        auth_buttons.addWidget(self.register_btn)
        
        self.login_btn = QPushButton("🔑 Voice Login")
        self.login_btn.clicked.connect(self._authenticate_user)
        auth_buttons.addWidget(self.login_btn)
        
        self.logout_btn = QPushButton("🚪 Logout")
        self.logout_btn.clicked.connect(self._logout_user)
        self.logout_btn.setEnabled(False)
        auth_buttons.addWidget(self.logout_btn)
        
        auth_layout.addLayout(auth_buttons)
        auth_group.setLayout(auth_layout)
        main_layout.addWidget(auth_group)
        
        # Voice control section
        control_group = QGroupBox("🎤 Voice Control")
        control_layout = QVBoxLayout()
        
        control_buttons = QHBoxLayout()
        self.start_btn = QPushButton("▶️ Start Listening")
        self.start_btn.clicked.connect(self._start_listening)
        self.start_btn.setEnabled(False)
        control_buttons.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Stop Listening")
        self.stop_btn.clicked.connect(self._stop_listening)
        self.stop_btn.setEnabled(False)
        control_buttons.addWidget(self.stop_btn)
        
        control_layout.addLayout(control_buttons)
        
        self.command_input = QLineEdit()
        self.command_input.setPlaceholderText("Or type command here...")
        self.command_input.returnPressed.connect(self._execute_typed_command)
        control_layout.addWidget(self.command_input)
        
        execute_btn = QPushButton("⚡ Execute")
        execute_btn.clicked.connect(self._execute_typed_command)
        control_layout.addWidget(execute_btn)
        
        control_group.setLayout(control_layout)
        main_layout.addWidget(control_group)
        
        # Status section
        status_group = QGroupBox("📊 Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            background-color: #2d2d2d;
            color: #e0e0e0;
            border-radius: 8px;
            padding: 10px;
            font-size: 12px;
        """)
        status_layout.addWidget(self.status_label)
        
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)
        
        # Log section
        log_group = QGroupBox("📝 Activity Log")
        log_layout = QVBoxLayout()
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        log_layout.addWidget(self.log_text)
        
        clear_btn = QPushButton("🗑️ Clear Log")
        clear_btn.clicked.connect(self.log_text.clear)
        log_layout.addWidget(clear_btn)
        
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)
        
        # Start idle animation
        self.waveform.start_animation()
        
        self._append_log("🚀 EchoOS Enhanced started")
        self._append_log("🌙 Dark mode enabled")
        
        if self.auth.is_voice_auth_available():
            self._append_log("✅ Voice authentication available")
        else:
            self._append_log("⚠️ Voice authentication not available")
    
    def _toggle_theme(self):
        """Toggle between dark and light themes"""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self._apply_dark_theme()
        else:
            self._apply_light_theme()
    
    def _apply_dark_theme(self):
        """Apply dark mode theme"""
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
    
    def _update_status(self, text: str):
        """Update status label (thread-safe)"""
        self.status_label.setText(text)
        
        # Color coding
        if "✅" in text or "success" in text.lower():
            if self.dark_mode:
                self.status_label.setStyleSheet("""
                    background-color: #1b5e20;
                    color: #c8e6c9;
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
        elif "❌" in text or "failed" in text.lower() or "error" in text.lower():
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
    
    def _show_message(self, title, message):
        """Show message box (thread-safe)"""
        QMessageBox.information(self, title, message)
    
    def _register_user(self):
        """Register new user"""
        username, ok = QInputDialog.getText(
            self, "📝 Register User", 
            "Enter username:\n\n(You will be asked to speak for 5 seconds)"
        )
        
        if ok and username:
            self._append_log(f"📝 Registering user: {username}")
            self._append_log("⏳ Please check the console window for recording instructions")
            self.signals.update_status.emit("🎤 Recording voice sample... (check console)")
            
            # Disable buttons during registration
            self.register_btn.setEnabled(False)
            self.login_btn.setEnabled(False)
            
            def register():
                try:
                    print("\n" + "="*70)
                    print(f"REGISTERING USER: {username}")
                    print("="*70)
                    
                    success = self.auth.register_user(username, duration=5)
                    
                    if success:
                        self.signals.update_status.emit(f"✅ User {username} registered!")
                        self.signals.update_log.emit(f"✅ User {username} registered successfully")
                        self.signals.update_log.emit("💡 You can now use 'Voice Login' to authenticate")
                        self.signals.show_message.emit(
                            "✅ Registration Successful",
                            f"User '{username}' has been registered!\n\nYou can now login using voice authentication."
                        )
                    else:
                        self.signals.update_status.emit("❌ Registration failed")
                        self.signals.update_log.emit("❌ Registration failed - check console for details")
                        self.signals.show_message.emit(
                            "❌ Registration Failed",
                            "Registration failed. Please check:\n\n"
                            "1. Microphone is connected and working\n"
                            "2. Microphone permissions are granted\n"
                            "3. You spoke clearly during recording\n\n"
                            "Run: python scripts/fix_audio.py"
                        )
                except Exception as e:
                    self.signals.update_status.emit(f"❌ Error: {str(e)}")
                    self.signals.update_log.emit(f"❌ Error: {str(e)}")
                    self.signals.show_message.emit(
                        "❌ Error",
                        f"An error occurred:\n\n{str(e)}\n\nCheck console for details."
                    )
                finally:
                    # Re-enable buttons
                    self.signals.update_log.emit("🔄 Ready for next operation")
                    self.register_btn.setEnabled(True)
                    self.login_btn.setEnabled(True)
            
            thread = threading.Thread(target=register, daemon=True)
            thread.start()
    
    def _authenticate_user(self):
        """Authenticate user by voice"""
        self._append_log("🔑 Starting voice authentication...")
        self._append_log("⏳ Please check the console window for recording instructions")
        self.signals.update_status.emit("🎤 Authenticating... (check console)")
        
        # Disable buttons during authentication
        self.login_btn.setEnabled(False)
        self.register_btn.setEnabled(False)
        
        def authenticate():
            try:
                print("\n" + "="*70)
                print("VOICE AUTHENTICATION")
                print("="*70)
                
                username = self.auth.authenticate(duration=3, threshold=0.75)
                
                if username:
                    self.is_authenticated = True
                    self.signals.update_status.emit(f"✅ Authenticated as {username}")
                    self.signals.update_log.emit(f"✅ Authenticated as {username}")
                    self.signals.update_log.emit("💡 You can now use voice commands")
                    
                    # Update UI
                    self.user_label.setText(f"✅ Logged in as: {username}")
                    self.start_btn.setEnabled(True)
                    self.logout_btn.setEnabled(True)
                    self.login_btn.setEnabled(False)
                    self.register_btn.setEnabled(False)
                    
                    self.signals.show_message.emit(
                        "✅ Authentication Successful",
                        f"Welcome {username}!\n\nYou can now use voice commands."
                    )
                else:
                    self.signals.update_status.emit("❌ Authentication failed")
                    self.signals.update_log.emit("❌ Authentication failed - check console for details")
                    self.signals.show_message.emit(
                        "❌ Authentication Failed",
                        "Authentication failed. Please:\n\n"
                        "1. Ensure you are registered\n"
                        "2. Speak clearly during authentication\n"
                        "3. Check microphone is working\n\n"
                        "Run: python scripts/fix_audio.py"
                    )
                    # Re-enable buttons
                    self.login_btn.setEnabled(True)
                    self.register_btn.setEnabled(True)
            except Exception as e:
                self.signals.update_status.emit(f"❌ Error: {str(e)}")
                self.signals.update_log.emit(f"❌ Error: {str(e)}")
                self.signals.show_message.emit(
                    "❌ Error",
                    f"An error occurred:\n\n{str(e)}\n\nCheck console for details."
                )
                # Re-enable buttons
                self.login_btn.setEnabled(True)
                self.register_btn.setEnabled(True)
        
        thread = threading.Thread(target=authenticate, daemon=True)
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
        """Start listening for voice commands"""
        if not self.is_authenticated:
            self._append_log("❌ Please authenticate first")
            return
        
        self.is_listening = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        
        self._append_log("🎤 Listening for commands...")
        self.signals.update_status.emit("🎤 Listening...")
        
        def listen():
            while self.is_listening:
                try:
                    text = self.stt_manager.listen()
                    if text:
                        self.signals.update_log.emit(f"🗣️ Heard: {text}")
                        
                        # Parse and execute
                        command = self.command_parser.parse(text)
                        if command:
                            self.signals.update_log.emit(f"⚙️ Executing: {command.action}")
                            result = self.executor.execute(command)
                            
                            if result.success:
                                self.signals.update_log.emit(f"✅ {result.message}")
                                if self.tts:
                                    self.tts.speak(result.message)
                            else:
                                self.signals.update_log.emit(f"❌ {result.message}")
                                if self.tts:
                                    self.tts.speak(result.message)
                except Exception as e:
                    self.signals.update_log.emit(f"❌ Error: {str(e)}")
        
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
    
    def _stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        self._append_log("⏹️ Stopped listening")
        self.signals.update_status.emit("Ready")
    
    def _execute_typed_command(self):
        """Execute typed command"""
        text = self.command_input.text().strip()
        if not text:
            return
        
        self._append_log(f"⌨️ Typed: {text}")
        
        command = self.command_parser.parse(text)
        if command:
            self._append_log(f"⚙️ Executing: {command.action}")
            result = self.executor.execute(command)
            
            if result.success:
                self._append_log(f"✅ {result.message}")
                if self.tts:
                    self.tts.speak(result.message)
            else:
                self._append_log(f"❌ {result.message}")
                if self.tts:
                    self.tts.speak(result.message)
        else:
            self._append_log("❌ Could not parse command")
        
        self.command_input.clear()
    
    def closeEvent(self, event):
        """Handle window close"""
        self.is_listening = False
        self.waveform.stop_animation()
        event.accept()
