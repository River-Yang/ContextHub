#!/bin/bash
# ContextHub 自动安装脚本

set -e  # 遇到错误时退出

echo "🚀 开始安装 ContextHub..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 函数：打印带颜色的消息
print_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Step 1: 检查 Python 版本
print_step "检查 Python 版本..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    print_error "未找到 Python，请先安装 Python 3.7+"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
print_success "发现 Python $PYTHON_VERSION"

# 检查 Python 版本是否 >= 3.7
if [[ $(echo "$PYTHON_VERSION" | cut -d'.' -f1) -lt 3 ]] || 
   [[ $(echo "$PYTHON_VERSION" | cut -d'.' -f1) -eq 3 && $(echo "$PYTHON_VERSION" | cut -d'.' -f2) -lt 7 ]]; then
    print_error "Python 版本过低，需要 3.7+，当前版本: $PYTHON_VERSION"
    exit 1
fi

# Step 2: 检查 pip
print_step "检查 pip..."
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    print_error "未找到 pip，请先安装 pip"
    exit 1
fi

print_success "发现 pip"

# Step 3: 升级 pip
print_step "升级 pip..."
$PIP_CMD install --upgrade pip || print_warning "pip 升级失败，继续安装..."

# Step 4: 安装依赖
print_step "安装 Python 依赖包..."

if [ -f "requirements.txt" ]; then
    print_step "使用 requirements.txt 安装依赖..."
    $PIP_CMD install -r requirements.txt
else
    print_step "手动安装核心依赖..."
    $PIP_CMD install openai>=1.0.0 Flask>=2.3.0 Flask-CORS>=4.0.0 requests>=2.28.0 typing-extensions>=4.0.0
fi

print_success "依赖包安装完成"

# Step 5: 验证安装
print_step "验证安装..."

# 检查核心模块
if $PYTHON_CMD -c "from convert import KimiConverter" 2>/dev/null; then
    print_success "KimiConverter 模块导入成功"
else
    print_error "KimiConverter 模块导入失败"
    exit 1
fi

# 检查 OpenAI 版本
OPENAI_VERSION=$($PYTHON_CMD -c "import openai; print(openai.__version__)" 2>/dev/null)
if [ $? -eq 0 ]; then
    print_success "OpenAI SDK 版本: $OPENAI_VERSION"
else
    print_error "OpenAI SDK 检查失败"
    exit 1
fi

# Step 6: 设置可执行权限
print_step "设置脚本权限..."
if [ -f "ctx" ]; then
    chmod +x ctx
    print_success "快捷脚本 ctx 权限设置完成"
fi

if [ -f "create_context.py" ]; then
    chmod +x create_context.py
    print_success "主脚本权限设置完成"
fi

# Step 7: 创建必要目录
print_step "创建必要目录..."
mkdir -p my_contexts
print_success "上下文存储目录创建完成"

# Step 8: 最终验证
print_step "最终验证..."
if $PYTHON_CMD create_context.py --help > /dev/null 2>&1; then
    print_success "命令行工具验证成功"
else
    print_error "命令行工具验证失败"
    exit 1
fi

# 完成安装
echo ""
echo "🎉 ContextHub 安装完成！"
echo ""
echo "📚 接下来你可以："
echo "  1. 运行 './ctx --help' 查看帮助"
echo "  2. 运行 './ctx stats' 查看统计信息"
echo "  3. 运行 './ctx create <file>' 创建上下文文件"
echo "  4. 运行 'python app.py' 启动 Web 服务器"
echo ""
echo "📖 查看详细文档："
echo "  - 安装指南: INSTALL.md"
echo "  - 使用指南: CLI_USAGE.md"
echo ""

# 显示快速测试
echo "🧪 快速测试:"
echo "  echo '# Test' > test.md && ./ctx create test.md && rm test.md"
echo ""

print_success "安装脚本执行完成！" 