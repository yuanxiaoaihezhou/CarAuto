#!/bin/bash
# Quick start script for CarAuto

set -e

echo "=========================================="
echo "   CarAuto - 智能车机系统快速启动"
echo "=========================================="
echo

# Check Python version
echo "1. 检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python $python_version"

required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "   ✗ 需要 Python 3.8 或更高版本"
    exit 1
fi
echo "   ✓ Python 版本符合要求"
echo

# Check if in correct directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "✗ 请在 CarAuto 项目根目录运行此脚本"
    exit 1
fi

# Create data directories
echo "2. 创建数据目录..."
mkdir -p data/music
mkdir -p data/config
echo "   ✓ 数据目录已创建"
echo

# Check dependencies
echo "3. 检查依赖项..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "   ⚠️  Flask 未安装"
    echo "   正在安装依赖项..."
    cd backend
    pip install -r requirements.txt
    cd ..
    echo "   ✓ 依赖项安装完成"
else
    echo "   ✓ 依赖项已安装"
fi
echo

# Check for music files
echo "4. 检查音乐文件..."
music_count=$(find data/music -type f \( -iname "*.mp3" -o -iname "*.wav" -o -iname "*.flac" \) 2>/dev/null | wc -l)
if [ "$music_count" -eq 0 ]; then
    echo "   ⚠️  未找到音乐文件"
    echo "   提示: 将音乐文件复制到 data/music/ 目录"
    echo "   支持格式: MP3, WAV, FLAC, M4A, OGG"
else
    echo "   ✓ 找到 $music_count 个音乐文件"
fi
echo

# Start server
echo "5. 启动服务器..."
echo "=========================================="
echo
cd backend
echo "服务器启动中..."
echo "访问地址: http://localhost:5000"
echo
echo "提示:"
echo "  - 按 Ctrl+C 停止服务器"
echo "  - 将音乐文件放入 data/music/ 目录"
echo "  - 查看文档: docs/README.md"
echo
echo "=========================================="
echo

python3 app.py
