#!/bin/bash

# SysScope AI 快速部署脚本

echo "🚀 SysScope AI 快速部署"
echo "请选择部署方式："
echo "1. 本地安装（使用国内镜像源）"
echo "2. Docker容器部署"
echo "3. 离线安装包部署"
echo "4. 创建离线安装包"
echo "5. 退出"

read -p "请输入选择 (1-5): " choice

case $choice in
    1)
        echo "🔧 开始本地安装..."
        ./install.sh
        ;;
    2)
        echo "🐳 开始Docker部署..."
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker未安装，请先安装Docker"
            exit 1
        fi
        
        if ! command -v docker-compose &> /dev/null; then
            echo "❌ Docker Compose未安装，请先安装Docker Compose"
            exit 1
        fi
        
        echo "📦 构建Docker镜像..."
        docker-compose build
        
        echo "🚀 启动服务..."
        docker-compose up -d
        
        echo "✅ Docker部署完成！"
        echo "📱 前端地址: http://localhost:3000"
        echo "🔧 后端地址: http://localhost:8000"
        echo "📝 查看日志: docker-compose logs -f"
        echo "🛑 停止服务: docker-compose down"
        ;;
    3)
        echo "📦 离线安装包部署..."
        if [ ! -f "SysScope_AI_offline.tar.gz" ]; then
            echo "❌ 离线安装包不存在，正在创建..."
            ./create_offline_package.sh
        fi
        
        echo "📦 解压离线安装包..."
        tar -xzf SysScope_AI_offline.tar.gz
        cd offline_package
        
        echo "🔧 开始离线安装..."
        ./install_offline.sh
        
        echo "✅ 离线安装完成！"
        ;;
    4)
        echo "📦 创建离线安装包..."
        ./create_offline_package.sh
        ;;
    5)
        echo "👋 退出部署"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac 