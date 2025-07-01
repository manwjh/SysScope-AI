#!/bin/bash

# SysScope AI 启动脚本
# SysScope AI Startup Script

# 显示使用说明
show_usage() {
    echo "🚀 SysScope AI 启动脚本"
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "选项 (Options):"
    echo "  --clean, -c    清理并重新安装所有依赖"
    echo "  --help, -h     显示此帮助信息"
    echo ""
    echo "示例 (Examples):"
    echo "  $0             正常启动（智能检测依赖）"
    echo "  $0 --clean     清理并重新安装所有依赖"
    echo ""
}

# 检查帮助参数
if [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    show_usage
    exit 0
fi

echo "🚀 启动 SysScope AI 系统..."
echo "Starting SysScope AI System..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 全局变量存储进程ID
BACKEND_PID=""
FRONTEND_PID=""
CHILD_PIDS=()

# 清理函数
cleanup() {
    echo -e "\n${YELLOW}🛑 正在停止所有服务...${NC}"
    
    # 停止后端服务
    if [ -n "$BACKEND_PID" ]; then
        echo -e "${BLUE}停止后端服务 (PID: $BACKEND_PID)...${NC}"
        kill -TERM $BACKEND_PID 2>/dev/null
        sleep 2
        # 如果进程仍然存在，强制杀死
        if kill -0 $BACKEND_PID 2>/dev/null; then
            echo -e "${YELLOW}强制停止后端服务...${NC}"
            kill -9 $BACKEND_PID 2>/dev/null
        fi
    fi
    
    # 停止前端服务
    if [ -n "$FRONTEND_PID" ]; then
        echo -e "${BLUE}停止前端服务 (PID: $FRONTEND_PID)...${NC}"
        kill -TERM $FRONTEND_PID 2>/dev/null
        sleep 2
        # 如果进程仍然存在，强制杀死
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            echo -e "${YELLOW}强制停止前端服务...${NC}"
            kill -9 $FRONTEND_PID 2>/dev/null
        fi
    fi
    
    # 停止所有子进程
    for pid in "${CHILD_PIDS[@]}"; do
        if [ -n "$pid" ] && kill -0 $pid 2>/dev/null; then
            echo -e "${BLUE}停止子进程 (PID: $pid)...${NC}"
            kill -TERM $pid 2>/dev/null
            sleep 1
            if kill -0 $pid 2>/dev/null; then
                kill -9 $pid 2>/dev/null
            fi
        fi
    done
    
    # 清理可能的残留进程
    echo -e "${BLUE}清理残留进程...${NC}"
    pkill -f "python.*app.py" 2>/dev/null
    pkill -f "node.*start" 2>/dev/null
    pkill -f "uvicorn.*app:app" 2>/dev/null
    
    echo -e "${GREEN}✅ 所有服务已停止${NC}"
    exit 0
}

# 注册信号处理器
trap cleanup INT TERM EXIT

# 检查并释放端口
check_and_free_port() {
    local port=$1
    local service_name=$2
    
    echo -e "${BLUE}检查${service_name}端口 ${port}...${NC}"
    PID=$(lsof -ti tcp:$port 2>/dev/null)
    if [ -n "$PID" ]; then
        echo -e "${YELLOW}⚠️  端口${port}已被进程${PID}占用，正在释放...${NC}"
        kill -TERM $PID 2>/dev/null
        sleep 3
        # 如果进程仍然存在，强制杀死
        if kill -0 $PID 2>/dev/null; then
            kill -9 $PID 2>/dev/null
            sleep 1
        fi
        echo -e "${GREEN}✅ 端口${port}已释放${NC}"
    else
        echo -e "${GREEN}✅ 端口${port}可用${NC}"
    fi
}

# 检查环境
check_environment() {
    echo -e "${BLUE}检查运行环境...${NC}"
    
    # 检查Python环境
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python3 未安装，请先安装Python3${NC}"
        exit 1
    fi
    
    # 检查Node.js环境
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js 未安装，请先安装Node.js${NC}"
        exit 1
    fi
    
    # 检查npm
    if ! command -v npm &> /dev/null; then
        echo -e "${RED}❌ npm 未安装，请先安装npm${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ 环境检查通过${NC}"
}

# 创建必要目录
create_directories() {
    echo -e "${BLUE}创建必要目录...${NC}"
    mkdir -p reports logs backend/reports
    echo -e "${GREEN}✅ 目录创建完成${NC}"
}

# 设置环境变量
setup_environment() {
    echo -e "${BLUE}设置环境变量...${NC}"
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}📝 创建环境变量文件...${NC}"
        # 优先使用 config.env，如果不存在则使用 config.env.example
        if [ -f "config.env" ]; then
            cp config.env .env
            echo -e "${GREEN}✅ 使用 config.env 创建环境变量文件${NC}"
        else
            cp config.env.example .env
            echo -e "${GREEN}✅ 使用 config.env.example 创建环境变量文件，请根据需要修改 .env 文件${NC}"
        fi
    else
        echo -e "${GREEN}✅ 环境变量文件已存在${NC}"
    fi
}

