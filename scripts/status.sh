#!/bin/bash

echo "🔍 Shop Manager 服务状态检查"
echo "================================"

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

# 检查Python后端状态
echo "1. Python后端状态检查..."
if pgrep -f "python main.py" > /dev/null; then
    BACKEND_PID=$(pgrep -f "python main.py")
    echo "   ✅ 后端服务运行中 (PID: $BACKEND_PID)"
    
    # 检查端口
    if lsof -i :8000 > /dev/null 2>&1; then
        echo "   ✅ 端口8000正常监听"
        
        # 测试API健康检查
        if curl -s http://localhost:8000/health > /dev/null; then
            echo "   ✅ API健康检查通过"
        else
            echo "   ❌ API健康检查失败"
        fi
    else
        echo "   ❌ 端口8000未监听"
    fi
else
    echo "   ❌ 后端服务未运行"
fi

# 检查前端状态
echo ""
echo "2. 前端服务状态检查..."
if pgrep -f "npm run dev" > /dev/null; then
    FRONTEND_PID=$(pgrep -f "npm run dev")
    echo "   ✅ 前端服务运行中 (PID: $FRONTEND_PID)"
    
    # 检查端口
    if lsof -i :3000 > /dev/null 2>&1; then
        echo "   ✅ 端口3000正常监听"
        
        # 测试前端访问
        if curl -s http://localhost:3000 > /dev/null; then
            echo "   ✅ 前端页面可访问"
        else
            echo "   ❌ 前端页面无法访问"
        fi
    else
        echo "   ❌ 端口3000未监听"
    fi
else
    echo "   ❌ 前端服务未运行"
fi

# 检查数据库连接
echo ""
echo "3. 数据库连接检查..."
if [ -f "backend-python/.env" ]; then
    echo "   ✅ 环境配置文件存在"
    
    # 尝试连接数据库
    cd backend-python
    if python -c "
import os
from dotenv import load_dotenv
load_dotenv()
from app.database import engine
try:
    with engine.connect() as conn:
        conn.execute('SELECT 1')
    print('✅ 数据库连接成功')
except Exception as e:
    print(f'❌ 数据库连接失败: {e}')
" 2>/dev/null; then
        echo "   ✅ 数据库连接正常"
    else
        echo "   ❌ 数据库连接失败"
    fi
    cd ..
else
    echo "   ❌ 环境配置文件不存在"
fi

# 检查日志文件
echo ""
echo "4. 日志文件检查..."
if [ -f "backend-python/logs/app.log" ]; then
    echo "   ✅ 后端日志文件存在"
    echo "   最后10行日志:"
    tail -5 backend-python/logs/app.log | sed 's/^/   /'
else
    echo "   ❌ 后端日志文件不存在"
fi

if [ -f "logs/frontend.log" ]; then
    echo "   ✅ 前端日志文件存在"
    echo "   最后5行日志:"
    tail -5 logs/frontend.log | sed 's/^/   /'
else
    echo "   ❌ 前端日志文件不存在"
fi

# 检查进程资源使用
echo ""
echo "5. 进程资源使用情况..."
echo "   后端进程:"
if pgrep -f "python main.py" > /dev/null; then
    ps -p $(pgrep -f "python main.py") -o pid,ppid,command | tail -1 | sed 's/^/   /'
fi

echo "   前端进程:"
if pgrep -f "npm run dev" > /dev/null; then
    ps -p $(pgrep -f "npm run dev") -o pid,ppid,command | tail -1 | sed 's/^/   /'
fi

# 检查端口占用
echo ""
echo "6. 端口占用情况..."
echo "   端口8000 (后端):"
lsof -i :8000 2>/dev/null | sed 's/^/   /' || echo "   ❌ 端口8000未被占用"

echo "   端口3000 (前端):"
lsof -i :3000 2>/dev/null | sed 's/^/   /' || echo "   ❌ 端口3000未被占用"

echo ""
echo "================================"
echo "状态检查完成！"
