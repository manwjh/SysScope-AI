# 使用官方Python镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 安装Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# 复制Python依赖文件
COPY backend/requirements.txt .

# 使用国内镜像源安装Python依赖
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt

# 复制后端代码
COPY backend/ ./backend/

# 复制前端代码
COPY frontend/ ./frontend/

# 设置npm镜像源并安装前端依赖
RUN cd frontend && \
    npm config set registry https://registry.npmmirror.com && \
    npm install && \
    npm run build

# 复制其他文件
COPY *.sh ./
COPY *.py ./
COPY config.env.example ./

# 创建必要的目录
RUN mkdir -p reports logs

# 暴露端口
EXPOSE 8000 3000

# 创建启动脚本
RUN echo '#!/bin/bash\n\
echo "🚀 启动 SysScope AI..."\n\
\n\
# 启动后端服务\n\
cd backend\n\
python app.py &\n\
BACKEND_PID=$!\n\
cd ..\n\
\n\
# 等待后端启动\n\
sleep 5\n\
\n\
# 启动前端服务\n\
cd frontend\n\
npm start &\n\
FRONTEND_PID=$!\n\
cd ..\n\
\n\
echo "🎉 服务启动完成！"\n\
echo "📱 前端地址: http://localhost:3000"\n\
echo "🔧 后端地址: http://localhost:8000"\n\
\n\
# 等待进程\n\
wait' > /app/start_docker.sh && chmod +x /app/start_docker.sh

# 设置启动命令
CMD ["/app/start_docker.sh"] 