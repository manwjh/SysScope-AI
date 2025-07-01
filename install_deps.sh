#!/bin/bash

# SysScope AI 依赖安装脚本
# Dependency Installation Script for SysScope AI

echo "🔧 安装 SysScope AI 依赖..."
echo "Installing SysScope AI dependencies..."

# 检查 Python 版本
echo "🐍 检查 Python 版本..."
python3 --version

# 创建后端虚拟环境
echo "📦 创建后端虚拟环境..."
if [ -d "backend/venv" ]; then
    echo "删除现有虚拟环境..."
    rm -rf backend/venv
fi

python3 -m venv backend/venv

# 激活虚拟环境并安装后端依赖
echo "📥 安装后端依赖..."
source backend/venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 验证后端依赖安装
echo "✅ 验证后端依赖..."
python -c "import fastapi, uvicorn, openai, psutil; print('后端依赖安装成功！')"

# 安装前端依赖
echo "📥 安装前端依赖..."
cd frontend
npm install
cd ..

echo "🎉 所有依赖安装完成！"
echo "All dependencies installed successfully!"
echo ""
echo "💡 使用以下命令启动开发环境："
echo "Use the following command to start the development environment:"
echo "   ./start.sh" 