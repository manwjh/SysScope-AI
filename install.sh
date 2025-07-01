#!/bin/bash

# SysScope AI 安装脚本

echo "🔧 开始安装 SysScope AI..."

# 检查Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 未检测到Python3，请先安装Python3。"
    exit 1
fi

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "❌ Node.js 未安装，请先安装Node.js"
    exit 1
fi

# 检查并安装sysbench
echo "🔧 检查sysbench工具..."
if ! command -v sysbench &> /dev/null; then
    echo "📦 sysbench未安装，正在安装..."
    if command -v brew &> /dev/null; then
        echo "🍺 使用Homebrew安装sysbench..."
        brew install sysbench
    elif command -v apt-get &> /dev/null; then
        echo "📦 使用apt-get安装sysbench..."
        sudo apt-get update
        sudo apt-get install -y sysbench
    elif command -v yum &> /dev/null; then
        echo "📦 使用yum安装sysbench..."
        sudo yum install -y sysbench
    else
        echo "⚠️  无法自动安装sysbench，请手动安装："
        echo "   macOS: brew install sysbench"
        echo "   Ubuntu/Debian: sudo apt-get install sysbench"
        echo "   CentOS/RHEL: sudo yum install sysbench"
    fi
else
    echo "✅ sysbench已安装"
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
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo "⬆️  升级pip..."
pip install --upgrade pip

# 安装后端依赖
if [ -f "requirements.txt" ]; then
    echo "📦 安装后端依赖..."
    pip install -r requirements.txt
else
    echo "❌ 未找到requirements.txt"
    exit 1
fi

# 检查关键依赖是否安装
echo "🔍 检查关键依赖..."
pip show fastapi &> /dev/null
if [ $? -ne 0 ]; then
    echo "❌ fastapi未安装，依赖安装失败。"
    exit 1
fi

pip show numpy &> /dev/null
if [ $? -ne 0 ]; then
    echo "❌ numpy未安装，算力测试将失败。"
    exit 1
fi

pip show torch &> /dev/null
if [ $? -ne 0 ]; then
    echo "❌ torch未安装，算力测试将失败。"
    exit 1
fi

echo "✅ 所有依赖安装完成！"
echo "🚀 现在可以运行 ./start.sh 启动服务"

cd ..

# 安装前端依赖（使用国内镜像源）
echo "📦 安装前端依赖（使用淘宝镜像源加速）..."
cd frontend

# 设置npm镜像源
npm config set registry https://registry.npmmirror.com

# 安装依赖
npm install

cd ..

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "📝 创建环境变量文件..."
    # 优先使用 config.env，如果不存在则使用 config.env.example
    if [ -f "config.env" ]; then
        cp config.env .env
        echo "✅ 使用 config.env 创建环境变量文件"
    else
        cp config.env.example .env
        echo "✅ 使用 config.env.example 创建环境变量文件，请根据需要修改 .env 文件"
    fi
fi

echo "🎉 安装完成！"
echo ""
echo "📝 下一步："
echo "1. 运行 ./test_system.py 验证安装"
echo "2. 运行 ./start.sh 启动系统"
echo "3. 访问 http://localhost:3000 使用前端界面" 