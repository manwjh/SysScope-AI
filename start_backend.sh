#!/bin/bash

echo "🚀 启动 SysScope AI 后端服务..."

# 检查虚拟环境是否存在
if [ ! -d "backend/venv" ]; then
    echo "❌ 未找到虚拟环境，请先运行 ./install.sh 进行安装。"
    exit 1
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source backend/venv/bin/activate

# 检查关键依赖
echo "🔍 检查关键依赖..."
if ! python -c "import fastapi, numpy, torch" 2>/dev/null; then
    echo "❌ 关键依赖缺失，请重新运行 ./install.sh"
    exit 1
fi

# 启动后端服务
echo "🌐 启动后端服务..."
cd backend
python app.py 