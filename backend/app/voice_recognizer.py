"""
Voice Recognition Service
Handles speech-to-text for command recognition
"""
import speech_recognition as sr
import logging
from typing import Optional, Dict
import threading
import queue

logger = logging.getLogger(__name__)


class VoiceRecognizer:
    """Voice recognition service for command detection"""
    
    # Command patterns
    COMMANDS = {
        # Music commands
        '播放': 'play',
        '暂停': 'pause',
        '继续': 'resume',
        '停止': 'stop',
        '下一首': 'next',
        '上一首': 'previous',
        '音量增加': 'volume_up',
        '音量减少': 'volume_down',
        '静音': 'mute',
        
        # Navigation commands
        '导航': 'navigation',
        '回家': 'navigate_home',
        '去公司': 'navigate_work',
        
        # System commands
        '设置': 'settings',
        '天气': 'weather',
        '电话': 'phone',
        '主页': 'home',
        '返回': 'back',
        
        # Driver assistance
        '我累了': 'driver_tired',
        '休息一下': 'take_break',
    }
    
    def __init__(self, language: str = 'zh-CN', timeout: int = 5):
        self.language = language
        self.timeout = timeout
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.is_listening = False
        self.listen_thread = None
        self.command_queue = queue.Queue()
        
    def initialize(self) -> bool:
        """Initialize microphone"""
        try:
            self.microphone = sr.Microphone()
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("Voice recognizer initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize microphone: {e}")
            return False
    
    def start_listening(self) -> bool:
        """Start continuous listening in background"""
        if self.is_listening:
            return True
        
        if not self.microphone:
            if not self.initialize():
                return False
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        logger.info("Started continuous listening")
        return True
    
    def stop_listening(self) -> bool:
        """Stop continuous listening"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        logger.info("Stopped listening")
        return True
    
    def _listen_loop(self):
        """Background listening loop"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
                # Recognize in background
                threading.Thread(
                    target=self._recognize_audio,
                    args=(audio,),
                    daemon=True
                ).start()
                
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in listen loop: {e}")
                continue
    
    def _recognize_audio(self, audio):
        """Recognize audio and extract command"""
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info(f"Recognized: {text}")
            
            command = self._parse_command(text)
            if command:
                self.command_queue.put({
                    'text': text,
                    'command': command,
                    'timestamp': self._get_timestamp()
                })
        except sr.UnknownValueError:
            pass  # Could not understand audio
        except sr.RequestError as e:
            logger.error(f"Recognition service error: {e}")
    
    def _parse_command(self, text: str) -> Optional[str]:
        """Parse recognized text into command"""
        text_lower = text.lower()
        
        for keyword, command in self.COMMANDS.items():
            if keyword in text_lower:
                return command
        
        return None
    
    def get_command(self, block: bool = False, timeout: float = None) -> Optional[Dict]:
        """Get next command from queue"""
        try:
            return self.command_queue.get(block=block, timeout=timeout)
        except queue.Empty:
            return None
    
    def recognize_once(self) -> Optional[Dict]:
        """Recognize speech once (not continuous)"""
        if not self.microphone:
            if not self.initialize():
                return None
        
        try:
            with self.microphone as source:
                logger.info("Listening...")
                audio = self.recognizer.listen(source, timeout=self.timeout)
            
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info(f"Recognized: {text}")
            
            command = self._parse_command(text)
            
            return {
                'text': text,
                'command': command,
                'timestamp': self._get_timestamp()
            }
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Recognition service error: {e}")
            return None
    
    @staticmethod
    def _get_timestamp():
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_status(self) -> Dict:
        """Get recognizer status"""
        return {
            'is_listening': self.is_listening,
            'microphone_available': self.microphone is not None,
            'queue_size': self.command_queue.qsize()
        }
