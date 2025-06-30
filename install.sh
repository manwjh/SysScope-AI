#!/bin/bash

# LLM Computer Report 安装脚本

echo "🔧 开始安装 LLM Computer Report..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装，请先安装Python3"
    exit 1
fi

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js"
    exit 1
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p reports logs

# 安装后端依赖
echo "📦 安装后端依赖..."
cd backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    echo "🔧 创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 升级pip
echo "⬆️  升级pip..."
pip install --upgrade pip

# 安装依赖
echo "📦 安装Python依赖..."
pip install -r requirements.txt

cd ..

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "📝 创建环境变量文件..."
    cp config.env.example .env
    echo "✅ 环境变量文件已创建，请根据需要修改 .env 文件"
fi

echo "🎉 安装完成！"
echo ""
echo "📝 下一步："
echo "1. 运行 ./test_system.py 验证安装"
echo "2. 运行 ./start.sh 启动系统"
echo "3. 访问 http://localhost:3000 使用前端界面" 