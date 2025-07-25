# ContextHub 安装指南

本指南将帮助你安装和配置 ContextHub 及其命令行工具。

## 📋 系统要求

- **Python 3.7 或更高版本**
- **互联网连接**（用于 Kimi API 调用）
- **操作系统**: Windows, macOS, Linux

## 🚀 快速安装

### 方法 1: pip 安装（最简单）

#### 基础安装
```bash
pip install contexthub
```

#### 包含Web服务器
```bash
pip install contexthub[server]
```

#### 完整安装（包含开发工具）
```bash
pip install contexthub[all]
```

安装完成后，你可以直接使用：
```bash
ctx --help                    # 查看帮助
ctx create file.py           # 创建上下文文件
contexthub stats             # 查看统计信息
contexthub-server            # 启动Web服务器
```

### 方法 2: 从源码安装

#### 方法 2a: 自动安装脚本（推荐）

**macOS/Linux**
```bash
git clone <your-contexthub-repo>
cd ContextHUb
./install.sh
```

**Windows**
```bash
git clone <your-contexthub-repo>
cd ContextHUb
install.bat
```

#### 方法 2b: 手动安装

#### 1. 克隆项目（如果尚未获取）
```bash
git clone <your-contexthub-repo>
cd ContextHUb
```

#### 2. 安装 Python 依赖
```bash
# 方法1: 使用 requirements.txt（推荐）
pip install -r requirements.txt

# 方法2: 手动安装核心依赖
pip install openai>=1.0.0 Flask>=2.3.0 Flask-CORS>=4.0.0 requests>=2.28.0
```

#### 3. 验证安装
```bash
# 测试命令行工具
python create_context.py --help

# 或使用快捷脚本
./ctx --help
```

## 📦 详细安装步骤

### Step 1: 检查 Python 版本
```bash
python --version
# 或
python3 --version
```
确保版本 ≥ 3.7

### Step 2: 创建虚拟环境（推荐）
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### Step 3: 升级 pip
```bash
pip install --upgrade pip
```

### Step 4: 安装依赖包
```bash
# 安装所有依赖
pip install -r requirements.txt
```

### Step 5: 设置 API 密钥（可选）
```bash
# 导出环境变量
export MOONSHOT_API_KEY="your-api-key-here"

# 或永久添加到 shell 配置文件
echo 'export MOONSHOT_API_KEY="your-api-key-here"' >> ~/.bashrc
# 或 ~/.zshrc (macOS)
```

**注意**: 如果不设置，工具会使用内置的 API 密钥。

### Step 6: 验证安装
```bash
# 检查核心模块是否可导入
python -c "from convert import KimiConverter; print('✅ KimiConverter 导入成功')"
python -c "import openai; print('✅ OpenAI SDK 版本:', openai.__version__)"

# 测试命令行工具
./ctx stats
```

## 🐳 Docker 安装（可选）

如果你prefer使用 Docker：

```bash
# 构建镜像
docker build -t contexthub .

# 运行容器
docker run -p 5001:5001 -p 3001:3001 contexthub
```

## 🔧 各平台特定说明

### macOS
```bash
# 如果使用 Homebrew 安装的 Python
brew install python3
pip3 install -r requirements.txt

# 设置别名（可选）
echo 'alias ctx="./ctx"' >> ~/.zshrc
```

### Windows
```bash
# 使用 cmd 或 PowerShell
python -m pip install -r requirements.txt

# 创建批处理文件 ctx.bat
@echo off
python create_context.py %*
```

### Linux (Ubuntu/Debian)
```bash
# 安装 Python 和 pip
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 安装依赖
pip3 install -r requirements.txt
```

## ✅ 验证安装成功

运行以下命令确认一切正常：

```bash
# 1. 检查帮助信息
./ctx --help

# 2. 查看统计信息
./ctx stats

# 3. 创建测试文件
echo "# 测试文件" > test.md
./ctx create test.md
rm test.md

# 4. 检查 Web 服务器（可选）
python app.py  # 应该在 http://localhost:5001 启动服务
```

## 🐛 常见问题解决

### 问题 1: `command not found: python`
**解决方案**:
```bash
# 尝试使用 python3
python3 create_context.py --help

# 或创建别名
alias python=python3
```

### 问题 2: `pip install` 失败
**解决方案**:
```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用国内镜像（中国用户）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 问题 3: `Permission denied: ./ctx`
**解决方案**:
```bash
# 添加执行权限
chmod +x ctx

# 或直接使用 Python
python create_context.py stats
```

### 问题 4: `ModuleNotFoundError: No module named 'openai'`
**解决方案**:
```bash
# 确认在正确的环境中
which python
which pip

# 重新安装 OpenAI SDK
pip install --force-reinstall openai>=1.0.0
```

### 问题 5: API 调用失败
**解决方案**:
```bash
# 检查网络连接
curl -I https://api.moonshot.cn

# 测试 API 密钥
python -c "
from convert import KimiConverter
try:
    converter = KimiConverter()
    print('✅ API 密钥有效')
except Exception as e:
    print('❌ API 配置问题:', e)
"
```

### 问题 6: 端口被占用
**解决方案**:
```bash
# 查找占用端口的进程
lsof -ti:5001

# 终止进程
lsof -ti:5001 | xargs kill -9

# 或使用不同端口
python app.py --port 5002
```

## 🔄 更新依赖

定期更新依赖包以获得最新功能和安全修复：

```bash
# 更新所有包到最新版本
pip install --upgrade -r requirements.txt

# 检查过时的包
pip list --outdated

# 更新特定包
pip install --upgrade openai
```

## 📁 目录结构

安装完成后，你的目录应该类似：

```
ContextHUb/
├── create_context.py    # 主命令行工具
├── ctx                  # 快捷脚本 (Unix/Linux/macOS)
├── ctx.bat             # 快捷脚本 (Windows，安装后生成)
├── convert.py          # 文件转换核心
├── app.py              # Web API 服务器
├── install.sh          # 自动安装脚本 (Unix/Linux/macOS)
├── install.bat         # 自动安装脚本 (Windows)
├── requirements.txt    # 依赖列表
├── CLI_USAGE.md       # 使用指南
├── INSTALL.md         # 本安装指南
├── my_contexts/       # 上下文文件存储目录
└── frontend/          # Web 前端（可选）
```

## 🎯 下一步

安装完成后，你可以：

1. **阅读使用指南**: `CLI_USAGE.md`
2. **开始使用命令行工具**: `./ctx create your_file.py`
3. **启动 Web 界面**: `python app.py` 然后访问 `http://localhost:5001`
4. **探索高级功能**: 批量处理、任务类型自定义等

## 💬 获取帮助

如果遇到问题：

1. 检查 [常见问题](#🐛-常见问题解决) 部分
2. 确认 Python 版本和依赖版本
3. 检查网络连接和 API 配置
4. 查看详细错误信息并搜索解决方案

---

**安装成功后，你就可以开始使用强大的 ContextHub 命令行工具了！** 🎉

运行 `./ctx --help` 查看所有可用命令，或查看 `CLI_USAGE.md` 了解详细用法。 