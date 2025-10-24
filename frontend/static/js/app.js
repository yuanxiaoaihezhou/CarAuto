// CarAuto Frontend Application

// Initialize Socket.IO connection
const socket = io();

// State
let currentPage = 'home';
let isMonitoring = false;
let isVoiceListening = false;
let monitorInterval = null;
let playerState = {
    is_playing: false,
    is_paused: false,
    volume: 70,
    current_track: null
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
    setupSocketListeners();
    updateClock();
    setInterval(updateClock, 1000);
});

// Initialize application
function initializeApp() {
    console.log('Initializing CarAuto...');
    
    // Load initial data
    loadMusicLibrary();
    loadSettings();
    loadPlayerState();
    
    // Check system health
    fetch('/health')
        .then(res => res.json())
        .then(data => {
            console.log('System health:', data);
            showToast('系统启动成功');
        })
        .catch(err => console.error('Health check failed:', err));
}

// Setup event listeners
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', function() {
            const page = this.dataset.page;
            navigateTo(page);
        });
    });
}

// Setup Socket.IO listeners
function setupSocketListeners() {
    socket.on('connect', () => {
        console.log('Connected to server');
    });
    
    socket.on('disconnect', () => {
        console.log('Disconnected from server');
    });
    
    socket.on('track_changed', (track) => {
        updateNowPlaying(track);
        showToast(`正在播放: ${track.title}`);
    });
    
    socket.on('playback_paused', () => {
        updatePlayPauseButton(false);
    });
    
    socket.on('playback_resumed', () => {
        updatePlayPauseButton(true);
    });
    
    socket.on('playback_stopped', () => {
        updateNowPlaying(null);
    });
    
    socket.on('volume_changed', (data) => {
        document.getElementById('volumeSlider').value = data.volume;
        document.getElementById('volumeValue').textContent = data.volume;
    });
    
    socket.on('monitor_frame', (data) => {
        if (isMonitoring) {
            updateMonitorDisplay(data);
        }
    });
    
    socket.on('player_state_updated', (state) => {
        playerState = state;
        updatePlayerUI();
    });
}

// Navigation
function navigateTo(page) {
    // Update active nav item
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.page === page) {
            item.classList.add('active');
        }
    });
    
    // Update active page
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });
    document.getElementById(`${page}-page`).classList.add('active');
    
    currentPage = page;
}

// Clock
function updateClock() {
    const now = new Date();
    const time = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    const date = now.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' });
    
    document.getElementById('currentTime').textContent = time;
    document.getElementById('currentDate').textContent = date;
}

// Music Player Functions
function loadMusicLibrary() {
    fetch('/api/music/library')
        .then(res => res.json())
        .then(tracks => {
            displayMusicLibrary(tracks);
        })
        .catch(err => console.error('Error loading library:', err));
}

function displayMusicLibrary(tracks) {
    const trackList = document.getElementById('trackList');
    
    if (tracks.length === 0) {
        trackList.innerHTML = '<div class="empty-library">音乐库为空，请添加音乐文件到 data/music 目录</div>';
        return;
    }
    
    trackList.innerHTML = tracks.map((track, index) => `
        <div class="track-item" onclick="playTrack(${track.id})">
            <div class="track-number">${index + 1}</div>
            <div class="track-details">
                <div class="track-name">${track.title}</div>
                <div class="track-meta">${track.artist} - ${track.album}</div>
            </div>
            <div class="track-duration">${formatDuration(track.duration)}</div>
        </div>
    `).join('');
}

function playTrack(trackId) {
    fetch(`/api/music/play/${trackId}`, { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                playerState.is_playing = true;
                playerState.is_paused = false;
                updatePlayerUI();
            }
        })
        .catch(err => console.error('Error playing track:', err));
}

function togglePlayPause() {
    if (!playerState.is_playing) {
        // Start playing first track if none playing
        if (playerState.current_track === null) {
            playTrack(0);
        }
        return;
    }
    
    if (playerState.is_paused) {
        resumeTrack();
    } else {
        pauseTrack();
    }
}

function pauseTrack() {
    fetch('/api/music/pause', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                playerState.is_paused = true;
                updatePlayerUI();
            }
        });
}

function resumeTrack() {
    fetch('/api/music/resume', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                playerState.is_paused = false;
                updatePlayerUI();
            }
        });
}

function stopTrack() {
    fetch('/api/music/stop', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                playerState.is_playing = false;
                playerState.is_paused = false;
                playerState.current_track = null;
                updatePlayerUI();
            }
        });
}

function nextTrack() {
    fetch('/api/music/next', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                updatePlayerUI();
            }
        });
}

function previousTrack() {
    fetch('/api/music/previous', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                updatePlayerUI();
            }
        });
}

function setVolume(volume) {
    fetch('/api/music/volume', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ volume: parseInt(volume) })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            document.getElementById('volumeValue').textContent = volume;
        }
    });
}

function loadPlayerState() {
    fetch('/api/music/state')
        .then(res => res.json())
        .then(state => {
            playerState = state;
            updatePlayerUI();
        });
}

function updatePlayerUI() {
    // Update play/pause button
    const playPauseBtn = document.getElementById('playPauseBtn');
    if (playerState.is_playing && !playerState.is_paused) {
        playPauseBtn.textContent = '⏸️';
    } else {
        playPauseBtn.textContent = '▶️';
    }
    
    // Update now playing
    if (playerState.current_track) {
        updateNowPlaying(playerState.current_track);
    } else {
        updateNowPlaying(null);
    }
    
    // Update volume
    document.getElementById('volumeSlider').value = playerState.volume;
    document.getElementById('volumeValue').textContent = playerState.volume;
}

