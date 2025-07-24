# ContextHub - AI Context Management System

> 🤖 一个专为AI模型设计的上下文管理系统，提供标准化的 `.ct` 文件格式来最大化模型的性能表现。

## 🚀 项目概述

ContextHub 是一个开源的上下文管理工具，旨在解决AI模型在长对话和复杂场景中的上下文管理问题。通过标准化的 `.ct` 文件格式，ContextHub 能够：

- 📝 **结构化存储**：以JSON格式存储会话信息，包含完整的元数据和对话历史
- 🔍 **智能关联**：自动发现和关联相关的上下文信息
- ⚡ **性能优化**：智能压缩和优化上下文，确保模型发挥最佳性能
- 🛡️ **格式验证**：完整的格式验证和错误检查机制
- 🔧 **易于扩展**：模块化设计，支持自定义扩展
- 💬 **AI对话功能**：支持多种AI模型的实时对话
- 🎨 **现代化UI**：GitHub风格的响应式前端界面

## ✨ 核心特性

### 🗂️ 标准化的 `.ct` 文件格式

`.ct` 文件采用结构化的JSON格式，包含以下核心组件：

- **文件头**：版本信息、创建时间、编码格式
- **元数据**：会话ID、模型信息、用户信息、标签
- **上下文内容**：会话摘要、关键点、完整对话历史
- **关联上下文**：相关会话的引用和关联关系
- **模型状态**：模型参数、内存使用情况
- **性能指标**：响应时间、token效率、用户满意度

### 🤖 AI对话功能

- **多模型支持**：GPT-4、GPT-3.5 Turbo、Claude 3 系列
- **参数配置**：温度、最大令牌数、Top P 等参数调节
- **上下文对话**：基于已有 `.ct` 文件进行对话
- **实时交互**：流畅的聊天界面体验

### 🎨 现代化前端

- **React + TypeScript**：类型安全的前端架构
- **GitHub风格设计**：熟悉的界面风格
- **响应式布局**：适配各种屏幕尺寸
- **组件化开发**：模块化的组件设计

## 🏗️ 技术架构

### 后端 (Python)
```
contexthub/
├── core.py          # 核心上下文管理
├── utils.py         # 工具函数集
├── validators.py    # 格式验证器
└── __init__.py      # 包初始化
```

### 前端 (React + TypeScript)
```
frontend/src/
├── components/      # React组件
├── pages/          # 页面组件
├── types/          # TypeScript类型定义
├── utils/          # 工具函数
└── styles/         # 样式文件
```

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/River-Yang/ContextHub.git
cd ContextHub

# 安装Python依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend
npm install
```

### 运行

```bash
# 启动前端开发服务器
cd frontend
npm run dev

# 在浏览器中访问 http://localhost:5173
```

### Python API 使用

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

## 📖 使用指南

### 1. 上下文文件管理
- 📁 上传和管理 `.ct` 文件
- 👀 查看和编辑文件内容
- 🔍 搜索和过滤功能
- 📊 文件统计和分析

### 2. AI对话功能
- 🤖 选择不同的AI模型
- ⚙️ 调整模型参数
- 💬 基于上下文进行对话
- 📝 保存对话历史

### 3. 文件格式验证
```python
# 验证上下文文件
validator = ContextValidator()
is_valid, errors, warnings = validator.validate_file(context.data)

if is_valid:
    print("✅ 上下文文件验证通过")
else:
    print("❌ 发现错误:", errors)
```

## 🛠️ 开发指南

### 环境设置

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -r requirements.txt
cd frontend && npm install
```

### 构建和部署

```bash
# 构建前端
cd frontend
npm run build

# Python包构建
python setup.py sdist bdist_wheel
```

## 📋 功能特性

- ✅ `.ct` 文件格式支持
- ✅ 文件上传和管理
- ✅ 上下文查看和编辑
- ✅ AI对话功能
- ✅ 多模型支持
- ✅ 响应式UI设计
- ✅ TypeScript类型安全
- ✅ 组件化架构

## 🔮 未来规划

- [ ] 云端同步功能
- [ ] 团队协作支持
- [ ] 更多AI模型集成
- [ ] 移动端应用
- [ ] API服务化
- [ ] 插件系统
- [ ] 数据分析面板

## 🤝 贡献指南

我们欢迎所有形式的贡献！

1. **报告问题**：在GitHub Issues中报告bug或提出功能建议
2. **提交代码**：Fork项目并提交Pull Request
3. **改进文档**：帮助改进README、示例和文档
4. **分享用例**：分享您的使用案例和经验

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- 🏠 项目主页：[https://github.com/River-Yang/ContextHub](https://github.com/River-Yang/ContextHub)
- 🐛 问题反馈：[GitHub Issues](https://github.com/River-Yang/ContextHub/issues)
- 📧 邮箱：river@example.com

---

**ContextHub** - 让AI模型的上下文管理更简单、更高效！ 🚀
