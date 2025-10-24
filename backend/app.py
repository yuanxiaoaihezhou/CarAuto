"""
Main Flask Application
CarAuto Backend Server
"""
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import logging
from pathlib import Path
import cv2
import base64
import numpy as np

from app.config import config, Config
from app.music_player import MusicPlayer
from app.driver_monitor import DriverMonitor
from app.voice_recognizer import VoiceRecognizer
from app.settings_manager import SettingsManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

# Load configuration
env = 'development'
app.config.from_object(config[env])
Config.init_app()

# Enable CORS
CORS(app)

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize services
music_player = MusicPlayer(Config.MUSIC_DIR, Config.SUPPORTED_AUDIO_FORMATS)
driver_monitor = DriverMonitor(
    Config.CAMERA_INDEX,
    Config.FACE_DETECTION_CONFIDENCE,
    Config.HAND_DETECTION_CONFIDENCE
)
voice_recognizer = VoiceRecognizer(Config.VOICE_LANGUAGE, Config.VOICE_TIMEOUT)
settings_manager = SettingsManager(Config.CONFIG_DIR)

# Scan music library on startup
music_player.scan_library()


# ============= Routes =============

@app.route('/')
def index():
    """Main application page"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'services': {
            'music_player': len(music_player.get_library()) > 0,
            'driver_monitor': driver_monitor.get_monitoring_status()['camera_available'],
            'voice_recognizer': voice_recognizer.get_status()['microphone_available']
        }
    })


# ============= Music API =============

@app.route('/api/music/library')
def get_music_library():
    """Get music library"""
    return jsonify(music_player.get_library())


@app.route('/api/music/scan', methods=['POST'])
def scan_music_library():
    """Rescan music library"""
    library = music_player.scan_library()
    return jsonify({
        'success': True,
        'track_count': len(library)
    })


@app.route('/api/music/play/<int:track_id>', methods=['POST'])
def play_track(track_id):
    """Play a track"""
    track = music_player.play_track(track_id)
    if track:
        socketio.emit('track_changed', track)
        return jsonify({'success': True, 'track': track})
    return jsonify({'success': False, 'error': 'Track not found'}), 404


@app.route('/api/music/pause', methods=['POST'])
def pause_track():
    """Pause current track"""
    success = music_player.pause()
    if success:
        socketio.emit('playback_paused')
    return jsonify({'success': success})


@app.route('/api/music/resume', methods=['POST'])
def resume_track():
    """Resume current track"""
    success = music_player.resume()
    if success:
        socketio.emit('playback_resumed')
    return jsonify({'success': success})


@app.route('/api/music/stop', methods=['POST'])
def stop_track():
    """Stop playback"""
    success = music_player.stop()
    if success:
        socketio.emit('playback_stopped')
    return jsonify({'success': success})


@app.route('/api/music/next', methods=['POST'])
def next_track():
    """Next track"""
    track = music_player.next_track()
    if track:
        socketio.emit('track_changed', track)
        return jsonify({'success': True, 'track': track})
    return jsonify({'success': False})


@app.route('/api/music/previous', methods=['POST'])
def previous_track():
    """Previous track"""
    track = music_player.previous_track()
    if track:
        socketio.emit('track_changed', track)
        return jsonify({'success': True, 'track': track})
    return jsonify({'success': False})


@app.route('/api/music/volume', methods=['POST'])
def set_volume():
    """Set volume"""
    data = request.get_json()
    volume = data.get('volume', 70)
    success = music_player.set_volume(volume)
    if success:
        socketio.emit('volume_changed', {'volume': volume})
    return jsonify({'success': success})


@app.route('/api/music/search')
def search_music():
    """Search music"""
    query = request.args.get('q', '')
    results = music_player.search_tracks(query)
    return jsonify(results)


@app.route('/api/music/state')
def get_player_state():
    """Get player state"""
    return jsonify(music_player.get_player_state())


# ============= Driver Monitor API =============

@app.route('/api/monitor/start', methods=['POST'])
def start_monitoring():
    """Start driver monitoring"""
    success = driver_monitor.start_monitoring()
    return jsonify({'success': success})


@app.route('/api/monitor/stop', methods=['POST'])
def stop_monitoring():
    """Stop driver monitoring"""
    success = driver_monitor.stop_monitoring()
    return jsonify({'success': success})


@app.route('/api/monitor/status')
def get_monitor_status():
    """Get monitoring status"""
    return jsonify(driver_monitor.get_monitoring_status())


# ============= Voice Recognition API =============

@app.route('/api/voice/start', methods=['POST'])
def start_voice_recognition():
    """Start voice recognition"""
    success = voice_recognizer.start_listening()
    return jsonify({'success': success})


@app.route('/api/voice/stop', methods=['POST'])
def stop_voice_recognition():
    """Stop voice recognition"""
    success = voice_recognizer.stop_listening()
    return jsonify({'success': success})


@app.route('/api/voice/status')
def get_voice_status():
    """Get voice recognition status"""
    return jsonify(voice_recognizer.get_status())


@app.route('/api/voice/recognize', methods=['POST'])
def recognize_voice():
    """Recognize voice once"""
    result = voice_recognizer.recognize_once()
    if result:
        return jsonify({'success': True, 'result': result})
    return jsonify({'success': False, 'error': 'Recognition failed'})


# ============= Settings API =============

@app.route('/api/settings')
def get_settings():
    """Get all settings"""
    return jsonify(settings_manager.get_settings())


@app.route('/api/settings/<category>')
def get_settings_category(category):
    """Get settings category"""
    return jsonify(settings_manager.get_category(category))


@app.route('/api/settings/<category>', methods=['PUT'])
def update_settings_category(category):
    """Update settings category"""
    data = request.get_json()
    success = settings_manager.update_category(category, data)
    if success:
        socketio.emit('settings_updated', {'category': category, 'values': data})
    return jsonify({'success': success})


@app.route('/api/settings/<category>/<key>', methods=['PUT'])
def update_setting(category, key):
    """Update a specific setting"""
    data = request.get_json()
    value = data.get('value')
    success = settings_manager.update_setting(category, key, value)
    if success:
        socketio.emit('setting_updated', {'category': category, 'key': key, 'value': value})
    return jsonify({'success': success})


@app.route('/api/settings/reset', methods=['POST'])
def reset_settings():
    """Reset settings to defaults"""
    data = request.get_json() or {}
    category = data.get('category')
    success = settings_manager.reset_to_defaults(category)
    return jsonify({'success': success})


# ============= WebSocket Events =============

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info('Client connected')
    emit('connected', {'status': 'success'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info('Client disconnected')


@socketio.on('request_monitor_frame')
def handle_monitor_frame_request():
    """Send driver monitor frame"""
    if driver_monitor.is_monitoring:
        frame = driver_monitor.get_frame()
        if frame is not None:
            # Process frame
            result = driver_monitor.process_frame(frame)
            
            # Encode frame to JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            
            emit('monitor_frame', {
                'image': frame_base64,
                'data': result
            })


@socketio.on('execute_voice_command')
def handle_voice_command(data):
    """Execute voice command"""
    command = data.get('command')
    logger.info(f"Executing voice command: {command}")
    
    # Handle music commands
    if command == 'play':
        if music_player.current_track_index is not None:
            music_player.resume()
        elif music_player.music_library:
            music_player.play_track(0)
    elif command == 'pause':
        music_player.pause()
    elif command == 'resume':
        music_player.resume()
    elif command == 'stop':
        music_player.stop()
    elif command == 'next':
        music_player.next_track()
    elif command == 'previous':
        music_player.previous_track()
    elif command == 'volume_up':
        current = music_player.volume
        music_player.set_volume(min(100, current + 10))
    elif command == 'volume_down':
        current = music_player.volume
        music_player.set_volume(max(0, current - 10))
    
    # Emit state update
    emit('player_state_updated', music_player.get_player_state(), broadcast=True)


if __name__ == '__main__':
    logger.info("Starting CarAuto Backend Server...")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
