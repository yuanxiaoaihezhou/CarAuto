"""
Tests for SettingsManager module
"""
import pytest
from pathlib import Path
import tempfile
import shutil
import json
from app.settings_manager import SettingsManager


class TestSettingsManager:
    """Test suite for SettingsManager class"""
    
    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary config directory"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def settings_manager(self, temp_config_dir):
        """Create SettingsManager instance"""
        return SettingsManager(temp_config_dir)
    
    def test_initialization(self, settings_manager, temp_config_dir):
        """Test SettingsManager initialization"""
        assert settings_manager.config_dir == temp_config_dir
        assert isinstance(settings_manager.settings, dict)
    
    def test_get_settings(self, settings_manager):
        """Test getting all settings"""
        settings = settings_manager.get_settings()
        assert isinstance(settings, dict)
        assert 'display' in settings
        assert 'audio' in settings
        assert 'voice' in settings
        assert 'system' in settings
    
    def test_get_category(self, settings_manager):
        """Test getting settings category"""
        display = settings_manager.get_category('display')
        assert isinstance(display, dict)
        assert 'theme' in display
        assert 'brightness' in display
    
    def test_get_setting(self, settings_manager):
        """Test getting specific setting"""
        theme = settings_manager.get_setting('display', 'theme')
        assert theme in ['dark', 'light']
    
    def test_update_setting(self, settings_manager):
        """Test updating a specific setting"""
        success = settings_manager.update_setting('display', 'theme', 'light')
        assert success
        assert settings_manager.get_setting('display', 'theme') == 'light'
    
    def test_update_category(self, settings_manager):
        """Test updating settings category"""
        new_values = {'theme': 'light', 'brightness': 90}
        success = settings_manager.update_category('display', new_values)
        assert success
        assert settings_manager.get_setting('display', 'theme') == 'light'
        assert settings_manager.get_setting('display', 'brightness') == 90
    
    def test_reset_to_defaults_category(self, settings_manager):
        """Test resetting a category to defaults"""
        settings_manager.update_setting('display', 'theme', 'light')
        success = settings_manager.reset_to_defaults('display')
        assert success
        
        default_theme = SettingsManager.DEFAULT_SETTINGS['display']['theme']
        assert settings_manager.get_setting('display', 'theme') == default_theme
    
    def test_reset_to_defaults_all(self, settings_manager):
        """Test resetting all settings to defaults"""
        settings_manager.update_setting('display', 'theme', 'light')
        settings_manager.update_setting('audio', 'volume', 50)
        
        success = settings_manager.reset_to_defaults()
        assert success
        
        default_theme = SettingsManager.DEFAULT_SETTINGS['display']['theme']
        default_volume = SettingsManager.DEFAULT_SETTINGS['audio']['volume']
        assert settings_manager.get_setting('display', 'theme') == default_theme
        assert settings_manager.get_setting('audio', 'volume') == default_volume
    
    def test_save_and_load_settings(self, settings_manager, temp_config_dir):
        """Test saving and loading settings"""
        settings_manager.update_setting('display', 'theme', 'light')
        settings_manager.save_settings()
        
        # Create new instance to load saved settings
        new_manager = SettingsManager(temp_config_dir)
        assert new_manager.get_setting('display', 'theme') == 'light'
    
    def test_settings_file_created(self, settings_manager, temp_config_dir):
        """Test that settings file is created"""
        settings_file = temp_config_dir / 'settings.json'
        assert settings_file.exists()