# 安装后端依赖
install_backend_deps() {
    echo -e "${BLUE}安装后端依赖...${NC}"
    cd backend
    
    # 检查是否需要清理和重新安装
    NEED_CLEAN_INSTALL=false
    
    # 检查命令行参数
    if [[ "$*" == *"--clean"* ]] || [[ "$*" == *"-c"* ]]; then
        NEED_CLEAN_INSTALL=true
        echo -e "${YELLOW}检测到 --clean 参数，将清理并重新安装依赖${NC}"
    fi
    
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}🔧 创建Python虚拟环境...${NC}"
        python3 -m venv venv
        NEED_CLEAN_INSTALL=true
    fi
    
    source venv/bin/activate
    
    # 检查 requirements.txt 是否被修改
    if [ -f "requirements.txt" ]; then
        if [ ! -f "venv/.requirements.txt" ] || [ "requirements.txt" -nt "venv/.requirements.txt" ]; then
            NEED_CLEAN_INSTALL=true
            echo -e "${YELLOW}检测到 requirements.txt 已更新，需要重新安装依赖${NC}"
        fi
    fi
    
    # 如果需要清理安装
    if [ "$NEED_CLEAN_INSTALL" = true ]; then
        # 升级pip
        pip install --upgrade pip
        
        # 安装依赖
        if [ -f "requirements.txt" ]; then
            pip install -r requirements.txt
            # 记录 requirements.txt 的时间戳
            cp requirements.txt venv/.requirements.txt
        else
            echo -e "${YELLOW}⚠️  requirements.txt 不存在，安装基础依赖...${NC}"
            pip install fastapi uvicorn python-dotenv pydantic requests
        fi
    else
        echo -e "${GREEN}✅ 后端依赖已是最新，跳过安装${NC}"
    fi
    
    cd ..
    echo -e "${GREEN}✅ 后端依赖安装完成${NC}"
}

# 安装前端依赖
install_frontend_deps() {
    echo -e "${BLUE}安装前端依赖...${NC}"
    cd frontend
    
    # 检查是否需要清理和重新安装
    NEED_CLEAN_INSTALL=false
    
    # 检查命令行参数
    if [[ "$*" == *"--clean"* ]] || [[ "$*" == *"-c"* ]]; then
        NEED_CLEAN_INSTALL=true
        echo -e "${YELLOW}检测到 --clean 参数，将清理并重新安装依赖${NC}"
    fi
    
    # 检查 package.json 是否被修改
    if [ -f "package.json" ] && [ -f "package-lock.json" ]; then
        if [ "$package.json" -nt "package-lock.json" ]; then
            NEED_CLEAN_INSTALL=true
            echo -e "${YELLOW}检测到 package.json 已更新，需要重新安装依赖${NC}"
        fi
    fi
    
    # 检查 node_modules 是否存在且完整
    if [ -d "node_modules" ]; then
        if [ ! -f "node_modules/.package-lock.json" ] || [ "package-lock.json" -nt "node_modules/.package-lock.json" ]; then
            NEED_CLEAN_INSTALL=true
            echo -e "${YELLOW}检测到 package-lock.json 已更新，需要重新安装依赖${NC}"
        fi
    else
        NEED_CLEAN_INSTALL=true
        echo -e "${YELLOW}node_modules 不存在，需要安装依赖${NC}"
    fi
    
    # 如果需要清理安装
    if [ "$NEED_CLEAN_INSTALL" = true ]; then
        if [ -d "node_modules" ]; then
            echo -e "${YELLOW}清理旧的node_modules...${NC}"
            # 使用更快的删除方法
            if command -v rsync &> /dev/null; then
                # 使用 rsync 快速清空目录（比 rm -rf 更快）
                rsync -a --delete /dev/null/ node_modules/
                rmdir node_modules
            else
                # 使用 rm -rf 的优化版本
                rm -rf node_modules
            fi
            rm -f package-lock.json
        fi
        
        # 安装依赖
        echo -e "${BLUE}安装前端依赖...${NC}"
        npm install
    else
        echo -e "${GREEN}✅ 前端依赖已是最新，跳过安装${NC}"
    fi
    
    cd ..
    echo -e "${GREEN}✅ 前端依赖安装完成${NC}"
}

