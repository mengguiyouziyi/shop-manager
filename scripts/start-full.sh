#!/bin/bash

echo "🏪 Shop Manager 完整启动脚本"
echo "================================"

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "项目根目录: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# 1. 检查Python环境
echo "1. 检查Python环境..."
if command -v pyenv &> /dev/null; then
    echo "   使用pyenv管理Python版本"
    # 激活pyenv环境
    eval "$(pyenv init -)"
    pyenv activate slj 2>/dev/null || echo "   警告: 无法激活slj环境，使用系统Python"
else
    echo "   使用系统Python"
fi

echo "   Python版本: $(python --version 2>&1)"

# 2. 启动Python后端
echo "2. 启动Python后端..."
cd "$PROJECT_ROOT/backend-python"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "   创建虚拟环境..."
    python -m venv venv
fi

echo "   激活虚拟环境..."
source venv/bin/activate

echo "   安装Python依赖..."
pip install -r requirements.txt

echo "   启动后端服务..."
nohup python main.py > logs/app.log 2>&1 &
BACKEND_PID=$!

echo "   Python后端已启动 (PID: $BACKEND_PID, 端口: 8000)"
echo "   等待后端服务启动..."
sleep 5

# 检查后端是否启动成功
if curl -s http://localhost:8000/health > /dev/null; then
    echo "   ✅ 后端服务启动成功"
else
    echo "   ❌ 后端服务启动失败"
    exit 1
fi

# 3. 创建测试数据
echo "3. 创建测试数据..."
cd "$PROJECT_ROOT/backend-python"
python create_test_users.py

# 4. 启动前端
echo "4. 启动前端..."
cd "$PROJECT_ROOT/frontend"

echo "   安装前端依赖..."
npm install

echo "   启动前端开发服务器..."
nohup npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!

echo "   前端已启动 (PID: $FRONTEND_PID, 端口: 3000)"
echo "   等待前端服务启动..."
sleep 10

# 检查前端是否启动成功
if curl -s http://localhost:3000 > /dev/null; then
    echo "   ✅ 前端服务启动成功"
else
    echo "   ❌ 前端服务启动失败"
    exit 1
fi

echo ""
echo "✅ 启动完成！"
echo "   前端: http://localhost:3000"
echo "   Python后端: http://localhost:8000"
echo "   API文档: http://localhost:8000/docs"
echo "   健康检查: http://localhost:8000/health"
echo ""
echo "📋 测试账户信息:"
echo "   用户名: admin, 密码: password"
echo "   用户名: user, 密码: password"
echo ""
echo "📁 日志文件:"
echo "   后端日志: backend-python/logs/app.log"
echo "   前端日志: logs/frontend.log"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo "================================"

# 创建日志目录
mkdir -p "$PROJECT_ROOT/logs"

# 等待用户中断
trap 'echo "正在停止服务..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT
wait
