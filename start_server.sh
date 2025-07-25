#!/bin/bash

echo "🚀 Starting ContextHub Application..."
echo "================================="

# 检查Python依赖
echo "📦 Checking Python dependencies..."
if ! python -c "import flask, flask_cors" 2>/dev/null; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# 检查前端依赖
echo "📦 Checking Frontend dependencies..."
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing Frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# 创建上下文目录
mkdir -p my_contexts

# 启动后端服务器
echo "🐍 Starting Backend API Server (Port 5000)..."
python app.py &
BACKEND_PID=$!

# 等待后端启动
sleep 3

# 启动前端服务器
echo "⚛️  Starting Frontend Server (Port 3000)..."
cd frontend && npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Services Started Successfully!"
echo "================================="
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5000"
echo "📁 Upload folder: $(pwd)/my_contexts"
echo ""
echo "Press Ctrl+C to stop all services"
echo "================================="

# 等待用户中断
trap 'kill $BACKEND_PID $FRONTEND_PID; echo ""; echo "🛑 Services stopped"; exit 0' INT

# 保持脚本运行
wait 