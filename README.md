# CarAuto - 智能车机系统 🚗

一个现代、美观的类似 Android Auto 的车载信息娱乐系统，采用 Python 后端和 Web 前端开发。

![CarAuto](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ 功能特性

- 🎵 **本地音乐播放器** - 支持多种音频格式，自动识别元数据
- 👁️ **驾驶员姿态识别** - 实时监测点头、摇头、手势、眼动
- 🎤 **语音识别** - 中文语音指令控制
- ⚙️ **设置管理** - 完整的系统设置和用户偏好
- 🗺️ **导航界面** - 预留地图集成接口
- 📞 **电话功能** - 联系人和拨号界面
- 🌐 **现代 UI** - 横屏布局，Android Auto 风格

## 🚀 快速开始

### 环境要求

- Python 3.8+
- 摄像头（用于驾驶员监控）
- 麦克风（用于语音识别）
- 现代浏览器

### 安装

```bash
# 克隆仓库
git clone https://github.com/yuanxiaoaihezhou/CarAuto.git
cd CarAuto

# 安装依赖
cd backend
pip install -r requirements.txt

# 添加音乐文件
mkdir -p ../data/music
cp /path/to/your/music/*.mp3 ../data/music/

# 运行应用
python app.py
```

访问 `http://localhost:5000` 开始使用！

## 📖 文档

- [完整文档](docs/README.md)
- [API 文档](docs/API.md)
- [架构设计](docs/ARCHITECTURE.md)

## 🧪 测试

```bash
cd backend
pytest
pytest --cov=app --cov-report=html
```

## 📁 项目结构

```
CarAuto/
├── backend/          # Python 后端
│   ├── app/         # 应用模块
│   ├── tests/       # 单元测试
│   └── app.py       # 主程序
├── frontend/        # Web 前端
│   ├── static/      # CSS/JS
│   └── templates/   # HTML
├── data/            # 数据目录
│   ├── music/       # 音乐文件
│   └── config/      # 配置文件
└── docs/            # 文档
```

## 🛠️ 技术栈

**后端**: Flask, Flask-SocketIO, MediaPipe, OpenCV, Mutagen, SpeechRecognition

**前端**: HTML5, CSS3, JavaScript, Socket.IO

## 📝 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📧 联系

项目链接: [https://github.com/yuanxiaoaihezhou/CarAuto](https://github.com/yuanxiaoaihezhou/CarAuto)