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
            logger.error(f"Error executing command: {e}")
            if self.tts:
                self.tts.speak("Command execution failed")
            return False
    
    def _execute_system(self, intent: str, params: Dict) -> bool:
        """Execute system commands"""
        if intent == 'shutdown':
            if self.tts:
                self.tts.speak("Shutting down system", blocking=True)
            
            if self.platform == 'Windows':
                os.system('shutdown /s /t 1')
            elif self.platform == 'Darwin':  # macOS
                os.system('sudo shutdown -h now')
            else:  # Linux
                os.system('shutdown -h now')
            return True
        
        elif intent == 'restart':
            if self.tts:
                self.tts.speak("Restarting system", blocking=True)
            
            if self.platform == 'Windows':
                os.system('shutdown /r /t 1')
            elif self.platform == 'Darwin':
                os.system('sudo shutdown -r now')
            else:
                os.system('shutdown -r now')
            return True
        
        elif intent == 'sleep':
            if self.tts:
                self.tts.speak("Putting system to sleep")
            
            if self.platform == 'Windows':
                os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            elif self.platform == 'Darwin':
                os.system('pmset sleepnow')
            else:
                os.system('systemctl suspend')
            return True
        
        elif intent == 'lock':
            if self.tts:
                self.tts.speak("Locking screen")
            
            if self.platform == 'Windows':
                os.system('rundll32.exe user32.dll,LockWorkStation')
            elif self.platform == 'Darwin':
                os.system('/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend')
            else:
                os.system('gnome-screensaver-command -l')
            return True
        
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
                        os.startfile(app_path)
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
                'chrome': ['chrome', 'google chrome', 'Google Chrome'],
                'firefox': ['firefox', 'Firefox'],
                'edge': ['msedge', 'Microsoft Edge'],
                'notepad': ['notepad', 'Notepad'],
                'calculator': ['calc', 'Calculator'],
                'terminal': ['cmd' if self.platform == 'Windows' else 'Terminal'],
            }
            
            for key, names in common_apps.items():
                if app_name in key or key in app_name:
                    try:
                        if self.platform == 'Windows':
                            subprocess.Popen(names[0])
                        elif self.platform == 'Darwin':
                            subprocess.Popen(['open', '-a', names[-1]])
                        else:
                            subprocess.Popen([names[0]])
                        
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
                        proc.kill()
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
        """Execute file operations"""
        filename = params.get('filename', '')
        
        if intent == 'open_file':
            if not filename:
                if self.tts:
                    self.tts.speak("Please specify filename")
                return False
            
            try:
                if self.platform == 'Windows':
                    os.startfile(filename)
                elif self.platform == 'Darwin':
                    subprocess.Popen(['open', filename])
                else:
                    subprocess.Popen(['xdg-open', filename])
                
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
                Path(filename).touch()
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
                Path(filename).unlink()
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
                if intent == 'volume_up':
                    # Use nircmd or similar tool
                    os.system(f'nircmd changesysvolume {amount * 655}')
                elif intent == 'volume_down':
                    os.system(f'nircmd changesysvolume -{amount * 655}')
                elif intent == 'mute':
                    os.system('nircmd mutesysvolume 1')
            
            elif self.platform == 'Darwin':
                current = subprocess.check_output(['osascript', '-e', 'output volume of (get volume settings)']).decode().strip()
                current_vol = int(current)
                
                if intent == 'volume_up':
                    new_vol = min(100, current_vol + amount)
                    os.system(f'osascript -e "set volume output volume {new_vol}"')
                elif intent == 'volume_down':
                    new_vol = max(0, current_vol - amount)
                    os.system(f'osascript -e "set volume output volume {new_vol}"')
                elif intent == 'mute':
                    os.system('osascript -e "set volume output muted true"')
            
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
