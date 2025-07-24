# ContextHub (.ct) 文件格式规范

## 概述
`.ct` 文件是 ContextHub 项目的标准上下文管理文件格式，用于存储和管理 AI 模型的会话上下文信息。该格式设计为结构化、可扩展且易于解析的 JSON 格式。

## 文件结构

### 1. 文件头 (Header)
```json
{
  "version": "1.0.0",
  "format": "contexthub",
  "created_at": "2024-01-01T00:00:00Z",
  "last_modified": "2024-01-01T00:00:00Z",
  "encoding": "utf-8"
}
```

### 2. 元数据 (Metadata)
```json
{
  "metadata": {
    "session_id": "unique-session-identifier",
    "model_info": {
      "name": "gpt-4",
      "version": "latest",
      "provider": "openai"
    },
    "user_info": {
      "user_id": "user-123",
      "session_name": "项目讨论",
      "tags": ["编程", "AI", "上下文管理"]
    },
    "context_type": "conversation",
    "priority": "high",
    "expires_at": "2024-12-31T23:59:59Z"
  }
}
```

### 3. 上下文内容 (Context Content)
```json
{
  "context": {
    "summary": "本次会话主要讨论了上下文管理系统的设计",
    "key_points": [
      "上下文格式标准化",
      "会话历史管理",
      "模型性能优化"
    ],
    "conversation": [
      {
        "id": "msg-001",
        "timestamp": "2024-01-01T10:00:00Z",
        "role": "user",
        "content": "用户输入的内容",
        "tokens": 150,
        "metadata": {
          "confidence": 0.95,
          "context_relevance": 0.9
        }
      },
      {
        "id": "msg-002",
        "timestamp": "2024-01-01T10:01:00Z",
        "role": "assistant",
        "content": "AI 助手的回复内容",
        "tokens": 300,
        "metadata": {
          "confidence": 0.92,
          "context_relevance": 0.85,
          "sources": ["source1", "source2"]
        }
      }
    ]
  }
}
```

### 4. 关联上下文 (Related Contexts)
```json
{
  "related_contexts": [
    {
      "context_id": "ctx-001",
      "relationship": "prerequisite",
      "relevance_score": 0.8,
      "file_path": "./related_context.ct"
    }
  ]
}
```

### 5. 模型状态 (Model State)
```json
{
  "model_state": {
    "temperature": 0.7,
    "max_tokens": 2000,
    "system_prompt": "你是一个专业的上下文管理助手",
    "context_window_size": 4000,
    "memory_usage": {
      "current": 1500,
      "max": 4000,
      "utilization": 0.375
    }
  }
}
```

### 6. 性能指标 (Performance Metrics)
```json
{
  "performance": {
    "response_time": 2.5,
    "token_efficiency": 0.85,
    "context_retention": 0.92,
    "user_satisfaction": 4.5
  }
}
```

## 完整示例

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
      "session_name": "上下文管理系统设计",
      "tags": ["系统设计", "AI", "上下文管理"]
    },
    "context_type": "conversation",
    "priority": "high",
    "expires_at": "2024-12-31T23:59:59Z"
  },
  
  "context": {
    "summary": "讨论上下文管理系统的核心功能和设计原则",
    "key_points": [
      "标准化上下文格式",
      "会话历史管理",
      "模型性能优化",
      "可扩展性设计"
    ],
    "conversation": [
      {
        "id": "msg-001",
        "timestamp": "2024-01-01T10:00:00Z",
        "role": "user",
        "content": "我需要设计一个上下文管理系统，能够有效管理AI模型的会话历史",
        "tokens": 25,
        "metadata": {
          "confidence": 0.95,
          "context_relevance": 0.9
        }
      },
      {
        "id": "msg-002",
        "timestamp": "2024-01-01T10:01:00Z",
        "role": "assistant",
        "content": "我建议采用结构化的JSON格式来存储上下文信息，包含会话元数据、对话历史、模型状态等关键信息。这样可以确保上下文的完整性和可追溯性。",
        "tokens": 45,
        "metadata": {
          "confidence": 0.92,
          "context_relevance": 0.85,
          "sources": ["best_practices", "ai_context_management"]
        }
      }
    ]
  },
  
  "related_contexts": [
    {
      "context_id": "ctx-001",
      "relationship": "prerequisite",
      "relevance_score": 0.8,
      "file_path": "./previous_discussion.ct"
    }
  ],
  
  "model_state": {
    "temperature": 0.7,
    "max_tokens": 2000,
    "system_prompt": "你是一个专业的上下文管理助手，擅长系统设计和最佳实践建议",
    "context_window_size": 4000,
    "memory_usage": {
      "current": 1500,
      "max": 4000,
      "utilization": 0.375
    }
  },
  
  "performance": {
    "response_time": 2.5,
    "token_efficiency": 0.85,
    "context_retention": 0.92,
    "user_satisfaction": 4.5
  }
}
```

## 字段说明

### 必需字段
- `version`: 文件格式版本
- `format`: 文件格式标识符
- `created_at`: 创建时间
- `last_modified`: 最后修改时间
- `metadata`: 会话元数据
- `context`: 上下文内容

### 可选字段
- `related_contexts`: 关联上下文
- `model_state`: 模型状态
- `performance`: 性能指标

## 扩展性
该格式支持通过添加新的顶级字段来扩展功能，同时保持向后兼容性。

## 文件命名规范
- 格式: `{session_id}_{timestamp}.ct`
- 示例: `session-2024-001_20240101T100000Z.ct` 