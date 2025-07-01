#!/bin/bash

# SysScope AI 开发环境停止脚本
# Development Environment Stop Script for SysScope AI

echo "🛑 停止 SysScope AI 开发环境..."
echo "Stopping SysScope AI Development Environment..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 停止函数
stop_services() {
    echo -e "${BLUE}正在停止所有服务...${NC}"
    
    # 从PID文件读取进程ID
    if [ -f "logs/backend.pid" ]; then
        BACKEND_PID=$(cat logs/backend.pid)
        if [ -n "$BACKEND_PID" ] && kill -0 $BACKEND_PID 2>/dev/null; then
            echo -e "${BLUE}停止后端服务 (PID: $BACKEND_PID)...${NC}"
            kill -TERM $BACKEND_PID 2>/dev/null
            sleep 3
            if kill -0 $BACKEND_PID 2>/dev/null; then
                echo -e "${YELLOW}强制停止后端服务...${NC}"
                kill -9 $BACKEND_PID 2>/dev/null
            fi
            echo -e "${GREEN}✅ 后端服务已停止${NC}"
        else
            echo -e "${YELLOW}⚠️  后端服务未运行或PID无效${NC}"
        fi
        rm -f logs/backend.pid
    else
        echo -e "${YELLOW}⚠️  未找到后端PID文件${NC}"
    fi
    
    if [ -f "logs/frontend.pid" ]; then
        FRONTEND_PID=$(cat logs/frontend.pid)
        if [ -n "$FRONTEND_PID" ] && kill -0 $FRONTEND_PID 2>/dev/null; then
            echo -e "${BLUE}停止前端服务 (PID: $FRONTEND_PID)...${NC}"
            kill -TERM $FRONTEND_PID 2>/dev/null
            sleep 3
            if kill -0 $FRONTEND_PID 2>/dev/null; then
                echo -e "${YELLOW}强制停止前端服务...${NC}"
                kill -9 $FRONTEND_PID 2>/dev/null
            fi
            echo -e "${GREEN}✅ 前端服务已停止${NC}"
        else
            echo -e "${YELLOW}⚠️  前端服务未运行或PID无效${NC}"
        fi
        rm -f logs/frontend.pid
    else
        echo -e "${YELLOW}⚠️  未找到前端PID文件${NC}"
    fi
    
    # 清理可能的残留进程
    echo -e "${BLUE}清理残留进程...${NC}"
    
    # 停止Python相关进程
    PYTHON_PIDS=$(pgrep -f "python.*app.py" 2>/dev/null)
    if [ -n "$PYTHON_PIDS" ]; then
        echo -e "${BLUE}停止Python进程: $PYTHON_PIDS${NC}"
        echo $PYTHON_PIDS | xargs kill -TERM 2>/dev/null
        sleep 2
        echo $PYTHON_PIDS | xargs kill -9 2>/dev/null
    fi
    
    # 停止Node.js相关进程
    NODE_PIDS=$(pgrep -f "node.*start" 2>/dev/null)
    if [ -n "$NODE_PIDS" ]; then
        echo -e "${BLUE}停止Node.js进程: $NODE_PIDS${NC}"
        echo $NODE_PIDS | xargs kill -TERM 2>/dev/null
        sleep 2
        echo $NODE_PIDS | xargs kill -9 2>/dev/null
    fi
    
    # 停止uvicorn进程
    UVICORN_PIDS=$(pgrep -f "uvicorn.*app:app" 2>/dev/null)
    if [ -n "$UVICORN_PIDS" ]; then
        echo -e "${BLUE}停止uvicorn进程: $UVICORN_PIDS${NC}"
        echo $UVICORN_PIDS | xargs kill -TERM 2>/dev/null
        sleep 2
        echo $UVICORN_PIDS | xargs kill -9 2>/dev/null
    fi
    
    # 检查端口占用情况
    echo -e "${BLUE}检查端口占用情况...${NC}"
    
    PORT_8000_PID=$(lsof -ti tcp:8000 2>/dev/null)
    if [ -n "$PORT_8000_PID" ]; then
        echo -e "${YELLOW}⚠️  端口8000仍被进程$PORT_8000_PID占用${NC}"
        kill -TERM $PORT_8000_PID 2>/dev/null
        sleep 2
        if kill -0 $PORT_8000_PID 2>/dev/null; then
            kill -9 $PORT_8000_PID 2>/dev/null
        fi
    fi
    
    PORT_3000_PID=$(lsof -ti tcp:3000 2>/dev/null)
    if [ -n "$PORT_3000_PID" ]; then
        echo -e "${YELLOW}⚠️  端口3000仍被进程$PORT_3000_PID占用${NC}"
        kill -TERM $PORT_3000_PID 2>/dev/null
        sleep 2
        if kill -0 $PORT_3000_PID 2>/dev/null; then
            kill -9 $PORT_3000_PID 2>/dev/null
        fi
    fi
    
    echo -e "${GREEN}✅ 所有服务已停止${NC}"
}

# 检查服务状态
check_status() {
    echo -e "${BLUE}检查服务状态...${NC}"
    
    # 检查后端服务
    if curl -s http://localhost:8000/ > /dev/null 2>&1; then
        echo -e "${RED}❌ 后端服务仍在运行 (端口8000)${NC}"
    else
        echo -e "${GREEN}✅ 后端服务已停止${NC}"
    fi
    
    # 检查前端服务
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo -e "${RED}❌ 前端服务仍在运行 (端口3000)${NC}"
    else
        echo -e "${GREEN}✅ 前端服务已停止${NC}"
    fi
    
    # 检查进程
    PYTHON_COUNT=$(pgrep -c -f "python.*app.py" 2>/dev/null || echo "0")
    NODE_COUNT=$(pgrep -c -f "node.*start" 2>/dev/null || echo "0")
    UVICORN_COUNT=$(pgrep -c -f "uvicorn.*app:app" 2>/dev/null || echo "0")
    
    echo -e "${BLUE}进程统计:${NC}"
    echo -e "  Python进程: $PYTHON_COUNT"
    echo -e "  Node.js进程: $NODE_COUNT"
    echo -e "  uvicorn进程: $UVICORN_COUNT"
}

# 主函数
main() {
    case "${1:-stop}" in
        "stop")
            stop_services
            ;;
        "status")
            check_status
            ;;
        "force")
            echo -e "${YELLOW}⚠️  强制停止所有相关进程...${NC}"
            pkill -f "python.*app.py" 2>/dev/null
            pkill -f "node.*start" 2>/dev/null
            pkill -f "uvicorn.*app:app" 2>/dev/null
            echo -e "${GREEN}✅ 强制停止完成${NC}"
            ;;
        *)
            echo -e "${YELLOW}用法: $0 [stop|status|force]${NC}"
            echo -e "  stop   - 正常停止服务 (默认)"
            echo -e "  status - 检查服务状态"
            echo -e "  force  - 强制停止所有相关进程"
            exit 1
            ;;
    esac
}

# 运行主函数
main "$@" 