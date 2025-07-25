@echo off
REM ContextHub Windows 自动安装脚本

echo 🚀 开始安装 ContextHub...

REM 检查 Python
echo 📋 检查 Python 版本...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到 Python，请先安装 Python 3.7+
    echo 💡 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ 发现 Python %PYTHON_VERSION%

REM 检查 pip
echo 📋 检查 pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到 pip，请重新安装 Python
    pause
    exit /b 1
)
echo ✅ 发现 pip

REM 升级 pip
echo 📋 升级 pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 📋 安装 Python 依赖包...
if exist requirements.txt (
    echo 📋 使用 requirements.txt 安装依赖...
    python -m pip install -r requirements.txt
) else (
    echo 📋 手动安装核心依赖...
    python -m pip install openai>=1.0.0 Flask>=2.3.0 Flask-CORS>=4.0.0 requests>=2.28.0 typing-extensions>=4.0.0
)

if %errorlevel% neq 0 (
    echo ❌ 依赖包安装失败
    pause
    exit /b 1
)
echo ✅ 依赖包安装完成

REM 验证安装
echo 📋 验证安装...

python -c "from convert import KimiConverter" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ KimiConverter 模块导入失败
    pause
    exit /b 1
)
echo ✅ KimiConverter 模块导入成功

for /f %%i in ('python -c "import openai; print(openai.__version__)"') do set OPENAI_VERSION=%%i
echo ✅ OpenAI SDK 版本: %OPENAI_VERSION%

REM 创建必要目录
echo 📋 创建必要目录...
if not exist my_contexts mkdir my_contexts
echo ✅ 上下文存储目录创建完成

REM 创建 Windows 快捷脚本
echo 📋 创建快捷脚本...
echo @echo off > ctx.bat
echo python create_context.py %%* >> ctx.bat
echo ✅ Windows 快捷脚本 ctx.bat 创建完成

REM 最终验证
echo 📋 最终验证...
python create_context.py --help >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 命令行工具验证失败
    pause
    exit /b 1
)
echo ✅ 命令行工具验证成功

REM 完成安装
echo.
echo 🎉 ContextHub 安装完成！
echo.
echo 📚 接下来你可以：
echo   1. 运行 'ctx --help' 查看帮助
echo   2. 运行 'ctx stats' 查看统计信息
echo   3. 运行 'ctx create ^<file^>' 创建上下文文件
echo   4. 运行 'python app.py' 启动 Web 服务器
echo.
echo 📖 查看详细文档：
echo   - 安装指南: INSTALL.md
echo   - 使用指南: CLI_USAGE.md
echo.
echo 🧪 快速测试:
echo   echo # Test ^> test.md ^&^& ctx create test.md ^&^& del test.md
echo.
echo ✅ 安装脚本执行完成！
echo.
pause 