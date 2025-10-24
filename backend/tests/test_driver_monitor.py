"""
Tests for DriverMonitor module
"""
import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from app.driver_monitor import DriverMonitor


class TestDriverMonitor:
    """Test suite for DriverMonitor class"""
    
    @pytest.fixture
    def driver_monitor(self):
        """Create DriverMonitor instance"""
        return DriverMonitor(camera_index=0, face_confidence=0.5, hand_confidence=0.5)
    
    def test_initialization(self, driver_monitor):
        """Test DriverMonitor initialization"""
        assert driver_monitor.camera_index == 0
        assert driver_monitor.face_confidence == 0.5
        assert driver_monitor.hand_confidence == 0.5
        assert not driver_monitor.is_monitoring
        assert driver_monitor.cap is None
    
    def test_get_monitoring_status(self, driver_monitor):
        """Test getting monitoring status"""
        status = driver_monitor.get_monitoring_status()
        assert isinstance(status, dict)
        assert 'is_monitoring' in status
        assert 'camera_available' in status
    
    @patch('cv2.VideoCapture')
    def test_start_monitoring_success(self, mock_capture, driver_monitor):
        """Test starting monitoring successfully"""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_capture.return_value = mock_cap
        
        success = driver_monitor.start_monitoring()
        assert success
        assert driver_monitor.is_monitoring
    
    @patch('cv2.VideoCapture')
    def test_start_monitoring_failure(self, mock_capture, driver_monitor):
        """Test starting monitoring failure"""
        mock_cap = Mock()
        mock_cap.isOpened.return_value = False
        mock_capture.return_value = mock_cap
        
        success = driver_monitor.start_monitoring()
        assert not success
    
    def test_stop_monitoring(self, driver_monitor):
        """Test stopping monitoring"""
        driver_monitor.is_monitoring = True
        driver_monitor.cap = Mock()
        
        success = driver_monitor.stop_monitoring()
        assert success
        assert not driver_monitor.is_monitoring
    
    def test_calculate_attention_score(self, driver_monitor):
        """Test calculating attention score"""
        assert driver_monitor._calculate_attention_score('open') == 100
        assert driver_monitor._calculate_attention_score('drowsy') == 50
        assert driver_monitor._calculate_attention_score('closed') == 0
    
    def test_process_frame_no_face(self, driver_monitor):
        """Test processing frame without face"""
        # Create a dummy frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        result = driver_monitor.process_frame(frame)
        assert isinstance(result, dict)
        assert 'face_detected' in result
        assert 'head_gesture' in result
        assert 'hand_gesture' in result
        assert 'eye_state' in result
        assert 'attention_score' in result