# 启动后端服务
start_backend() {
    echo -e "${BLUE}启动后端服务...${NC}"
    cd backend
    source venv/bin/activate
    
    # 设置环境变量文件路径
    export ENV_FILE="../.env"
    
    # 使用nohup启动后端，并记录PID
    nohup python app.py > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../logs/backend.pid
    CHILD_PIDS+=($BACKEND_PID)
    cd ..
    
    # 等待后端启动
    echo -e "${YELLOW}⏳ 等待后端服务启动...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:8000/ > /dev/null 2>&1; then
            echo -e "${GREEN}✅ 后端服务启动成功 (PID: $BACKEND_PID)${NC}"
            return 0
        fi
        sleep 1
    done
    
    echo -e "${RED}❌ 后端服务启动失败${NC}"
    return 1
}

# 启动前端服务
start_frontend() {
    echo -e "${BLUE}启动前端服务...${NC}"
    cd frontend
    
    # 设置环境变量
    export BROWSER=none  # 不自动打开浏览器
    
    # 使用nohup启动前端，并记录PID
    nohup npm start > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../logs/frontend.pid
    CHILD_PIDS+=($FRONTEND_PID)
    cd ..
    
    # 等待前端启动
    echo -e "${YELLOW}⏳ 等待前端服务启动...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:3000 > /dev/null 2>&1; then
            echo -e "${GREEN}✅ 前端服务启动成功 (PID: $FRONTEND_PID)${NC}"
            return 0
        fi
        sleep 1
    done
    
    echo -e "${RED}❌ 前端服务启动失败${NC}"
    return 1
}

# 主函数
main() {
    # 检查并释放端口
    check_and_free_port 8000 "后端"
    check_and_free_port 3000 "前端"
    
    # 检查环境
    check_environment
    
    # 创建目录
    create_directories
    
    # 设置环境变量
    setup_environment
    
    # 安装依赖（传递所有命令行参数）
    install_backend_deps "$@"
    install_frontend_deps "$@"
    
    # 启动服务
    if start_backend; then
        if start_frontend; then
            echo ""
            echo -e "${GREEN}🎉 SysScope AI 启动完成！${NC}"
            echo ""
            echo -e "${BLUE}📱 前端地址: ${GREEN}http://localhost:3000${NC}"
            echo -e "${BLUE}🔧 后端地址: ${GREEN}http://localhost:8000${NC}"
            echo -e "${BLUE}📚 API文档: ${GREEN}http://localhost:8000/docs${NC}"
            echo ""
            echo -e "${YELLOW}按 Ctrl+C 停止服务${NC}"
            echo -e "${BLUE}日志文件位置:${NC}"
            echo -e "  后端: ${GREEN}logs/backend.log${NC}"
            echo -e "  前端: ${GREEN}logs/frontend.log${NC}"
            echo ""
            
            # 等待用户中断或进程结束
            while true; do
                # 检查进程是否还在运行
                if [ -n "$BACKEND_PID" ] && ! kill -0 $BACKEND_PID 2>/dev/null; then
                    echo -e "${RED}❌ 后端服务意外停止${NC}"
                    break
                fi
                if [ -n "$FRONTEND_PID" ] && ! kill -0 $FRONTEND_PID 2>/dev/null; then
                    echo -e "${RED}❌ 前端服务意外停止${NC}"
                    break
                fi
                sleep 5
            done
        else
            echo -e "${RED}❌ 前端启动失败${NC}"
            exit 1
        fi
    else
        echo -e "${RED}❌ 后端启动失败${NC}"
        exit 1
    fi
}

# 运行主函数
main 