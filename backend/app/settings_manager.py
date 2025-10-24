"""
Settings Service
Manages application settings and user preferences
"""
import json
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class SettingsManager:
    """Settings manager for user preferences and system configuration"""
    
    DEFAULT_SETTINGS = {
        'display': {
            'theme': 'dark',
            'brightness': 80,
            'orientation': 'landscape',
            'screen_timeout': 300  # seconds
        },
        'audio': {
            'volume': 70,
            'balance': 0,  # -100 (left) to 100 (right)
            'bass': 0,
            'treble': 0,
            'equalizer_preset': 'normal'
        },
        'voice': {
            'enabled': True,
            'language': 'zh-CN',
            'wake_word': '你好汽车',
            'voice_feedback': True
        },
        'driver_monitoring': {
            'enabled': True,
            'drowsiness_alert': True,
            'gesture_control': True,
            'privacy_mode': False
        },
        'navigation': {
            'map_style': 'standard',
            'traffic_enabled': True,
            'voice_guidance': True,
            'auto_zoom': True
        },
        'connectivity': {
            'bluetooth_enabled': True,
            'wifi_enabled': True,
            'auto_connect': True
        },
        'system': {
            'language': 'zh-CN',
            'units': 'metric',
            'time_format': '24h',
            'date_format': 'YYYY-MM-DD'
        },
        'locations': {
            'home': {'name': '家', 'address': '', 'lat': 0.0, 'lng': 0.0},
            'work': {'name': '公司', 'address': '', 'lat': 0.0, 'lng': 0.0}
        }
    }
    
    def __init__(self, config_dir: Path):
        self.config_dir = config_dir
        self.settings_file = config_dir / 'settings.json'
        self.settings = self.DEFAULT_SETTINGS.copy()
        self.load_settings()
    
    def load_settings(self) -> Dict:
        """Load settings from file"""
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self.settings = self._merge_settings(self.DEFAULT_SETTINGS, loaded_settings)
                logger.info("Settings loaded successfully")
            except Exception as e:
                logger.error(f"Error loading settings: {e}")
                self.settings = self.DEFAULT_SETTINGS.copy()
        else:
            logger.info("No settings file found, using defaults")
            self.save_settings()
        
        return self.settings
    
    def save_settings(self) -> bool:
        """Save settings to file"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            logger.info("Settings saved successfully")
            return True
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            return False
    
    def get_settings(self) -> Dict:
        """Get all settings"""
        return self.settings
    
    def get_category(self, category: str) -> Dict:
        """Get settings for a specific category"""
        return self.settings.get(category, {})
    
    def get_setting(self, category: str, key: str) -> Any:
        """Get a specific setting value"""
        return self.settings.get(category, {}).get(key)
    
    def update_setting(self, category: str, key: str, value: Any) -> bool:
        """Update a specific setting"""
        if category in self.settings:
            if key in self.settings[category]:
                self.settings[category][key] = value
                return self.save_settings()
        return False
    
    def update_category(self, category: str, values: Dict) -> bool:
        """Update multiple settings in a category"""
        if category in self.settings:
            self.settings[category].update(values)
            return self.save_settings()
        return False
    
    def reset_to_defaults(self, category: str = None) -> bool:
        """Reset settings to defaults"""
        if category:
            if category in self.DEFAULT_SETTINGS:
                self.settings[category] = self.DEFAULT_SETTINGS[category].copy()
                return self.save_settings()
            return False
        else:
            self.settings = self.DEFAULT_SETTINGS.copy()
            return self.save_settings()
    
    @staticmethod
    def _merge_settings(default: Dict, loaded: Dict) -> Dict:
        """Merge loaded settings with defaults"""
        merged = default.copy()
        for key, value in loaded.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key].update(value)
            else:
                merged[key] = value
        return merged
