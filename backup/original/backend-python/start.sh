#!/bin/bash

# 安装依赖
echo "Installing Python dependencies..."
pip install -r requirements.txt

# 启动服务
echo "Starting Python backend server..."
uvicorn main:app --host 0.0.0.0 --port 8000 --reload