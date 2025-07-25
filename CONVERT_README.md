# ContextHub 文件转换器

## 概述

`convert.py` 是一个强大的文件转换工具，使用 Kimi (Moonshot AI) API 来分析各种文件并将其转换为规范的 .ct 格式文件 (v3.0 状态链版)。

## 特性

- 🤖 **智能分析**: 使用 Kimi API 深度分析文件内容
- 📁 **多文件支持**: 支持代码文件、文档、图片等多种格式
- 🔄 **批量处理**: 可以批量转换整个目录
- 🎯 **自动分类**: 自动检测任务类型 (code_project, document_analysis, general_chat)
- 📊 **状态链记录**: 采用 v3.0 格式的状态链结构
- 🖼️ **图像支持**: 支持图像文件的 Vision 分析

## 安装依赖

```bash
pip install openai>=1.0.0
```

## 配置 API 密钥

在使用前，需要设置 Kimi API 密钥：

```bash
export MOONSHOT_API_KEY="your-api-key-here"
```

或者在代码中直接传入：

```python
converter = KimiConverter(api_key="your-api-key-here")
```

获取 API 密钥: https://platform.moonshot.cn/

## 使用方法

### 1. 命令行使用

#### 转换单个文件
```bash
python convert.py /path/to/file.py
```

#### 转换目录中的所有文件
```bash
python convert.py /path/to/directory -r
```

#### 指定输出目录
```bash
python convert.py /path/to/file.py -o ./output_contexts
```

#### 强制指定任务类型
```bash
python convert.py /path/to/file.py -t code_project
```

#### 筛选文件类型
```bash
# 只处理 Python 和 JavaScript 文件
python convert.py /path/to/directory -r --include "*.py" "*.js"

# 排除测试文件和缓存文件
python convert.py /path/to/directory -r --exclude "*test*" "*.pyc" "*__pycache__*"
```

### 2. Python API 使用

```python
from convert import KimiConverter

# 创建转换器
converter = KimiConverter()

# 转换单个文件
output_file = converter.convert_file(
    input_file="example.py",
    output_dir="./contexts",
    task_type="code_project"  # 可选，会自动检测
)

# 批量转换目录
converted_files = converter.convert_directory(
    input_dir="./src",
    output_dir="./contexts",
    recursive=True,
    include_patterns=["*.py", "*.js"],
    exclude_patterns=["*test*", "*.pyc"]
)
```

## 支持的文件格式

### 文本文件
- **代码文件**: `.py`, `.js`, `.ts`, `.tsx`, `.jsx`, `.java`, `.cpp`, `.c`, `.cs`, `.php`, `.rb`, `.go`, `.rs`, `.swift`, `.kt`, `.scala`
- **脚本文件**: `.sh`, `.bash`, `.zsh`
- **标记语言**: `.html`, `.xml`, `.md`
- **样式文件**: `.css`, `.scss`, `.sass`
- **配置文件**: `.json`, `.yaml`, `.yml`, `.toml`, `.ini`
- **数据库**: `.sql`
- **文档**: `.txt`, `.md`

### 图像文件
- `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`

## 任务类型

转换器会自动检测以下任务类型：

### 1. code_project
- **触发条件**: 代码文件、配置文件
- **分析重点**: 代码功能、技术栈、代码质量、改进建议、模块关系
- **文件示例**: `.py`, `.js`, `.json`, `.yaml`

### 2. document_analysis  
- **触发条件**: 文档文件、README文件
- **分析重点**: 内容结构、关键信息、文档类型、信息组织
- **文件示例**: `.md`, `.txt`, `README`

### 3. general_chat
- **触发条件**: 手动指定或其他类型文件
- **分析重点**: 通用内容分析

## .ct 文件格式 (v3.0)

生成的 .ct 文件遵循 v3.0 状态链格式：

