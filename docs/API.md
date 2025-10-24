# CarAuto API 文档

## 概述

CarAuto 提供 RESTful API 和 WebSocket 接口用于前后端通信。

## 基础信息

- 基础URL: `http://localhost:5000`
- WebSocket URL: `ws://localhost:5000/socket.io`
- Content-Type: `application/json`

## API 端点

### 系统 API

#### 健康检查

```
GET /health
```

**响应示例：**
```json
{
  "status": "healthy",
  "services": {
    "music_player": true,
    "driver_monitor": true,
    "voice_recognizer": true
  }
}
```

---

### 音乐 API

#### 获取音乐库

```
GET /api/music/library
```

**响应示例：**
```json
[
  {
    "id": 0,
    "path": "/path/to/song.mp3",
    "filename": "song.mp3",
    "title": "Song Title",
    "artist": "Artist Name",
    "album": "Album Name",
    "genre": "Pop",
    "duration": 240,
    "format": "MP3"
  }
]
```

#### 扫描音乐库

```
POST /api/music/scan
```

**响应示例：**
```json
{
  "success": true,
  "track_count": 42
}
```

#### 播放音乐

```
POST /api/music/play/<track_id>
```

**参数：**
- `track_id` (int): 音乐ID

**响应示例：**
```json
{
  "success": true,
  "track": {
    "id": 0,
    "title": "Song Title",
    "artist": "Artist Name"
  }
}
```

#### 暂停播放

```
POST /api/music/pause
```

**响应示例：**
```json
{
  "success": true
}
```

#### 继续播放

```
POST /api/music/resume
```

**响应示例：**
```json
{
  "success": true
}
```

#### 停止播放

```
POST /api/music/stop
```

**响应示例：**
```json
{
  "success": true
}
```

#### 下一首

```
POST /api/music/next
```

**响应示例：**
```json
{
  "success": true,
  "track": { ... }
}
```

#### 上一首

```
POST /api/music/previous
```

**响应示例：**
```json
{
  "success": true,
  "track": { ... }
}
```

#### 设置音量

```
POST /api/music/volume
```

**请求体：**
```json
{
  "volume": 70
}
```

**响应示例：**
```json
{
  "success": true
}
```

#### 搜索音乐

```
GET /api/music/search?q=<query>
```

**参数：**
- `q` (string): 搜索关键词

**响应示例：**
```json
[
  {
    "id": 0,
    "title": "Matching Song",
    "artist": "Artist Name"
  }
]
```

#### 获取播放器状态

```
GET /api/music/state
```

**响应示例：**
```json
{
  "is_playing": true,
  "is_paused": false,
  "volume": 70,
  "repeat_mode": "none",
  "shuffle": false,
  "current_track": { ... },
  "track_count": 42
}
```

---

### 驾驶员监控 API

#### 启动监控

```
POST /api/monitor/start
```

**响应示例：**
```json
{
  "success": true
}
```

#### 停止监控

```
POST /api/monitor/stop
```

**响应示例：**
```json
{
  "success": true
}
```

#### 获取监控状态

```
GET /api/monitor/status
```

**响应示例：**
```json
{
  "is_monitoring": true,
  "camera_available": true
}
```

---

### 语音识别 API

#### 启动语音识别

```
POST /api/voice/start
```

**响应示例：**
```json
{
  "success": true
}
```

#### 停止语音识别

```
POST /api/voice/stop
```

**响应示例：**
```json
{
  "success": true
}
```

#### 获取语音识别状态

```
GET /api/voice/status
```

**响应示例：**
```json
{
  "is_listening": true,
  "microphone_available": true,
  "queue_size": 0
}
```

#### 单次语音识别

```
POST /api/voice/recognize
```

**响应示例：**
```json
{
  "success": true,
  "result": {
    "text": "播放音乐",
    "command": "play",
    "timestamp": "2025-10-24T10:23:34.493Z"
  }
}
```

---

### 设置 API

#### 获取所有设置

```
GET /api/settings
```

**响应示例：**
```json
{
  "display": {
    "theme": "dark",
    "brightness": 80,
    "orientation": "landscape",
    "screen_timeout": 300
  },
  "audio": {
    "volume": 70,
    "balance": 0,
    "bass": 0,
    "treble": 0,
    "equalizer_preset": "normal"
  },
  ...
}
```

#### 获取设置分类

```
GET /api/settings/<category>
```

**参数：**
- `category` (string): 设置分类（display, audio, voice, driver_monitoring, navigation, connectivity, system, locations）

**响应示例：**
```json
{
  "theme": "dark",
  "brightness": 80,
  "orientation": "landscape",
  "screen_timeout": 300
}
```

#### 更新设置分类

