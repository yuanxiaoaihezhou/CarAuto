"""
Driver Monitoring Service
Handles face detection, gesture recognition, and eye tracking using MediaPipe
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, Optional, Tuple
import logging
import threading

logger = logging.getLogger(__name__)


class DriverMonitor:
    """Driver monitoring service using MediaPipe for face and hand detection"""
    
    def __init__(self, camera_index: int = 0, 
                 face_confidence: float = 0.5,
                 hand_confidence: float = 0.5):
        self.camera_index = camera_index
        self.face_confidence = face_confidence
        self.hand_confidence = hand_confidence
        
        # MediaPipe solutions
        self.mp_face_mesh = mp.solutions.face_mesh
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Initialize detectors
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=face_confidence,
            min_tracking_confidence=face_confidence
        )
        
        self.hands = self.mp_hands.Hands(
            max_num_hands=2,
            min_detection_confidence=hand_confidence,
            min_tracking_confidence=hand_confidence
        )
        
        # Camera
        self.cap = None
        self.is_monitoring = False
        self.monitor_thread = None
        
        # State tracking
        self.previous_head_position = None
        self.nod_counter = 0
        self.shake_counter = 0
        self.last_gesture = None
        self.eye_closure_counter = 0
        
    def start_monitoring(self) -> bool:
        """Start camera monitoring"""
        if self.is_monitoring:
            return True
        
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                logger.error("Failed to open camera")
                return False
            
            self.is_monitoring = True
            logger.info("Driver monitoring started")
            return True
        except Exception as e:
            logger.error(f"Error starting monitoring: {e}")
            return False
    
    def stop_monitoring(self) -> bool:
        """Stop camera monitoring"""
        self.is_monitoring = False
        if self.cap:
            self.cap.release()
            self.cap = None
        logger.info("Driver monitoring stopped")
        return True
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Capture a frame from camera"""
        if not self.cap or not self.cap.isOpened():
            return None
        
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        return frame
    
    def process_frame(self, frame: np.ndarray) -> Dict:
        """Process frame and detect gestures"""
        result = {
            'face_detected': False,
            'head_gesture': None,  # 'nod', 'shake', None
            'hand_gesture': None,  # 'thumbs_up', 'peace', 'palm', None
            'eye_state': 'open',   # 'open', 'closed', 'drowsy'
            'attention_score': 100
        }
        
        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process face
        face_results = self.face_mesh.process(rgb_frame)
        if face_results.multi_face_landmarks:
            result['face_detected'] = True
            landmarks = face_results.multi_face_landmarks[0]
            
            # Detect head gestures
            head_gesture = self._detect_head_gesture(landmarks, frame.shape)
            if head_gesture:
                result['head_gesture'] = head_gesture
            
            # Detect eye state
            eye_state = self._detect_eye_state(landmarks)
            result['eye_state'] = eye_state
            
            # Calculate attention score
            result['attention_score'] = self._calculate_attention_score(eye_state)
        
        # Process hands
        hand_results = self.hands.process(rgb_frame)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                gesture = self._detect_hand_gesture(hand_landmarks)
                if gesture:
                    result['hand_gesture'] = gesture
                    break
        
        return result
    
    def _detect_head_gesture(self, landmarks, frame_shape: Tuple) -> Optional[str]:
        """Detect head nodding and shaking"""
        # Get nose tip landmark (index 1)
        nose_tip = landmarks.landmark[1]
        current_position = (nose_tip.x, nose_tip.y)
        
        if self.previous_head_position is None:
            self.previous_head_position = current_position
            return None
        
        # Calculate movement
        dx = current_position[0] - self.previous_head_position[0]
        dy = current_position[1] - self.previous_head_position[1]
        
        gesture = None
        
        # Detect vertical movement (nod)
        if abs(dy) > 0.02:
            self.nod_counter += 1
            if self.nod_counter > 3:
                gesture = 'nod'
                self.nod_counter = 0
        
        # Detect horizontal movement (shake)
        if abs(dx) > 0.02:
            self.shake_counter += 1
            if self.shake_counter > 3:
                gesture = 'shake'
                self.shake_counter = 0
        
        self.previous_head_position = current_position
        return gesture
    
    def _detect_eye_state(self, landmarks) -> str:
        """Detect eye open/closed state"""
        # Left eye landmarks (indices for upper and lower eyelids)
        left_eye_top = landmarks.landmark[159]
        left_eye_bottom = landmarks.landmark[145]
        
        # Right eye landmarks
        right_eye_top = landmarks.landmark[386]
        right_eye_bottom = landmarks.landmark[374]
        
        # Calculate eye aspect ratio
        left_ear = abs(left_eye_top.y - left_eye_bottom.y)
        right_ear = abs(right_eye_top.y - right_eye_bottom.y)
        avg_ear = (left_ear + right_ear) / 2
        
        # Thresholds
        if avg_ear < 0.01:
            self.eye_closure_counter += 1
            if self.eye_closure_counter > 5:
                return 'closed'
            return 'drowsy'
        else:
            self.eye_closure_counter = max(0, self.eye_closure_counter - 1)
            return 'open'
    
    def _detect_hand_gesture(self, hand_landmarks) -> Optional[str]:
        """Detect hand gestures"""
        # Get key landmarks
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]
        
        thumb_ip = hand_landmarks.landmark[3]
        index_pip = hand_landmarks.landmark[6]
        middle_pip = hand_landmarks.landmark[10]
        ring_pip = hand_landmarks.landmark[14]
        pinky_pip = hand_landmarks.landmark[18]
        
        # Count extended fingers
        fingers_up = 0
        
        # Thumb
        if thumb_tip.x < thumb_ip.x:
            fingers_up += 1
        
        # Other fingers
        if index_tip.y < index_pip.y:
            fingers_up += 1
        if middle_tip.y < middle_pip.y:
            fingers_up += 1
        if ring_tip.y < ring_pip.y:
            fingers_up += 1
        if pinky_tip.y < pinky_pip.y:
            fingers_up += 1
        
        # Detect gestures based on finger count
        if fingers_up == 5:
            return 'palm'
        elif fingers_up == 2:
            return 'peace'
        elif fingers_up == 1:
            return 'thumbs_up'
        
        return None
    
    def _calculate_attention_score(self, eye_state: str) -> int:
        """Calculate driver attention score (0-100)"""
        if eye_state == 'closed':
            return 0
        elif eye_state == 'drowsy':
            return 50
        else:
            return 100
    
    def get_monitoring_status(self) -> Dict:
        """Get current monitoring status"""
        return {
            'is_monitoring': self.is_monitoring,
            'camera_available': self.cap is not None and self.cap.isOpened() if self.cap else False
        }
    
    def __del__(self):
        """Cleanup resources"""
        self.stop_monitoring()
