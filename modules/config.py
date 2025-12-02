"""
Configuration Manager for EchoOS
Handles loading and saving configuration files
"""

import json
import pathlib
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = pathlib.Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        
    def load_json(self, filename: str, default: Optional[Dict] = None) -> Dict[str, Any]:
        """Load JSON configuration file"""
        filepath = self.config_dir / filename
        
        try:
            if filepath.exists():
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                logger.warning(f"Config file not found: {filename}, using default")
                return default or {}
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            return default or {}
    
    def save_json(self, filename: str, data: Dict[str, Any]) -> bool:
        """Save data to JSON configuration file"""
        filepath = self.config_dir / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved configuration to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving {filename}: {e}")
            return False
    
    def get_commands(self) -> Dict[str, Any]:
        """Get command mappings"""
        return self.load_json("commands.json", {})
    
    def get_apps(self) -> Dict[str, Any]:
        """Get discovered applications"""
        return self.load_json("apps.json", {"apps": []})
    
    def save_apps(self, apps_data: Dict[str, Any]) -> bool:
        """Save discovered applications"""
        return self.save_json("apps.json", apps_data)
