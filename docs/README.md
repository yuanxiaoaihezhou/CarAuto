# CarAuto - 智能车机系统

一个现代、美观的类似 Android Auto 的车载信息娱乐系统，采用 Python 后端和 Web 前端开发。

## 功能特性

### 核心功能

1. **本地音乐播放器** 🎵
   - 自动扫描和识别音乐文件
   - 支持 MP3、WAV、FLAC、M4A、OGG 格式
   - 元数据提取（标题、艺术家、专辑、时长）
   - 播放控制（播放、暂停、停止、上一首、下一首）
   - 音量控制
   - 音乐搜索功能
   - 循环和随机播放模式

2. **驾驶员姿态识别** 👁️
   - 使用 MediaPipe 进行实时面部检测
   - 头部姿态识别（点头、摇头）
   - 手势识别（竖大拇指、比V、手掌）
   - 眼睛状态监测（睁开、闭合、疲劳）
   - 注意力评分系统
   - 疲劳驾驶警告

3. **语音识别** 🎤
   - 基于 Google Speech Recognition 的中文语音识别
   - 支持音乐控制命令
   - 支持导航命令
   - 支持系统控制命令
   - 持续监听模式

4. **设置管理** ⚙️
   - 显示设置（主题、亮度）
   - 音频设置（音量、均衡器）
   - 语音设置（语言、启用/禁用）
   - 驾驶员监控设置
   - 系统设置（语言、时间格式）
   - 设置持久化存储

5. **附加功能**
   - 导航界面（预留地图集成接口）
   - 电话界面（联系人、拨号盘）
   - 实时时钟和日期显示
   - 天气信息显示
   - 系统状态监控
   - WebSocket 实时通信

## 技术栈

### 后端
- **Python 3.8+**
- **Flask** - Web 框架
- **Flask-SocketIO** - WebSocket 支持
- **MediaPipe** - 面部和手部检测
- **OpenCV** - 图像处理
- **Mutagen** - 音频元数据提取
- **SpeechRecognition** - 语音识别

### 前端
- **HTML5/CSS3/JavaScript**
- **Socket.IO Client** - 实时通信
- 响应式横屏布局设计
- 现代 UI/UX 设计

### 测试
- **pytest** - 单元测试框架
- **pytest-cov** - 代码覆盖率
- **pytest-mock** - 模拟对象

## 项目结构

```
CarAuto/
├── backend/                    # 后端代码
│   ├── app/                   # 应用模块
│   │   ├── __init__.py       # 应用初始化
│   │   ├── config.py         # 配置管理
│   │   ├── music_player.py   # 音乐播放器服务
│   │   ├── driver_monitor.py # 驾驶员监控服务
│   │   ├── voice_recognizer.py # 语音识别服务
│   │   └── settings_manager.py # 设置管理服务
│   ├── tests/                # 单元测试
│   │   ├── __init__.py
│   │   ├── test_music_player.py
│   │   ├── test_driver_monitor.py
│   │   └── test_settings_manager.py
│   ├── app.py                # 主应用入口
│   └── requirements.txt      # Python 依赖
├── frontend/                  # 前端代码
│   ├── static/               # 静态资源
│   │   ├── css/
│   │   │   └── style.css    # 样式表
│   │   └── js/
│   │       └── app.js       # 前端 JavaScript
│   └── templates/            # HTML 模板
│       └── index.html       # 主页面
├── data/                     # 数据目录
│   ├── music/               # 音乐文件目录
│   └── config/              # 配置文件目录
├── docs/                     # 文档
│   ├── README.md            # 本文档
│   ├── API.md               # API 文档
│   ├── ARCHITECTURE.md      # 架构设计文档
│   └── USER_GUIDE.md        # 用户指南
└── README.md                # 项目说明
```

## 安装和运行

### 环境要求

