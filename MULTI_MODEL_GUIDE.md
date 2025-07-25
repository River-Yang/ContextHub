# ContextHub 多模型转换器使用指南

## 🌟 概述

ContextHub 现在支持多个AI模型来分析文件并转换为 `.ct` 格式！你可以选择最适合你需求的AI模型。

## 🤖 支持的模型

| 模型 | 提供商 | 支持状态 | 支持图像 | 特点 |
|------|--------|----------|----------|------|
| **kimi** | Moonshot AI | ✅ 已实现 | ✅ | 中文友好，性价比高 |
| **openai** | OpenAI | ✅ 已实现 | ✅ | GPT-4o-mini，质量稳定 |
| **claude** | Anthropic | ✅ 已实现 | ✅ | Claude-3.5，推理能力强 |
| **qwen** | 阿里云 | 🚧 计划中 | ✅ | 通义千问，中文优化 |
| **ernie** | 百度 | 🚧 计划中 | ✅ | 文心一言，本土化 |
| **glm** | 智谱AI | 🚧 计划中 | ✅ | GLM-4，性能均衡 |

## 🔧 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

有两种方式配置API密钥：

#### 方式一：环境变量（推荐）

```bash
# Moonshot Kimi
export MOONSHOT_API_KEY="your-kimi-api-key"

# OpenAI
export OPENAI_API_KEY="your-openai-api-key"

# Anthropic Claude
export ANTHROPIC_API_KEY="your-claude-api-key"
```

#### 方式二：配置文件

编辑 `model_config.yaml`：

```yaml
default_model: "kimi"

api_keys:
  kimi:
    api_key: "your-kimi-api-key"
  openai:
    api_key: "your-openai-api-key"
  claude:
    api_key: "your-claude-api-key"
```

### 3. 使用命令行工具

#### 查看可用模型

```bash
python convert_multi_model.py --list-models
```

#### 使用默认模型转换文件

```bash
python convert_multi_model.py example.py
```

#### 指定模型转换文件

```bash
# 使用 OpenAI GPT
python convert_multi_model.py example.py -m openai

# 使用 Claude
python convert_multi_model.py example.py -m claude

# 使用 Kimi
python convert_multi_model.py example.py -m kimi
```

#### 批量转换目录

```bash
python convert_multi_model.py ./my_project -m openai -o ./contexts
```

## 🖥️ Web界面使用

### 1. 启动服务器

```bash
python app.py
```

### 2. 查看可用模型

访问API端点查看所有可用模型：

```bash
curl http://localhost:5001/api/models
```

### 3. 切换模型

通过API切换当前使用的模型：

```bash
curl -X POST http://localhost:5001/api/models/switch \
  -H "Content-Type: application/json" \
  -d '{"model": "openai", "api_key": "your-key-here"}'
```

### 4. 在前端使用

前端界面会自动使用当前配置的模型进行文件转换。

## 📝 使用示例

### Python API 使用

```python
from convert_multi_model import create_converter

# 创建 OpenAI 转换器
converter = create_converter("openai", api_key="your-key")

# 转换单个文件
output_file = converter.convert_file("example.py", "./contexts")
print(f"转换完成: {output_file}")

# 批量转换
output_files = converter.convert_directory("./my_project", "./contexts")
print(f"批量转换完成，共 {len(output_files)} 个文件")
```

### 切换模型

```python
# 尝试不同的模型
models = ["kimi", "openai", "claude"]

for model_name in models:
    try:
        converter = create_converter(model_name)
        result = converter.convert_file("test.py")
        print(f"✅ {model_name}: 转换成功")
        break
    except Exception as e:
        print(f"❌ {model_name}: {e}")
        continue
```

## ⚙️ 高级配置

### 自定义模型配置

在 `model_config.yaml` 中自定义设置：

```yaml
model_settings:
  generation:
    max_tokens: 4000
    temperature: 0.3
    
  output:
    default_dir: "./my_contexts"
    file_naming: "{filename}_{model}_{timestamp}.ct"
    
advanced:
  retry:
    max_attempts: 3
    delay_seconds: 1
```

### 并发处理（计划功能）

```yaml
advanced:
  concurrency:
    enabled: true
    max_workers: 3
```

## 🔍 故障排除

### 常见问题

1. **API密钥错误**
   ```
   错误: 请设置 OPENAI_API_KEY 环境变量或传入 api_key 参数
   ```
   解决：确保正确设置了对应模型的API密钥。

2. **模型不可用**
   ```
   错误: 模型 qwen 的转换器尚未实现
   ```
   解决：选择已实现的模型（kimi、openai、claude）。

3. **依赖缺失**
   ```
   错误: 请安装 Anthropic SDK: pip install anthropic
   ```
   解决：安装对应的SDK依赖。

### 调试模式

启用详细日志输出：

```bash
export CONTEXTHUB_DEBUG=1
python convert_multi_model.py example.py -m openai
```

## 📚 API 参考

### 核心类

- `BaseConverter`: 转换器基类
- `KimiConverter`: Kimi API 转换器
- `OpenAIConverter`: OpenAI API 转换器  
- `ClaudeConverter`: Claude API 转换器

### 主要函数

- `create_converter(model_name, api_key=None)`: 创建指定模型的转换器
- `list_available_models()`: 列出所有可用模型

### Web API 端点

- `GET /api/models`: 获取可用模型列表
- `POST /api/models/switch`: 切换当前模型
- `POST /api/create`: 使用当前模型转换文件

## 🔗 扩展开发

想添加新的模型支持？查看 `ClaudeConverter` 的实现作为参考：

```python
class YourConverter(BaseConverter):
    def _setup_client(self):
        # 设置你的API客户端
        pass
    
    def _call_api(self, prompt, is_image=False, image_data=None):
        # 实现API调用逻辑
        pass
```

然后在 `CONVERTER_CLASSES` 中注册：

```python
CONVERTER_CLASSES = {
    "kimi": KimiConverter,
    "openai": OpenAIConverter,
    "claude": ClaudeConverter,
    "your_model": YourConverter,  # 添加这里
}
```

## 📞 支持

遇到问题？

1. 查看 [故障排除](#-故障排除) 部分
2. 检查API密钥和网络连接
3. 确认模型服务状态
4. 提交Issue到项目仓库

---

🎉 **享受多模型的强大功能！** 选择最适合你任务的AI模型，获得最佳的文件分析效果。 