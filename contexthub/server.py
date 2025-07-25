#!/usr/bin/env python3
"""
ContextHub Web 服务器入口点
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def main():
    """Web 服务器主入口点"""
    try:
        # 导入并运行 Flask 应用
        from app import app
        
        # 打印启动信息
        print("🚀 Starting ContextHub API Server...")
        print("🌐 Server will run on: http://localhost:5001")
        
        # 运行服务器
        app.run(
            host="0.0.0.0",
            port=5001,
            debug=True
        )
        
    except KeyboardInterrupt:
        print("\n服务器已停止")
        sys.exit(0)
    except Exception as e:
        print(f"服务器启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 