- Python 3.8 或更高版本
- 摄像头（用于驾驶员监控）
- 麦克风（用于语音识别）
- 现代浏览器（Chrome、Firefox、Edge）

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/yuanxiaoaihezhou/CarAuto.git
cd CarAuto
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
cd backend
pip install -r requirements.txt
```

4. 准备音乐文件：
```bash
# 将音乐文件复制到 data/music/ 目录
mkdir -p ../data/music
cp /path/to/your/music/*.mp3 ../data/music/
```

5. 运行应用：
```bash
python app.py
```

6. 访问应用：
打开浏览器访问 `http://localhost:5000`

### Docker 部署（可选）

```bash
# 构建镜像
docker build -t carauto .

# 运行容器
docker run -p 5000:5000 --device=/dev/video0 carauto
```

## 使用说明

### 音乐播放器

1. 将音乐文件放入 `data/music/` 目录
2. 点击"音乐"标签进入音乐播放器
3. 点击"扫描"按钮扫描音乐库
4. 点击歌曲即可播放
5. 使用控制按钮进行播放控制

### 驾驶员监控

1. 点击"监控"标签
2. 点击"启动监控"按钮
3. 允许浏览器访问摄像头
4. 系统将实时监测驾驶员状态
5. 查看检测结果和注意力评分

### 语音控制

1. 点击主页的"语音"按钮
2. 说出命令，例如：
   - "播放" - 开始播放
   - "暂停" - 暂停播放
   - "下一首" - 下一首歌
   - "音量增加" - 增加音量
   - "导航" - 打开导航
   - "设置" - 打开设置

### 设置

1. 点击"设置"标签
2. 调整各项设置
3. 设置自动保存
4. 可点击"恢复默认"重置所有设置

## 测试

运行单元测试：

```bash
cd backend
pytest
```

运行测试并查看覆盖率：

```bash
pytest --cov=app --cov-report=html
```

查看覆盖率报告：

```bash
open htmlcov/index.html  # Mac/Linux
# 或
start htmlcov/index.html  # Windows
```

## 语音命令列表

### 音乐控制
- 播放
- 暂停
- 继续
- 停止
- 下一首
- 上一首
- 音量增加
- 音量减少
- 静音

### 导航
- 导航
- 回家
- 去公司

### 系统
- 设置
- 天气
- 电话
- 主页
- 返回

### 驾驶员辅助
- 我累了
- 休息一下

## API 接口

详细的 API 文档请查看 [API.md](API.md)

### 主要接口

- `GET /api/music/library` - 获取音乐库
- `POST /api/music/play/<track_id>` - 播放音乐
- `POST /api/monitor/start` - 启动监控
- `POST /api/voice/start` - 启动语音识别
- `GET /api/settings` - 获取设置
- `PUT /api/settings/<category>` - 更新设置

## 扩展功能

### 地图集成

系统预留了地图集成接口，可以集成以下地图服务：
- 高德地图 API
- 百度地图 API
- Google Maps API

### 蓝牙连接

可以添加蓝牙功能实现：
- 蓝牙音乐播放
- 免提通话
- 手机通知同步

### OBD-II 集成

可以集成 OBD-II 接口获取：
- 车辆速度
- 发动机转速
- 油耗信息
- 故障诊断

## 故障排除

### 摄像头无法访问
- 检查摄像头权限
- 确认没有其他应用占用摄像头
- 在 config.py 中修改 CAMERA_INDEX

### 麦克风无法识别
- 检查麦克风权限
- 确认麦克风工作正常
- 检查网络连接（使用 Google Speech API）

### 音乐无法播放
- 确认音乐文件格式正确
- 检查文件权限
- 查看后端日志

## 贡献

欢迎贡献代码、报告问题或提出建议！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证。详见 LICENSE 文件。

## 联系方式

项目链接: [https://github.com/yuanxiaoaihezhou/CarAuto](https://github.com/yuanxiaoaihezhou/CarAuto)

## 致谢

- MediaPipe - Google 的优秀机器学习框架
- Flask - 轻量级 Web 框架
- Socket.IO - 实时通信库
- 所有开源贡献者
