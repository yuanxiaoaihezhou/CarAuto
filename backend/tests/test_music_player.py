"""
Tests for MusicPlayer module
"""
import pytest
from pathlib import Path
import tempfile
import shutil
from app.music_player import MusicPlayer


class TestMusicPlayer:
    """Test suite for MusicPlayer class"""
    
    @pytest.fixture
    def temp_music_dir(self):
        """Create temporary music directory"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def music_player(self, temp_music_dir):
        """Create MusicPlayer instance"""
        return MusicPlayer(temp_music_dir, ['.mp3', '.wav', '.flac'])
    
    def test_initialization(self, music_player, temp_music_dir):
        """Test MusicPlayer initialization"""
        assert music_player.music_dir == temp_music_dir
        assert music_player.current_track_index is None
        assert not music_player.is_playing
        assert not music_player.is_paused
        assert music_player.volume == 70
        assert music_player.repeat_mode == 'none'
        assert not music_player.shuffle
    
    def test_scan_empty_library(self, music_player):
        """Test scanning empty music directory"""
        library = music_player.scan_library()
        assert len(library) == 0
    
    def test_get_library(self, music_player):
        """Test getting music library"""
        library = music_player.get_library()
        assert isinstance(library, list)
    
    def test_set_volume_valid(self, music_player):
        """Test setting valid volume"""
        assert music_player.set_volume(50)
        assert music_player.volume == 50
    
    def test_set_volume_invalid(self, music_player):
        """Test setting invalid volume"""
        assert not music_player.set_volume(-10)
        assert not music_player.set_volume(150)
    
    def test_toggle_shuffle(self, music_player):
        """Test toggle shuffle mode"""
        initial = music_player.shuffle
        result = music_player.toggle_shuffle()
        assert result != initial
        assert music_player.shuffle != initial
    
    def test_set_repeat_mode(self, music_player):
        """Test setting repeat mode"""
        assert music_player.set_repeat_mode('one')
        assert music_player.repeat_mode == 'one'
        
        assert music_player.set_repeat_mode('all')
        assert music_player.repeat_mode == 'all'
        
        assert not music_player.set_repeat_mode('invalid')
    
    def test_stop_playback(self, music_player):
        """Test stopping playback"""
        music_player.is_playing = True
        music_player.current_track_index = 0
        
        assert music_player.stop()
        assert not music_player.is_playing
        assert not music_player.is_paused
        assert music_player.current_track_index is None
    
    def test_get_player_state(self, music_player):
        """Test getting player state"""
        state = music_player.get_player_state()
        assert isinstance(state, dict)
        assert 'is_playing' in state
        assert 'is_paused' in state
        assert 'volume' in state
        assert 'repeat_mode' in state
        assert 'shuffle' in state
        assert 'current_track' in state
        assert 'track_count' in state
    
    def test_search_tracks_empty(self, music_player):
        """Test searching in empty library"""
        results = music_player.search_tracks('test')
        assert len(results) == 0