```
PUT /api/settings/<category>
```

**请求体：**
```json
{
  "theme": "light",
  "brightness": 90
}
```

**响应示例：**
```json
{
  "success": true
}
```

#### 更新单个设置

```
PUT /api/settings/<category>/<key>
```

**请求体：**
```json
{
  "value": "light"
}
```

**响应示例：**
```json
{
  "success": true
}
```

#### 重置设置

```
POST /api/settings/reset
```

**请求体（可选）：**
```json
{
  "category": "display"
}
```

**响应示例：**
```json
{
  "success": true
}
```

---

## WebSocket 事件

### 客户端到服务器

#### 请求监控帧

```javascript
socket.emit('request_monitor_frame');
```

#### 执行语音命令

```javascript
socket.emit('execute_voice_command', {
  command: 'play'
});
```

### 服务器到客户端

#### 连接成功

```javascript
socket.on('connected', (data) => {
  console.log(data.status);
});
```

#### 音乐轨道变更

```javascript
socket.on('track_changed', (track) => {
  console.log('Now playing:', track.title);
});
```

#### 播放暂停

```javascript
socket.on('playback_paused', () => {
  console.log('Playback paused');
});
```

#### 播放恢复

```javascript
socket.on('playback_resumed', () => {
  console.log('Playback resumed');
});
```

#### 播放停止

```javascript
socket.on('playback_stopped', () => {
  console.log('Playback stopped');
});
```

#### 音量变更

```javascript
socket.on('volume_changed', (data) => {
  console.log('Volume:', data.volume);
});
```

#### 监控帧

```javascript
socket.on('monitor_frame', (data) => {
  console.log('Frame data:', data.data);
  // data.image: base64 编码的图像
  // data.data: 检测结果
});
```

#### 播放器状态更新

```javascript
socket.on('player_state_updated', (state) => {
  console.log('Player state:', state);
});
```

#### 设置更新

```javascript
socket.on('settings_updated', (data) => {
  console.log('Settings updated:', data.category);
});
```

#### 单个设置更新

```javascript
socket.on('setting_updated', (data) => {
  console.log('Setting updated:', data.category, data.key, data.value);
});
```

---

## 错误响应

所有失败的请求将返回以下格式的错误响应：

```json
{
  "success": false,
  "error": "Error message"
}
```

常见 HTTP 状态码：
- 200: 成功
- 400: 请求错误
- 404: 未找到
- 500: 服务器内部错误

---

## 数据模型

### Track (音乐轨道)

```typescript
interface Track {
  id: number;
  path: string;
  filename: string;
  title: string;
  artist: string;
  album: string;
  genre: string;
  duration: number;  // 秒
  format: string;
}
```

### MonitorData (监控数据)

```typescript
interface MonitorData {
  face_detected: boolean;
  head_gesture: 'nod' | 'shake' | null;
  hand_gesture: 'thumbs_up' | 'peace' | 'palm' | null;
  eye_state: 'open' | 'closed' | 'drowsy';
  attention_score: number;  // 0-100
}
```

### PlayerState (播放器状态)

```typescript
interface PlayerState {
  is_playing: boolean;
  is_paused: boolean;
  volume: number;  // 0-100
  repeat_mode: 'none' | 'one' | 'all';
  shuffle: boolean;
  current_track: Track | null;
  track_count: number;
}
```

### VoiceResult (语音识别结果)

```typescript
interface VoiceResult {
  text: string;
  command: string | null;
  timestamp: string;  // ISO 8601
}
```

---

## 使用示例

### JavaScript 示例

```javascript
// 播放音乐
fetch('/api/music/play/0', { method: 'POST' })
  .then(res => res.json())
  .then(data => console.log('Playing:', data.track.title));

// 设置音量
fetch('/api/music/volume', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ volume: 80 })
})
.then(res => res.json())
.then(data => console.log('Volume set:', data.success));

// WebSocket 连接
const socket = io();
socket.on('track_changed', (track) => {
  console.log('Now playing:', track.title);
});
```

### Python 示例

```python
import requests

# 播放音乐
response = requests.post('http://localhost:5000/api/music/play/0')
data = response.json()
print(f"Playing: {data['track']['title']}")

# 设置音量
response = requests.post(
    'http://localhost:5000/api/music/volume',
    json={'volume': 80}
)
data = response.json()
print(f"Volume set: {data['success']}")
```

---

## 速率限制

当前版本没有速率限制，但建议：
- API 请求：每秒不超过 10 次
- WebSocket 消息：每秒不超过 30 次
- 监控帧请求：每秒不超过 10 帧

---

## 版本信息

- API Version: 1.0.0
- Last Updated: 2025-10-24
