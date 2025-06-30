#!/bin/bash

# 创建离线安装包脚本

echo "📦 创建离线安装包..."

# 创建离线包目录
mkdir -p offline_package
cd offline_package

# 下载Python依赖包
echo "📥 下载Python依赖包..."
pip download -r ../backend/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ -d python_packages

# 下载Node.js依赖包
echo "📥 下载Node.js依赖包..."
cd ../frontend
npm pack --registry https://registry.npmmirror.com
cd ..

# 复制项目文件
echo "📋 复制项目文件..."
cp -r backend offline_package/
cp -r frontend offline_package/
cp *.sh offline_package/
cp *.py offline_package/
cp *.md offline_package/
cp config.env.example offline_package/

# 创建离线安装脚本
cat > offline_package/install_offline.sh << 'EOF'
#!/bin/bash

echo "🔧 离线安装 SysScope AI..."

# 创建必要的目录
mkdir -p reports logs

# 安装Python依赖（离线）
echo "📦 安装Python依赖（离线模式）..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --no-index --find-links ../python_packages -r requirements.txt
cd ..

# 安装Node.js依赖（离线）
echo "📦 安装Node.js依赖（离线模式）..."
cd frontend
npm install --offline
cd ..

# 检查环境变量文件
if [ ! -f ".env" ]; then
    cp config.env.example .env
fi

echo "🎉 离线安装完成！"
EOF

chmod +x offline_package/install_offline.sh

# 创建压缩包
echo "🗜️  创建压缩包..."
tar -czf SysScope_AI_offline.tar.gz offline_package/

echo "✅ 离线安装包创建完成：SysScope_AI_offline.tar.gz"
echo ""
echo "📋 使用说明："
echo "1. 解压：tar -xzf SysScope_AI_offline.tar.gz"
echo "2. 进入目录：cd offline_package"
echo "3. 运行安装：./install_offline.sh" 