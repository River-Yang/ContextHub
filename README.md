# ContextHub

一个专为AI模型设计的上下文管理系统，提供标准化的 `.ct` 文件格式来最大化模型的性能表现。

## 项目概述

ContextHub 是一个开源的上下文管理工具，旨在解决AI模型在长对话和复杂场景中的上下文管理问题。通过标准化的 `.ct` 文件格式，ContextHub 能够：

- 📝 **结构化存储**：以JSON格式存储会话信息，包含完整的元数据和对话历史
- 🔍 **智能关联**：自动发现和关联相关的上下文信息
- ⚡ **性能优化**：智能压缩和优化上下文，确保模型发挥最佳性能
- 🛡️ **格式验证**：完整的格式验证和错误检查机制
- 🔧 **易于扩展**：模块化设计，支持自定义扩展

## 核心特性

### 1. 标准化的 `.ct` 文件格式

`.ct` 文件采用结构化的JSON格式，包含以下核心组件：

- **文件头**：版本信息、创建时间、编码格式
- **元数据**：会话ID、模型信息、用户信息、标签
- **上下文内容**：会话摘要、关键点、完整对话历史
- **关联上下文**：相关会话的引用和关联关系
- **模型状态**：模型参数、内存使用情况
- **性能指标**：响应时间、token效率、用户满意度

### 2. 完整的API支持

```python
from contexthub import ContextFile, ContextManager, ContextValidator, ContextUtils

# 创建上下文管理器
manager = ContextManager("./contexts")

# 创建新的上下文文件
context = manager.create_context(
    session_name="AI助手对话",
    user_id="user-001",
    model_name="gpt-4",
    tags=["对话", "AI"]
)

# 添加对话消息
context.add_message("user", "你好，我想了解上下文管理")
context.add_message("assistant", "很高兴为您介绍上下文管理...")

# 保存上下文
context.save()
```

### 3. 智能验证系统

```python
# 验证上下文文件
validator = ContextValidator()
is_valid, errors, warnings = validator.validate_file(context.data)

if is_valid:
    print("✅ 上下文文件验证通过")
else:
    print("❌ 发现错误:", errors)
```

### 4. 强大的工具集

```python
# 生成会话ID
session_id = ContextUtils.generate_session_id()

# 估算token数量
tokens = ContextUtils.estimate_tokens("这是一段文本")

# 提取关键点
key_points = ContextUtils.extract_key_points(conversation)

# 优化上下文
optimized = ContextUtils.optimize_context_for_model(context_data, max_tokens=4000)

# 导出为Markdown
markdown = ContextUtils.export_to_markdown(context_data)
```

## 安装和使用

### 安装

```bash
# 克隆项目
git clone https://github.com/your-username/ContextHub.git
cd ContextHub

# 安装依赖
pip install -r requirements.txt
```

### 快速开始

```python
from contexthub import ContextManager

# 创建上下文管理器
manager = ContextManager("./my_contexts")

# 创建新会话
context = manager.create_context(
    session_name="我的AI对话",
    user_id="user-001",
    model_name="gpt-4"
)

# 添加对话
context.add_message("user", "你好，AI助手")
context.add_message("assistant", "你好！我是您的AI助手，有什么可以帮助您的吗？")

# 保存会话
context.save()
```

## 文件格式规范

### 基本结构

```json
{
  "version": "1.0.0",
  "format": "contexthub",
  "created_at": "2024-01-01T00:00:00Z",
  "last_modified": "2024-01-01T00:00:00Z",
  "encoding": "utf-8",
  
  "metadata": {
    "session_id": "session-2024-001",
    "model_info": {
      "name": "gpt-4",
      "version": "latest",
      "provider": "openai"
    },
    "user_info": {
      "user_id": "user-123",
      "session_name": "项目讨论",
      "tags": ["编程", "AI", "上下文管理"]
    }
  },
  
  "context": {
    "summary": "本次会话主要讨论了上下文管理系统的设计",
    "key_points": ["结构化存储", "元数据管理"],
    "conversation": [
      {
        "id": "msg-001",
        "timestamp": "2024-01-01T10:00:00Z",
        "role": "user",
        "content": "用户输入",
        "tokens": 10,
        "metadata": {
          "confidence": 0.95,
          "context_relevance": 0.9
        }
      }
    ]
  }
}
```

### 文件命名规范

- 格式：`{session_id}_{timestamp}.ct`
- 示例：`session-2024-001_20240101T100000Z.ct`

## 高级功能

### 1. 上下文关联

```python
# 查找相关上下文
related = ContextUtils.find_related_contexts(
    context_data,
    search_dir="./contexts",
    min_similarity=0.3
)
```

### 2. 智能压缩

```python
# 优化上下文以适应模型限制
optimized = ContextUtils.optimize_context_for_model(
    context_data,
    max_tokens=4000,
    model_name="gpt-4"
)
```

### 3. 上下文合并

```python
# 合并多个上下文
merged = ContextUtils.merge_contexts([context1, context2], "append")
```

## 示例和测试

运行示例代码：

```bash
python examples/usage_example.py
```

查看示例文件：

```bash
# 查看示例上下文文件
cat examples/sample_context.ct
```

## 贡献指南

我们欢迎所有形式的贡献！请查看以下指南：

1. **报告问题**：在GitHub Issues中报告bug或提出功能建议
2. **提交代码**：Fork项目并提交Pull Request
3. **改进文档**：帮助改进README、示例和文档
4. **分享用例**：分享您的使用案例和经验

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/your-username/ContextHub.git
cd ContextHub

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -r requirements.txt
```

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 联系方式

- 项目主页：https://github.com/your-username/ContextHub
- 问题反馈：https://github.com/your-username/ContextHub/issues
- 邮箱：your-email@example.com

## 更新日志

### v1.0.0 (2024-01-01)
- 🎉 初始版本发布
- ✨ 实现核心的 `.ct` 文件格式
- 🔧 提供完整的API和工具集
- 📝 添加详细的文档和示例

---

**ContextHub** - 让AI模型的上下文管理更简单、更高效！ 