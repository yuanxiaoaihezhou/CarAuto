"""
Configuration module for CarAuto backend
"""
import os
from pathlib import Path

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    MUSIC_DIR = BASE_DIR / 'data' / 'music'
    CONFIG_DIR = BASE_DIR / 'data' / 'config'
    
    # Music player settings
    SUPPORTED_AUDIO_FORMATS = ['.mp3', '.wav', '.flac', '.m4a', '.ogg']
    
    # Voice recognition settings
    VOICE_LANGUAGE = 'zh-CN'  # Chinese
    VOICE_TIMEOUT = 5
    
    # Driver monitoring settings
    CAMERA_INDEX = 0
    FACE_DETECTION_CONFIDENCE = 0.5
    HAND_DETECTION_CONFIDENCE = 0.5
    
    # WebSocket settings
    SOCKETIO_CORS_ALLOWED_ORIGINS = "*"
    
    # Weather API (using free API)
    WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
    
    @classmethod
    def init_app(cls):
        """Initialize application directories"""
        cls.MUSIC_DIR.mkdir(parents=True, exist_ok=True)
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
