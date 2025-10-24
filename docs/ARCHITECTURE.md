# CarAuto 架构设计文档

## 系统概述

CarAuto 是一个现代化的车载信息娱乐系统，采用前后端分离的架构设计。

## 架构图

```
┌─────────────────────────────────────────────────────────┐
│                      前端层 (Frontend)                   │
│  ┌────────────────────────────────────────────────────┐ │
│  │  HTML/CSS/JavaScript + Socket.IO Client           │ │
│  │  - 用户界面                                         │ │
│  │  - 实时通信                                         │ │
│  │  - 状态管理                                         │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↕ HTTP/WebSocket
┌─────────────────────────────────────────────────────────┐
│                   应用层 (Application)                   │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Flask + Flask-SocketIO                           │ │
│  │  - RESTful API                                    │ │
│  │  - WebSocket 服务                                  │ │
│  │  - 路由控制                                        │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────┐
│                   业务逻辑层 (Business)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │  Music   │  │ Driver   │  │  Voice   │  │Settings ││
│  │  Player  │  │ Monitor  │  │Recognition│ │ Manager ││
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘│
└─────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────┐
│                 外部服务层 (External)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │ Mutagen  │  │MediaPipe │  │  Google  │  │  File   ││
│  │  Audio   │  │   CV     │  │  Speech  │  │ System  ││
│  │ Metadata │  │          │  │   API    │  │         ││
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘│
└─────────────────────────────────────────────────────────┘
```

## 组件设计

### 1. 前端组件

#### 1.1 页面结构
- **主页 (Home)**: 概览和快捷操作
- **音乐 (Music)**: 音乐播放器
- **导航 (Navigation)**: 地图和导航
- **电话 (Phone)**: 通话功能
- **监控 (Monitor)**: 驾驶员监控
- **设置 (Settings)**: 系统设置

#### 1.2 通信模块
- HTTP 客户端：处理 RESTful API 请求
- WebSocket 客户端：实时双向通信
- 状态管理：本地状态同步

### 2. 后端组件

#### 2.1 Flask 应用 (app.py)
- 路由定义
- 中间件配置
- 错误处理
- WebSocket 事件处理

#### 2.2 配置管理 (config.py)
- 环境配置
- 路径管理
- 常量定义

#### 2.3 音乐播放器 (music_player.py)
```python
class MusicPlayer:
    - scan_library()      # 扫描音乐库
    - play_track()        # 播放音乐
    - pause()             # 暂停
    - resume()            # 继续
    - stop()              # 停止
    - next_track()        # 下一首
    - previous_track()    # 上一首
    - set_volume()        # 设置音量
    - search_tracks()     # 搜索音乐
```

#### 2.4 驾驶员监控 (driver_monitor.py)
```python
class DriverMonitor:
    - start_monitoring()    # 启动监控
    - stop_monitoring()     # 停止监控
    - get_frame()          # 获取帧
    - process_frame()      # 处理帧
    - _detect_head_gesture()   # 检测头部姿态
    - _detect_eye_state()      # 检测眼睛状态
    - _detect_hand_gesture()   # 检测手势
    - _calculate_attention_score()  # 计算注意力
```

#### 2.5 语音识别 (voice_recognizer.py)
```python
class VoiceRecognizer:
    - initialize()         # 初始化
    - start_listening()    # 开始监听
    - stop_listening()     # 停止监听
    - recognize_once()     # 单次识别
    - _parse_command()     # 解析命令
```

#### 2.6 设置管理 (settings_manager.py)
```python
class SettingsManager:
    - load_settings()      # 加载设置
    - save_settings()      # 保存设置
    - get_settings()       # 获取设置
    - update_setting()     # 更新设置
    - reset_to_defaults()  # 重置
```

## 数据流

### 音乐播放流程
```
用户点击播放按钮
    ↓
前端发送 POST /api/music/play/{id}
    ↓
Flask 路由接收请求
    ↓
MusicPlayer.play_track(id)
    ↓
更新播放状态
    ↓
通过 WebSocket 广播 'track_changed' 事件
    ↓
前端更新 UI
```