```json
{
  "version": "3.0",
  "metadata": {
    "name": "文件名 分析",
    "task_type": "code_project",
    "createdAt": "2024-01-01T10:00:00Z",
    "source_file": "/path/to/original/file",
    "analysis_model": "kimi-k2-0711-preview"
  },
  "instructions": {
    "role_and_goal": "你是一个专业的代码项目专家..."
  },
  "assets": {
    "files": {
      "/path/to/file": {
        "asset_id": "file-12345678",
        "state_chain": [
          {
            "state_id": "s0",
            "timestamp": "2024-01-01T10:00:00Z",
            "summary": "初始分析: 文件的主要功能和特性",
            "content": "原始文件内容",
            "metadata": {
              "file_type": "text",
              "complexity": "medium",
              "purpose": "数据处理模块"
            }
          }
        ]
      }
    }
  },
  "examples": [
    {
      "context": "关键理解点1",
      "usage": "关键理解点"
    }
  ],
  "history": [
    {
      "role": "system",
      "content": "开始分析文件: /path/to/file",
      "timestamp": "2024-01-01T10:00:00Z"
    },
    {
      "role": "assistant",
      "content": "分析结果和建议",
      "timestamp": "2024-01-01T10:00:00Z",
      "metadata": {
        "analysis_summary": "简要总结",
        "key_points": ["要点1", "要点2"],
        "asset_reference": "file-12345678:s0"
      }
    }
  ]
}
```

## 运行示例

查看 `examples/usage_example.py` 获取完整的使用示例：

```bash
cd examples
python usage_example.py
```

## 命令行参数详解

```
使用 Kimi API 将文件转换为 .ct 格式

positional arguments:
  input                 输入文件或目录路径

optional arguments:
  -h, --help            显示帮助信息
  -o, --output OUTPUT   输出目录 (默认: ./contexts)
  -t, --task-type {general_chat,document_analysis,code_project}
                        强制指定任务类型
  -r, --recursive       递归处理目录
  --include INCLUDE [INCLUDE ...]
                        包含的文件模式 (如 *.py *.js)
  --exclude EXCLUDE [EXCLUDE ...]
                        排除的文件模式 (如 *test* *.pyc)
  --api-key API_KEY     Kimi API 密钥
```

## 最佳实践

1. **API 密钥安全**: 使用环境变量存储 API 密钥，不要硬编码在代码中
2. **批量处理**: 对于大量文件，建议使用批量处理功能
3. **文件筛选**: 使用 `--include` 和 `--exclude` 参数过滤不需要的文件
4. **输出管理**: 指定合适的输出目录避免文件混乱
5. **错误处理**: 转换失败的文件会显示错误信息，不会中断整个过程

## 错误处理

转换器包含完善的错误处理机制：

- **API 调用失败**: 返回错误信息，继续处理其他文件
- **文件读取失败**: 记录错误，跳过该文件
- **JSON 解析失败**: 使用原始响应内容作为分析结果
- **权限问题**: 显示权限错误信息

## 性能优化建议

1. **API 调用频率**: 注意 API 调用限制，避免频繁请求
2. **大文件处理**: 对于大型文件，API 可能需要更长处理时间
3. **并发控制**: 避免同时发起过多 API 请求
4. **缓存机制**: 考虑实现缓存避免重复分析相同文件

## 故障排除

### 常见问题

1. **API 密钥错误**
   ```
   ValueError: 请设置 MOONSHOT_API_KEY 环境变量或传入 api_key 参数
   ```
   解决：设置正确的 API 密钥

2. **网络连接问题**
   ```
   调用Kimi API失败: Connection error
   ```
   解决：检查网络连接和 API 服务状态

3. **文件权限问题**
   ```
   读取文件失败: Permission denied
   ```
   解决：检查文件读取权限

4. **输出目录权限**
   ```
   无法保存 .ct 文件: Permission denied
   ```
   解决：确保输出目录有写入权限

## 更新日志

### v1.0.0
- 初始版本发布
- 支持文本文件和图像文件分析
- 自动任务类型检测
- 批量处理功能
- 完整的命令行界面

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个工具。

## 许可证

此项目使用 MIT 许可证。 