"""
Music Player Service
Handles music library scanning, playback control, and metadata extraction
"""
import os
from pathlib import Path
from typing import List, Dict, Optional
from mutagen import File as MutagenFile
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
import logging

logger = logging.getLogger(__name__)


class MusicPlayer:
    """Music player service for managing and playing audio files"""
    
    def __init__(self, music_dir: Path, supported_formats: List[str]):
        self.music_dir = music_dir
        self.supported_formats = supported_formats
        self.music_library: List[Dict] = []
        self.current_track_index: Optional[int] = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 70
        self.repeat_mode = 'none'  # none, one, all
        self.shuffle = False
        
    def scan_library(self) -> List[Dict]:
        """Scan music directory and build library"""
        self.music_library = []
        
        if not self.music_dir.exists():
            logger.warning(f"Music directory does not exist: {self.music_dir}")
            return self.music_library
        
        for file_path in self.music_dir.rglob('*'):
            if file_path.suffix.lower() in self.supported_formats:
                metadata = self._extract_metadata(file_path)
                if metadata:
                    self.music_library.append(metadata)
        
        logger.info(f"Scanned {len(self.music_library)} tracks")
        return self.music_library
    
    def _extract_metadata(self, file_path: Path) -> Optional[Dict]:
        """Extract metadata from audio file"""
        try:
            audio = MutagenFile(str(file_path), easy=True)
            if audio is None:
                return None
            
            # Extract common metadata
            title = self._get_tag(audio, 'title') or file_path.stem
            artist = self._get_tag(audio, 'artist') or 'Unknown Artist'
            album = self._get_tag(audio, 'album') or 'Unknown Album'
            genre = self._get_tag(audio, 'genre') or 'Unknown'
            
            # Get duration
            duration = int(audio.info.length) if hasattr(audio, 'info') else 0
            
            return {
                'id': len(self.music_library),
                'path': str(file_path),
                'filename': file_path.name,
                'title': title,
                'artist': artist,
                'album': album,
                'genre': genre,
                'duration': duration,
                'format': file_path.suffix[1:].upper()
            }
        except Exception as e:
            logger.error(f"Error extracting metadata from {file_path}: {e}")
            return None
    
    @staticmethod
    def _get_tag(audio, tag_name: str) -> str:
        """Safely get tag value"""
        try:
            value = audio.get(tag_name, [''])[0]
            return value if value else ''
        except (KeyError, IndexError, AttributeError):
            return ''
    
    def get_library(self) -> List[Dict]:
        """Get the music library"""
        return self.music_library
    
    def play_track(self, track_id: int) -> Dict:
        """Play a specific track"""
        if 0 <= track_id < len(self.music_library):
            self.current_track_index = track_id
            self.is_playing = True
            self.is_paused = False
            logger.info(f"Playing track: {self.music_library[track_id]['title']}")
            return self.get_current_track()
        return {}
    
    def pause(self) -> bool:
        """Pause current track"""
        if self.is_playing:
            self.is_paused = True
            logger.info("Playback paused")
            return True
        return False
    
    def resume(self) -> bool:
        """Resume current track"""
        if self.is_playing and self.is_paused:
            self.is_paused = False
            logger.info("Playback resumed")
            return True
        return False
    
    def stop(self) -> bool:
        """Stop playback"""
        self.is_playing = False
        self.is_paused = False
        self.current_track_index = None
        logger.info("Playback stopped")
        return True
    
    def next_track(self) -> Optional[Dict]:
        """Skip to next track"""
        if self.current_track_index is not None and self.music_library:
            if self.repeat_mode == 'one':
                return self.get_current_track()
            
            self.current_track_index = (self.current_track_index + 1) % len(self.music_library)
            self.is_playing = True
            self.is_paused = False
            logger.info(f"Next track: {self.music_library[self.current_track_index]['title']}")
            return self.get_current_track()
        return None
    
    def previous_track(self) -> Optional[Dict]:
        """Go to previous track"""
        if self.current_track_index is not None and self.music_library:
            self.current_track_index = (self.current_track_index - 1) % len(self.music_library)
            self.is_playing = True
            self.is_paused = False
            logger.info(f"Previous track: {self.music_library[self.current_track_index]['title']}")
            return self.get_current_track()
        return None
    
    def set_volume(self, volume: int) -> bool:
        """Set volume (0-100)"""
        if 0 <= volume <= 100:
            self.volume = volume
            logger.info(f"Volume set to {volume}")
            return True
        return False
    
    def toggle_shuffle(self) -> bool:
        """Toggle shuffle mode"""
        self.shuffle = not self.shuffle
        logger.info(f"Shuffle {'enabled' if self.shuffle else 'disabled'}")
        return self.shuffle
    
    def set_repeat_mode(self, mode: str) -> bool:
        """Set repeat mode"""
        if mode in ['none', 'one', 'all']:
            self.repeat_mode = mode
            logger.info(f"Repeat mode set to {mode}")
            return True
        return False
    
    def get_current_track(self) -> Optional[Dict]:
        """Get current track info"""
        if self.current_track_index is not None and 0 <= self.current_track_index < len(self.music_library):
            return self.music_library[self.current_track_index]
        return None
    
    def get_player_state(self) -> Dict:
        """Get current player state"""
        return {
            'is_playing': self.is_playing,
            'is_paused': self.is_paused,
            'volume': self.volume,
            'repeat_mode': self.repeat_mode,
            'shuffle': self.shuffle,
            'current_track': self.get_current_track(),
            'track_count': len(self.music_library)
        }
    
    def search_tracks(self, query: str) -> List[Dict]:
        """Search tracks by title, artist, or album"""
        query = query.lower()
        results = []
        for track in self.music_library:
            if (query in track['title'].lower() or 
                query in track['artist'].lower() or 
                query in track['album'].lower()):
                results.append(track)
        return results
