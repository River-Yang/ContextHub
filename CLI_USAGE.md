# ContextHub 命令行工具使用指南

ContextHub 提供了强大的命令行工具，让你可以快速将各种文件转换为标准化的 `.ct` 格式并添加到你的上下文库中。

## 快速开始

### 安装依赖
```bash
pip install openai>=1.0.0 requests>=2.28.0
```

### 设置 API 密钥（可选）
```bash
export MOONSHOT_API_KEY="your-api-key-here" 
```
*注意：如果不设置，工具会使用内置的 API 密钥*

## 基本用法

### 使用 Python 脚本
```bash
python create_context.py [command] [options]
```

### 使用快捷脚本
```bash
./ctx [command] [options]
```

## 可用命令

### 1. 创建上下文文件 (`create`)

#### 转换单个文件
```bash
./ctx create README.md
./ctx create app.py -t code_project
```

#### 批量转换目录
```bash
./ctx create src/ -r                    # 递归处理整个目录
./ctx create . --include "*.py" "*.js"  # 只处理特定类型文件
./ctx create . --exclude "*test*"      # 排除测试文件
```

#### 选项说明
- `-t, --task-type`: 强制指定任务类型
  - `general_chat`: 普通对话
  - `document_analysis`: 文档分析
  - `code_project`: 代码项目
- `-r, --recursive`: 递归处理子目录
- `--include`: 包含的文件模式（如 `*.py` `*.js`）
- `--exclude`: 排除的文件模式（如 `*test*` `*.pyc`）
- `--hub-dir`: 指定存储目录（默认：`./my_contexts`）

### 2. 列出现有文件 (`list`)

#### 查看所有文件
```bash
./ctx list
```

#### 只显示最近的几个文件
```bash
./ctx list -n 5
```

### 3. 查看统计信息 (`stats`)

```bash
./ctx stats
```

显示：
- 总文件数
- 总存储大小
- 存储位置
- 任务类型分布

## 支持的文件类型

### 代码文件
- **Python**: `.py`
- **JavaScript/TypeScript**: `.js`, `.ts`, `.tsx`, `.jsx`
- **Web**: `.html`, `.css`, `.scss`, `.sass`, `.vue`
- **其他语言**: `.java`, `.cpp`, `.c`, `.cs`, `.php`, `.rb`, `.go`, `.rs`, `.swift`, `.kt`, `.scala`
- **脚本**: `.sh`, `.bash`, `.zsh`

### 配置文件
- `.json`, `.yaml`, `.yml`, `.toml`, `.ini`, `.xml`

### 文档文件
- `.md`, `.txt`, `.rst`

### 图像文件
- `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`

## 任务类型自动检测

工具会根据文件扩展名自动检测任务类型：

- **`code_project`**: 代码文件（`.py`, `.js`, `.java` 等）和配置文件
- **`document_analysis`**: 文档文件（`.md`, `.txt` 等）
- **`general_chat`**: 其他文件类型

你也可以使用 `-t` 选项强制指定任务类型。

## 使用示例

### 创建单个文件的上下文
```bash
# 分析 Python 文件（自动检测为 code_project）
./ctx create app.py

# 分析文档文件（自动检测为 document_analysis）
./ctx create README.md

# 强制指定任务类型
./ctx create config.json -t code_project
```

### 批量处理项目目录
```bash
# 处理整个项目（递归）
./ctx create . -r --exclude "*.pyc" "*__pycache__*" "*.git*"

# 只处理 Python 文件
./ctx create src/ -r --include "*.py"

# 处理前端文件
./ctx create frontend/ -r --include "*.js" "*.ts" "*.jsx" "*.tsx" "*.vue"
```

### 管理和查看文件
```bash
# 查看最近创建的 5 个文件
./ctx list -n 5

# 查看统计信息
./ctx stats

# 查看所有文件
./ctx list
```

## 输出格式

创建的 `.ct` 文件遵循 v3.0 标准格式，包含：

- **版本信息**: `version: "3.0"`
- **元数据**: 任务类型、创建时间、源文件等
- **指令**: AI 角色定义和目标
- **资产**: 文件内容和状态链
- **示例**: 关键理解点
- **历史**: 分析过程记录

## 存储位置

- 默认存储在 `./my_contexts/` 目录
- 可以通过 `--hub-dir` 选项指定其他目录
- 文件命名格式：`{原文件名}_{时间戳}.ct`

## 错误处理

如果遇到问题：

1. **API 密钥错误**: 确保设置了正确的 `MOONSHOT_API_KEY` 环境变量
2. **网络问题**: 检查网络连接，稍后重试
3. **文件读取错误**: 确保文件存在且有读取权限
4. **目录权限**: 确保对输出目录有写入权限

## 高级用法

### 集成到工作流
```bash
# Git Hook: 每次提交后自动创建上下文
git log --name-only -1 --pretty=format: | xargs -I {} ./ctx create {}

# 定期备份：批量处理修改的文件
find . -name "*.py" -mtime -1 | xargs -I {} ./ctx create {}
```

### 与 ContextHub Web 界面配合
命令行工具创建的文件会自动出现在 Web 界面 (`http://localhost:3001`) 中，你可以：
- 在浏览器中查看和管理文件
- 下载转换后的 `.ct` 文件
- 与 AI 进行交互

---

## 支持与反馈

如有问题或建议，请检查：
1. 文件权限和网络连接
2. API 密钥配置
3. 依赖包是否正确安装

Happy coding! 🚀 