### 驾驶员监控流程
```
用户启动监控
    ↓
前端发送 POST /api/monitor/start
    ↓
DriverMonitor.start_monitoring()
    ↓
打开摄像头
    ↓
前端定期发送 WebSocket 'request_monitor_frame'
    ↓
后端捕获和处理帧
    ↓
通过 WebSocket 发送 'monitor_frame' 事件
    ↓
前端显示图像和数据
```

### 语音识别流程
```
用户启动语音识别
    ↓
前端发送 POST /api/voice/start
    ↓
VoiceRecognizer.start_listening()
    ↓
后台线程持续监听
    ↓
识别到语音
    ↓
解析命令
    ↓
执行命令（如播放音乐）
    ↓
通过 WebSocket 广播状态更新
    ↓
前端更新 UI
```

## 技术选型

### 后端技术

#### Flask
- **优点**: 轻量级、灵活、易于扩展
- **用途**: Web 框架、API 服务

#### Flask-SocketIO
- **优点**: 实时双向通信、自动降级
- **用途**: WebSocket 支持

#### MediaPipe
- **优点**: 高性能、跨平台、预训练模型
- **用途**: 面部和手部检测

#### OpenCV
- **优点**: 功能强大、社区支持
- **用途**: 图像处理、视频捕获

#### Mutagen
- **优点**: 支持多种格式、易用
- **用途**: 音频元数据提取

#### SpeechRecognition
- **优点**: 支持多种引擎、简单易用
- **用途**: 语音转文本

### 前端技术

#### 原生 JavaScript
- **优点**: 无需构建、快速开发、轻量
- **用途**: 应用逻辑、DOM 操作

#### Socket.IO Client
- **优点**: 与后端集成、自动重连
- **用途**: 实时通信

#### CSS3
- **优点**: 现代化样式、动画支持
- **用途**: UI 设计

## 安全考虑

### 1. 输入验证
- 所有 API 输入进行验证
- 文件路径限制在指定目录

### 2. 数据隐私
- 摄像头数据不存储
- 语音数据不保存
- 本地处理敏感数据

### 3. 网络安全
- CORS 配置
- WebSocket 认证（待实现）
- HTTPS 支持（生产环境）

## 性能优化

### 1. 前端优化
- 事件节流和防抖
- 懒加载
- 本地缓存

### 2. 后端优化
- 异步处理
- 资源池管理
- 缓存机制

### 3. 通信优化
- WebSocket 减少轮询
- 压缩传输数据
- 批量更新

## 扩展性设计

### 1. 插件系统
- 预留插件接口
- 支持动态加载

### 2. 多语言支持
- i18n 国际化
- 语言包分离

### 3. 主题系统
- 可切换主题
- 自定义样式

### 4. 外部集成
- 地图 API 接口
- 蓝牙模块
- OBD-II 接口

## 测试策略

### 1. 单元测试
- 使用 pytest
- 覆盖核心业务逻辑
- 模拟外部依赖

### 2. 集成测试
- API 端点测试
- WebSocket 通信测试

### 3. 性能测试
- 响应时间测试
- 并发测试
- 资源使用测试

## 部署架构

### 开发环境
```
Python 虚拟环境
    ↓
Flask 开发服务器
    ↓
本地访问 (localhost:5000)
```

### 生产环境
```
Gunicorn + Gevent
    ↓
Nginx 反向代理
    ↓
HTTPS 访问
```

## 监控和日志

### 1. 日志系统
- 应用日志
- 错误日志
- 访问日志

### 2. 性能监控
- CPU 使用率
- 内存使用率
- 网络流量

### 3. 错误追踪
- 异常捕获
- 堆栈跟踪
- 错误报告

## 未来规划

### 短期 (1-3 个月)
- 完善地图导航功能
- 添加蓝牙支持
- 优化语音识别准确率

### 中期 (3-6 个月)
- OBD-II 集成
- 手机应用同步
- 云端服务集成

### 长期 (6-12 个月)
- AI 驾驶助手
- 个性化推荐
- 车队管理功能