function updateNowPlaying(track) {
    if (track) {
        document.getElementById('trackTitle').textContent = track.title;
        document.getElementById('trackArtist').textContent = track.artist;
        document.getElementById('trackAlbum').textContent = track.album;
        document.getElementById('totalTime').textContent = formatDuration(track.duration);
        
        // Update home widget
        document.getElementById('homeNowPlaying').innerHTML = `
            <div class="track-name">${track.title}</div>
            <div class="track-meta">${track.artist}</div>
        `;
    } else {
        document.getElementById('trackTitle').textContent = '未播放';
        document.getElementById('trackArtist').textContent = '-';
        document.getElementById('trackAlbum').textContent = '-';
        document.getElementById('homeNowPlaying').innerHTML = '<div class="no-music">暂无播放</div>';
    }
}

function updatePlayPauseButton(playing) {
    const btn = document.getElementById('playPauseBtn');
    btn.textContent = playing ? '⏸️' : '▶️';
}

function searchMusic() {
    const query = document.getElementById('musicSearch').value;
    if (query.length === 0) {
        loadMusicLibrary();
        return;
    }
    
    fetch(`/api/music/search?q=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(tracks => {
            displayMusicLibrary(tracks);
        });
}

function scanLibrary() {
    showToast('正在扫描音乐库...');
    fetch('/api/music/scan', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            showToast(`扫描完成，找到 ${data.track_count} 首歌曲`);
            loadMusicLibrary();
        });
}

function formatDuration(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Driver Monitor Functions
function toggleMonitoring() {
    if (isMonitoring) {
        stopMonitoring();
    } else {
        startMonitoring();
    }
}

function startMonitoring() {
    fetch('/api/monitor/start', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                isMonitoring = true;
                document.getElementById('startMonitorBtn').textContent = '停止监控';
                showToast('驾驶员监控已启动');
                
                // Request frames regularly
                monitorInterval = setInterval(() => {
                    socket.emit('request_monitor_frame');
                }, 200); // 5 fps
            }
        });
}

function stopMonitoring() {
    fetch('/api/monitor/stop', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                isMonitoring = false;
                document.getElementById('startMonitorBtn').textContent = '启动监控';
                showToast('驾驶员监控已停止');
                
                if (monitorInterval) {
                    clearInterval(monitorInterval);
                    monitorInterval = null;
                }
            }
        });
}

function updateMonitorDisplay(data) {
    // Update camera feed
    document.getElementById('cameraFeed').src = 'data:image/jpeg;base64,' + data.image;
    
    // Update monitoring info
    const monitorData = data.data;
    document.getElementById('faceDetected').textContent = monitorData.face_detected ? '已检测' : '未检测';
    document.getElementById('headGesture').textContent = monitorData.head_gesture || '-';
    document.getElementById('handGesture').textContent = monitorData.hand_gesture || '-';
    document.getElementById('eyeState').textContent = 
        monitorData.eye_state === 'open' ? '睁开' :
        monitorData.eye_state === 'closed' ? '闭合' : '疲劳';
    document.getElementById('attentionScore').textContent = monitorData.attention_score + '%';
    
    // Update driver status in status bar
    const driverStatus = document.getElementById('driverStatus');
    if (monitorData.attention_score < 30) {
        driverStatus.className = 'driver-status danger';
        driverStatus.innerHTML = '<span class="status-icon">⚠️</span><span class="status-text">危险驾驶</span>';
    } else if (monitorData.attention_score < 70) {
        driverStatus.className = 'driver-status warning';
        driverStatus.innerHTML = '<span class="status-icon">⚠️</span><span class="status-text">疲劳驾驶</span>';
    } else {
        driverStatus.className = 'driver-status';
        driverStatus.innerHTML = '<span class="status-icon">👤</span><span class="status-text">正常驾驶</span>';
    }
}

// Voice Recognition Functions
function toggleVoiceRecognition() {
    if (isVoiceListening) {
        stopVoiceRecognition();
    } else {
        startVoiceRecognition();
    }
}

function startVoiceRecognition() {
    fetch('/api/voice/start', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                isVoiceListening = true;
                document.getElementById('voiceIndicator').classList.add('active');
                showToast('语音识别已启动');
            }
        });
}

function stopVoiceRecognition() {
    fetch('/api/voice/stop', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                isVoiceListening = false;
                document.getElementById('voiceIndicator').classList.remove('active');
                showToast('语音识别已停止');
            }
        });
}

// Settings Functions
function loadSettings() {
    fetch('/api/settings')
        .then(res => res.json())
        .then(settings => {
            // Apply settings to UI
            if (settings.display) {
                document.getElementById('themeSetting').value = settings.display.theme;
            }
            if (settings.voice) {
                document.getElementById('voiceEnabled').checked = settings.voice.enabled;
            }
            if (settings.audio) {
                document.getElementById('settingsVolume').value = settings.audio.volume;
            }
        });
}

function updateSetting(category, key, value) {
    fetch(`/api/settings/${category}/${key}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: value })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showToast('设置已更新');
        }
    });
}

function resetSettings() {
    if (confirm('确定要恢复默认设置吗？')) {
        fetch('/api/settings/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                showToast('设置已恢复默认');
                loadSettings();
            }
        });
    }
}

// Toast Notification
function showToast(message, duration = 3000) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, duration);
}
