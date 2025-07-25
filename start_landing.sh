#!/bin/bash

# ContextHub 展示页面启动脚本

echo "🚀 启动 ContextHub 展示页面..."

# 检查是否安装了 Python
if command -v python3 &> /dev/null; then
    echo "✅ 检测到 Python3"
    
    # 切换到 landing 目录
    cd landing 2>/dev/null || {
        echo "❌ 找不到 landing 目录"
        echo "请确保在项目根目录运行此脚本"
        exit 1
    }
    
    echo "📁 进入 landing 目录"
    echo "🌐 启动本地服务器在 http://localhost:8080"
    echo "按 Ctrl+C 停止服务器"
    echo ""
    
    # 启动 Python 简单服务器
    python3 -m http.server 8080
    
elif command -v python &> /dev/null; then
    echo "✅ 检测到 Python2"
    
    cd landing 2>/dev/null || {
        echo "❌ 找不到 landing 目录"
        exit 1
    }
    
    echo "📁 进入 landing 目录"
    echo "🌐 启动本地服务器在 http://localhost:8080"
    echo "按 Ctrl+C 停止服务器"
    echo ""
    
    # 启动 Python2 简单服务器
    python -m SimpleHTTPServer 8080
    
else
    echo "❌ 未检测到 Python"
    echo "请先安装 Python，或者："
    echo ""
    echo "1. 使用其他 HTTP 服务器:"
    echo "   - Node.js: npx serve landing"
    echo "   - PHP: php -S localhost:8080 -t landing"
    echo ""
    echo "2. 或直接在浏览器中打开 landing/index.html"
    echo "   注意：某些功能可能需要 HTTP 服务器环境"
fi 