# ContextHub - AI Context Management System

> **上下文是新的源代码**  
> 🤖 一个专为AI模型设计的上下文管理系统，提供标准化的 `.ct` 文件格式来最大化模型的性能表现。

## 🎨 精美展示页面

体验 ContextHub 的现代化展示页面，参考 [SpecStory](https://specstory.com/) 设计：

```bash
# 启动展示页面
./start_landing.sh
# 访问 http://localhost:8080
```

**展示页面特色：**
- 🌟 现代化深色主题设计
- 📱 完全响应式布局
- ✨ 精美动画和交互效果
- 🔥 终端演示和代码展示
- 🚀 一键体验 ContextHub 功能

## 🚀 项目概述

ContextHub 是一个开源的上下文管理工具，旨在解决AI模型在长对话和复杂场景中的上下文管理问题。通过标准化的 `.ct` 文件格式，ContextHub 能够：

- 📝 **结构化存储**：以JSON格式存储会话信息，包含完整的元数据和对话历史
- 🔍 **智能关联**：自动发现和关联相关的上下文信息
- ⚡ **性能优化**：智能压缩和优化上下文，确保模型发挥最佳性能
- 🛡️ **格式验证**：完整的格式验证和错误检查机制
- 🔧 **易于扩展**：模块化设计，支持自定义扩展
- 💬 **AI对话功能**：支持多种AI模型的实时对话
- 🎨 **现代化UI**：GitHub风格的响应式前端界面
- 📤 **文件上传下载**：完整的文件管理功能

## 📦 快速安装

### pip 安装（推荐）
```bash
# 基础版本
pip install contexthub

# 包含Web服务器
pip install contexthub[server]

# 完整版本
pip install contexthub[all]
```

安装后即可使用：
```bash
ctx create file.py          # 创建上下文文件
contexthub stats            # 查看统计信息
contexthub-server           # 启动Web服务器
```

### 从源码安装

#### 自动安装
**macOS/Linux**
```bash
git clone <your-repo>
cd ContextHUb
./install.sh
```

**Windows**
```bash
git clone <your-repo>
cd ContextHUb  
install.bat
```

#### 手动安装
```bash
git clone <your-repo>
cd ContextHUb
pip install -r requirements.txt
```

📖 **详细安装指南**: [INSTALL.md](INSTALL.md)  
📚 **使用说明**: [CLI_USAGE.md](CLI_USAGE.md)

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

### 📁 文件管理功能

- **拖拽上传**：支持拖拽上传 `.ct` 文件
- **批量上传**：支持同时上传多个文件
- **格式验证**：自动验证文件格式和完整性
- **一键下载**：支持单个文件下载
- **文件预览**：在线查看文件内容
- **文件删除**：安全删除不需要的文件

### 🎨 现代化前端

- **React + TypeScript**：类型安全的前端架构
- **GitHub风格设计**：熟悉的界面风格
- **响应式布局**：适配各种屏幕尺寸
- **组件化开发**：模块化的组件设计

## 🏗️ 技术架构

### 后端 (Python + Flask)
```
app.py               # Flask API服务器
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
├── utils/          # 工具函数（包含API调用）
└── styles/         # 样式文件
```

## 🚀 快速开始

### 一键启动（推荐）

```bash
# 克隆项目
git clone https://github.com/River-Yang/ContextHub.git
cd ContextHub

# 一键启动前后端服务
./start_server.sh
```

启动后：
- 🌐 前端界面：http://localhost:3000
- 🔧 后端API：http://localhost:5000
- 📁 文件存储：./my_contexts/

### 手动启动

#### 1. 启动后端API服务器

```bash
# 安装Python依赖
pip install -r requirements.txt

# 启动后端服务
python app.py
```

后端将在 `http://localhost:5000` 启动

#### 2. 启动前端开发服务器

```bash
# 安装前端依赖
cd frontend
npm install

# 启动前端服务
npm run dev
```

前端将在 `http://localhost:3000` 启动

### Python API 使用

```python
from contexthub import ContextFile, ContextManager, ContextValidator, ContextUtils

# 创建上下文管理器
manager = ContextManager("./my_contexts")

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

### 1. 文件上传操作

#### 通过界面上传
1. 点击页面顶部的"上传"按钮
2. 在弹出的模态框中拖拽 `.ct` 文件或点击"浏览文件"
3. 支持同时选择多个文件
4. 系统会自动验证文件格式
5. 上传成功后文件会出现在列表中

#### API上传
```bash
curl -X POST http://localhost:5000/api/upload \
  -F "files=@example.ct" \
  -F "files=@another.ct"
```

### 2. 文件下载操作

#### 通过界面下载
1. 在文件列表中找到要下载的文件
2. 点击右上角的下载图标
3. 文件会自动下载到浏览器默认下载目录

#### API下载
```bash
curl -O http://localhost:5000/api/download/{context_id}
```

### 3. 文件管理

- **查看详情**：点击文件卡片或眼睛图标查看完整内容
- **删除文件**：点击垃圾桶图标删除文件
- **搜索过滤**：使用搜索框快速找到特定文件

### 4. AI对话功能

- 🤖 选择不同的AI模型
- ⚙️ 调整模型参数
- 💬 基于上下文进行对话
- 📝 保存对话历史

## 🔌 API接口文档

### 文件管理接口

- `GET /api/contexts` - 获取所有上下文文件列表
- `GET /api/contexts/<id>` - 获取特定上下文文件详情
- `POST /api/upload` - 上传文件（支持多文件）
- `GET /api/download/<id>` - 下载特定文件
- `DELETE /api/contexts/<id>` - 删除特定文件
- `POST /api/validate` - 验证文件格式

### 响应格式

```json
{
  "success": true,
  "data": {...},
  "message": "操作成功"
}
```

错误响应：
```json
{
  "success": false,
  "error": "错误描述"
}
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

### 项目结构

```
ContextHub/
├── app.py                  # Flask API服务器
├── start_server.sh         # 一键启动脚本
├── contexthub/            # Python库
├── frontend/              # React前端
├── my_contexts/           # 上传文件存储目录
├── requirements.txt       # Python依赖
└── README.md             # 项目文档
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
- ✅ 拖拽上传文件
- ✅ 批量文件上传
- ✅ 文件格式验证
- ✅ 一键文件下载
- ✅ 文件在线预览
- ✅ 文件删除管理
- ✅ AI对话功能
- ✅ 多模型支持
- ✅ 响应式UI设计
- ✅ TypeScript类型安全
- ✅ REST API接口
- ✅ 错误处理和用户反馈

## 🔮 未来规划

- [ ] 云端同步功能
- [ ] 团队协作支持
- [ ] 更多AI模型集成
- [ ] 移动端应用
- [ ] 插件系统
- [ ] 数据分析面板
- [ ] 文件版本控制
- [ ] 批量下载功能

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
