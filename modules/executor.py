"""
Command Executor Module for EchoOS
Executes parsed commands with cross-platform support
Handles system, application, file, and web operations
"""

import os
import sys
import platform
import subprocess
import logging
import webbrowser
import psutil
from typing import Dict, Optional
from pathlib import Path
import re

logger = logging.getLogger(__name__)


class Executor:
    """Executes voice commands"""
    
    def __init__(self, tts=None, auth=None):
        """
        Initialize executor
        
        Args:
            tts: TTS instance for feedback
            auth: Authenticator instance
        """
        self.tts = tts
        self.auth = auth
        self.platform = platform.system()
        self.app_paths = self._load_app_paths()
        
        logger.info(f"Executor initialized for {self.platform}")
    
    def _load_app_paths(self) -> Dict:
        """Load application paths from config"""
        try:
            import json
            config_file = Path("config/apps.json")
            if config_file.exists():
                with open(config_file, 'r') as f:
                    data = json.load(f)
                    return {app['name'].lower(): app['path'] 
                           for app in data.get('apps', [])}
        except Exception as e:
            logger.error(f"Error loading app paths: {e}")
        return {}
    
    def _validate_filename(self, filename: str) -> bool:
        """
        Validate filename for security
        
        Args:
            filename: Filename to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not filename:
            return False
        
        # Check for directory traversal
        if '..' in filename or filename.startswith('/'):
            logger.warning(f"Invalid filename detected: {filename}")
            return False
        
        # Check for suspicious characters
        if any(char in filename for char in ['|', '&', ';', '`', '$', '(', ')']):
            logger.warning(f"Suspicious characters in filename: {filename}")
            return False
        
        return True
    
    def execute(self, command: Dict) -> bool:
        """
        Execute parsed command
        
        Args:
            command: Parsed command dictionary
            
        Returns:
            True if successful, False otherwise
        """
        if not command:
            return False
        
        category = command.get('category')
        intent = command.get('intent')
        params = command.get('parameters', {})
        
        logger.info(f"Executing: {category}.{intent}")
        
        try:
            # Route to appropriate handler
            if category == 'system':
                return self._execute_system(intent, params)
            elif category == 'application':
                return self._execute_application(intent, params)
            elif category == 'file':
                return self._execute_file(intent, params)
            elif category == 'web':
                return self._execute_web(intent, params)
            elif category == 'system_info':
                return self._execute_system_info(intent, params)
            elif category == 'volume':
                return self._execute_volume(intent, params)
            elif category == 'control':
                return self._execute_control(intent, params)
            else:
                logger.warning(f"Unknown category: {category}")
                if self.tts:
                    self.tts.speak("Unknown command category")
                return False
                
        except Exception as e:
            logger.error(f"Error executing command: {e}", exc_info=True)
            if self.tts:
                self.tts.speak("Command execution failed")
            return False
    
    def _execute_system(self, intent: str, params: Dict) -> bool:
        """Execute system commands with proper security"""
        if intent == 'shutdown':
            if self.tts:
                self.tts.speak("Shutting down system", blocking=True)
            
            try:
                if self.platform == 'Windows':
                    subprocess.run(['shutdown', '/s', '/t', '1'], check=False)
                elif self.platform == 'Darwin':  # macOS
                    # Note: Requires sudo privileges
                    subprocess.run(['osascript', '-e', 'tell app "System Events" to shut down'], check=False)
                else:  # Linux
                    subprocess.run(['systemctl', 'poweroff'], check=False)
                return True
            except Exception as e:
                logger.error(f"Shutdown failed: {e}")
                if self.tts:
                    self.tts.speak("Shutdown failed. May require administrator privileges")
                return False
        
        elif intent == 'restart':
            if self.tts:
                self.tts.speak("Restarting system", blocking=True)
            
            try:
                if self.platform == 'Windows':
                    subprocess.run(['shutdown', '/r', '/t', '1'], check=False)
                elif self.platform == 'Darwin':
                    subprocess.run(['osascript', '-e', 'tell app "System Events" to restart'], check=False)
                else:
                    subprocess.run(['systemctl', 'reboot'], check=False)
                return True
            except Exception as e:
                logger.error(f"Restart failed: {e}")
                if self.tts:
                    self.tts.speak("Restart failed")
                return False
        
        elif intent == 'sleep':
            if self.tts:
                self.tts.speak("Putting system to sleep")
            
            try:
                if self.platform == 'Windows':
                    subprocess.run(['rundll32.exe', 'powrprof.dll,SetSuspendState', '0', '1', '0'], check=False)
                elif self.platform == 'Darwin':
                    subprocess.run(['pmset', 'sleepnow'], check=False)
                else:
                    subprocess.run(['systemctl', 'suspend'], check=False)
                return True
            except Exception as e:
                logger.error(f"Sleep failed: {e}")
                if self.tts:
                    self.tts.speak("Sleep failed")
                return False
        
        elif intent == 'lock':
            if self.tts:
                self.tts.speak("Locking screen")
            
            try:
                if self.platform == 'Windows':
                    subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'], check=False)
                elif self.platform == 'Darwin':
                    subprocess.run(['/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession', '-suspend'], check=False)
                else:
                    # Try multiple lock commands for different desktop environments
                    for cmd in [['gnome-screensaver-command', '-l'], 
                               ['xdg-screensaver', 'lock'],
                               ['loginctl', 'lock-session']]:
                        try:
                            subprocess.run(cmd, check=False, timeout=2)
                            break
                        except:
                            continue
                return True
            except Exception as e:
                logger.error(f"Lock failed: {e}")
                if self.tts:
                    self.tts.speak("Lock failed")
                return False
        
        return False
    
    def _execute_application(self, intent: str, params: Dict) -> bool:
        """Execute application commands"""
        app_name = params.get('app_name', '').lower()
        
        if intent == 'open':
            if not app_name:
                if self.tts:
                    self.tts.speak("Please specify application name")
                return False
            
            # Try to find app in discovered apps
            if app_name in self.app_paths:
                app_path = self.app_paths[app_name]
                try:
                    if self.platform == 'Windows':
                        subprocess.Popen([app_path], shell=False)
                    elif self.platform == 'Darwin':
                        subprocess.Popen(['open', '-a', app_path])
                    else:
                        subprocess.Popen([app_path])
                    
                    if self.tts:
                        self.tts.speak(f"Opening {app_name}")
                    return True
                except Exception as e:
                    logger.error(f"Error opening {app_name}: {e}")
            
            # Try common applications
            common_apps = {
                'chrome': {'win': 'chrome', 'mac': 'Google Chrome', 'linux': 'google-chrome'},
                'firefox': {'win': 'firefox', 'mac': 'Firefox', 'linux': 'firefox'},
                'edge': {'win': 'msedge', 'mac': 'Microsoft Edge', 'linux': 'microsoft-edge'},
                'notepad': {'win': 'notepad', 'mac': 'TextEdit', 'linux': 'gedit'},
                'calculator': {'win': 'calc', 'mac': 'Calculator', 'linux': 'gnome-calculator'},
                'terminal': {'win': 'cmd', 'mac': 'Terminal', 'linux': 'gnome-terminal'},
            }
            
            for key, apps in common_apps.items():
                if app_name in key or key in app_name:
                    try:
                        if self.platform == 'Windows':
                            subprocess.Popen([apps['win']], shell=False)
                        elif self.platform == 'Darwin':
                            subprocess.Popen(['open', '-a', apps['mac']])
                        else:
                            subprocess.Popen([apps['linux']])
                        
                        if self.tts:
                            self.tts.speak(f"Opening {app_name}")
                        return True
                    except Exception as e:
                        logger.error(f"Error opening {app_name}: {e}")
            
            if self.tts:
                self.tts.speak(f"Could not find {app_name}")
            return False
        
        elif intent == 'close':
            if not app_name:
                if self.tts:
                    self.tts.speak("Please specify application name")
                return False
            
            # Find and kill process
            killed = False
            for proc in psutil.process_iter(['name']):
                try:
                    if app_name in proc.info['name'].lower():
                        proc.terminate()
                        killed = True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            if killed:
                if self.tts:
                    self.tts.speak(f"Closed {app_name}")
                return True
            else:
                if self.tts:
                    self.tts.speak(f"{app_name} is not running")
                return False
        
        return False
    
    def _execute_file(self, intent: str, params: Dict) -> bool:
        """Execute file operations with validation"""
        filename = params.get('filename', '')
        
        # Validate filename
        if not self._validate_filename(filename):
            if self.tts:
                self.tts.speak("Invalid filename")
            return False
        
        if intent == 'open_file':
            if not filename:
                if self.tts:
                    self.tts.speak("Please specify filename")
                return False
            
            try:
                file_path = Path(filename)
                if not file_path.exists():
                    if self.tts:
                        self.tts.speak("File not found")
                    return False
                
                if self.platform == 'Windows':
                    subprocess.Popen(['start', '', str(file_path)], shell=True)
                elif self.platform == 'Darwin':
                    subprocess.Popen(['open', str(file_path)])
                else:
                    subprocess.Popen(['xdg-open', str(file_path)])
                
                if self.tts:
                    self.tts.speak(f"Opening {filename}")
                return True
            except Exception as e:
                logger.error(f"Error opening file: {e}")
                if self.tts:
                    self.tts.speak("Could not open file")
                return False
        
        elif intent == 'create_file':
            if not filename:
                if self.tts:
                    self.tts.speak("Please specify filename")
                return False
            
            try:
                file_path = Path(filename)
                if file_path.exists():
                    if self.tts:
                        self.tts.speak("File already exists")
                    return False
                
                file_path.touch()
                if self.tts:
                    self.tts.speak(f"Created {filename}")
                return True
            except Exception as e:
                logger.error(f"Error creating file: {e}")
                if self.tts:
                    self.tts.speak("Could not create file")
                return False
        
        elif intent == 'delete_file':
            if not filename:
                if self.tts:
                    self.tts.speak("Please specify filename")
                return False
            
            try:
                file_path = Path(filename)
                if not file_path.exists():
                    if self.tts:
                        self.tts.speak("File not found")
                    return False
                
                file_path.unlink()
                if self.tts:
                    self.tts.speak(f"Deleted {filename}")
                return True
            except Exception as e:
                logger.error(f"Error deleting file: {e}")
                if self.tts:
                    self.tts.speak("Could not delete file")
                return False
        
        elif intent == 'list_files':
            try:
                files = [f.name for f in Path('.').iterdir() if f.is_file()]
                count = len(files)
                if self.tts:
                    self.tts.speak(f"Found {count} files")
                logger.info(f"Files: {', '.join(files[:10])}")
                return True
            except Exception as e:
                logger.error(f"Error listing files: {e}")
                return False
        
        return False
    
    def _execute_web(self, intent: str, params: Dict) -> bool:
        """Execute web operations"""
        if intent == 'open_website':
            url = params.get('url', '')
            if not url:
                if self.tts:
                    self.tts.speak("Please specify website")
                return False
            
            # Add protocol if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Add .com if no TLD
            if '.' not in url.split('/')[-1]:
                url = url + '.com'
            
            try:
                webbrowser.open(url)
                if self.tts:
                    self.tts.speak(f"Opening {url}")
                return True
            except Exception as e:
                logger.error(f"Error opening website: {e}")
                if self.tts:
                    self.tts.speak("Could not open website")
                return False
        
        elif intent == 'search_google':
            query = params.get('query', '')
            if not query:
                if self.tts:
                    self.tts.speak("Please specify search query")
                return False
            
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            try:
                webbrowser.open(url)
                if self.tts:
                    self.tts.speak(f"Searching for {query}")
                return True
            except Exception as e:
                logger.error(f"Error searching: {e}")
                return False
        
        elif intent == 'search_youtube':
            query = params.get('query', '')
            if not query:
                if self.tts:
                    self.tts.speak("Please specify search query")
                return False
            
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            try:
                webbrowser.open(url)
                if self.tts:
                    self.tts.speak(f"Searching YouTube for {query}")
                return True
            except Exception as e:
                logger.error(f"Error searching YouTube: {e}")
                return False
        
        return False
    
    def _execute_system_info(self, intent: str, params: Dict) -> bool:
        """Execute system information commands"""
        if intent == 'system_info':
            info = f"System: {platform.system()} {platform.release()}"
            if self.tts:
                self.tts.speak(info)
            logger.info(info)
            return True
        
        elif intent == 'battery':
            try:
                battery = psutil.sensors_battery()
                if battery:
                    percent = battery.percent
                    plugged = "plugged in" if battery.power_plugged else "on battery"
                    info = f"Battery at {percent} percent, {plugged}"
                    if self.tts:
                        self.tts.speak(info)
                    logger.info(info)
                    return True
                else:
                    if self.tts:
                        self.tts.speak("No battery detected")
                    return False
            except Exception as e:
                logger.error(f"Error getting battery info: {e}")
                return False
        
        elif intent == 'disk_space':
            try:
                disk = psutil.disk_usage('/')
                total_gb = disk.total / (1024**3)
                used_gb = disk.used / (1024**3)
                free_gb = disk.free / (1024**3)
                percent = disk.percent
                
                info = f"Disk: {used_gb:.1f} GB used of {total_gb:.1f} GB, {free_gb:.1f} GB free, {percent}% used"
                if self.tts:
                    self.tts.speak(f"Disk is {percent} percent full")
                logger.info(info)
                return True
            except Exception as e:
                logger.error(f"Error getting disk space: {e}")
                return False
        
        elif intent == 'memory':
            try:
                mem = psutil.virtual_memory()
                total_gb = mem.total / (1024**3)
                used_gb = mem.used / (1024**3)
                percent = mem.percent
                
                info = f"Memory: {used_gb:.1f} GB used of {total_gb:.1f} GB, {percent}% used"
                if self.tts:
                    self.tts.speak(f"Memory is {percent} percent used")
                logger.info(info)
                return True
            except Exception as e:
                logger.error(f"Error getting memory info: {e}")
                return False
        
        elif intent == 'cpu':
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                info = f"CPU usage: {cpu_percent}%"
                if self.tts:
                    self.tts.speak(f"CPU usage is {cpu_percent} percent")
                logger.info(info)
                return True
            except Exception as e:
                logger.error(f"Error getting CPU info: {e}")
                return False
        
        elif intent == 'network':
            try:
                # Get network interfaces
                addrs = psutil.net_if_addrs()
                connected = len(addrs) > 0
                
                if connected:
                    if self.tts:
                        self.tts.speak("Network is connected")
                    logger.info(f"Network interfaces: {list(addrs.keys())}")
                    return True
                else:
                    if self.tts:
                        self.tts.speak("No network connection")
                    return False
            except Exception as e:
                logger.error(f"Error getting network info: {e}")
                return False
        
        return False
    
    def _execute_volume(self, intent: str, params: Dict) -> bool:
        """Execute volume control commands"""
        amount = params.get('amount', 10)
        
        try:
            if self.platform == 'Windows':
                # Windows volume control using nircmd (if available)
                if intent == 'volume_up':
                    subprocess.run(['nircmd', 'changesysvolume', str(amount * 655)], check=False)
                elif intent == 'volume_down':
                    subprocess.run(['nircmd', 'changesysvolume', str(-amount * 655)], check=False)
                elif intent == 'mute':
                    subprocess.run(['nircmd', 'mutesysvolume', '1'], check=False)
            
            elif self.platform == 'Darwin':
                # macOS volume control
                try:
                    result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], 
                                          capture_output=True, text=True, check=True)
                    current_vol = int(result.stdout.strip())
                    
                    if intent == 'volume_up':
                        new_vol = min(100, current_vol + amount)
                        subprocess.run(['osascript', '-e', f'set volume output volume {new_vol}'], check=False)
                    elif intent == 'volume_down':
                        new_vol = max(0, current_vol - amount)
                        subprocess.run(['osascript', '-e', f'set volume output volume {new_vol}'], check=False)
                    elif intent == 'mute':
                        subprocess.run(['osascript', '-e', 'set volume output muted true'], check=False)
                except subprocess.CalledProcessError:
                    logger.error("Failed to control volume on macOS")
                    return False
            
            if self.tts:
                self.tts.speak(f"Volume {intent.replace('_', ' ')}")
            return True
            
        except Exception as e:
            logger.error(f"Error controlling volume: {e}")
            if self.tts:
                self.tts.speak("Volume control not available")
            return False
    
    def _execute_control(self, intent: str, params: Dict) -> bool:
        """Execute control commands"""
        if intent == 'stop_listening':
            if self.tts:
                self.tts.speak("Stopping")
            # This will be handled by the main window
            return True
        
        elif intent == 'wake_up':
            if self.tts:
                self.tts.speak("I'm listening")
            return True
        
        return False
