"""
ContextHub 核心模块

提供 .ct 文件的基础操作和管理功能。
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
import uuid


class ContextFile:
    """ContextHub .ct 文件的核心类"""
    
    def __init__(self, file_path: Optional[str] = None):
        """
        初始化 ContextFile
        
        Args:
            file_path: .ct 文件路径，如果为 None 则创建新的上下文文件
        """
        self.file_path = file_path
        self.data = self._create_default_structure()
        
        if file_path and os.path.exists(file_path):
            self.load(file_path)
    
    def _create_default_structure(self) -> Dict[str, Any]:
        """创建默认的 .ct 文件结构"""
        return {
            "version": "1.0.0",
            "format": "contexthub",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "last_modified": datetime.now(timezone.utc).isoformat(),
            "encoding": "utf-8",
            "metadata": {
                "session_id": f"session-{uuid.uuid4().hex[:8]}",
                "model_info": {
                    "name": "unknown",
                    "version": "latest",
                    "provider": "unknown"
                },
                "user_info": {
                    "user_id": "unknown",
                    "session_name": "未命名会话",
                    "tags": []
                },
                "context_type": "conversation",
                "priority": "medium",
                "expires_at": None
            },
            "context": {
                "summary": "",
                "key_points": [],
                "conversation": []
            }
        }
    
    def load(self, file_path: str) -> None:
        """
        从文件加载 .ct 数据
        
        Args:
            file_path: .ct 文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.file_path = file_path
        except Exception as e:
            raise ValueError(f"无法加载 .ct 文件: {e}")
    
    def save(self, file_path: Optional[str] = None) -> None:
        """
        保存 .ct 数据到文件
        
        Args:
            file_path: 保存路径，如果为 None 则使用当前文件路径
        """
        save_path = file_path or self.file_path
        if not save_path:
            raise ValueError("必须指定保存路径")
        
        # 更新最后修改时间
        self.data["last_modified"] = datetime.now(timezone.utc).isoformat()
        
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            
            self.file_path = save_path
        except Exception as e:
            raise ValueError(f"无法保存 .ct 文件: {e}")
    
    def add_message(self, role: str, content: str, **metadata) -> str:
        """
        添加消息到对话历史
        
        Args:
            role: 消息角色 ('user' 或 'assistant')
            content: 消息内容
            **metadata: 额外的元数据
            
        Returns:
            消息ID
        """
        message_id = f"msg-{len(self.data['context']['conversation']) + 1:03d}"
        
        message = {
            "id": message_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "role": role,
            "content": content,
            "tokens": len(content.split()),  # 简单的token估算
            "metadata": {
                "confidence": metadata.get("confidence", 0.9),
                "context_relevance": metadata.get("context_relevance", 0.8),
                **{k: v for k, v in metadata.items() if k not in ["confidence", "context_relevance"]}
            }
        }
        
        self.data["context"]["conversation"].append(message)
        return message_id
    
    def update_summary(self, summary: str) -> None:
        """更新会话摘要"""
        self.data["context"]["summary"] = summary
    
    def add_key_point(self, key_point: str) -> None:
        """添加关键点"""
        if key_point not in self.data["context"]["key_points"]:
            self.data["context"]["key_points"].append(key_point)
    
    def set_model_info(self, name: str, version: str = "latest", provider: str = "unknown") -> None:
        """设置模型信息"""
        self.data["metadata"]["model_info"] = {
            "name": name,
            "version": version,
            "provider": provider
        }
    
    def set_user_info(self, user_id: str, session_name: str, tags: Optional[List[str]] = None) -> None:
        """设置用户信息"""
        self.data["metadata"]["user_info"] = {
            "user_id": user_id,
            "session_name": session_name,
            "tags": tags or []
        }
    
    def get_conversation(self) -> List[Dict[str, Any]]:
        """获取对话历史"""
        return self.data["context"]["conversation"]
    
    def get_summary(self) -> str:
        """获取会话摘要"""
        return self.data["context"]["summary"]
    
    def get_key_points(self) -> List[str]:
        """获取关键点列表"""
        return self.data["context"]["key_points"]
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return self.data.copy()


class ContextManager:
    """ContextHub 上下文管理器"""
    
    def __init__(self, storage_dir: str = "./contexts"):
        """
        初始化上下文管理器
        
        Args:
            storage_dir: 上下文文件存储目录
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.active_contexts: Dict[str, ContextFile] = {}
    
    def create_context(self, session_name: str, user_id: str = "default", 
                      model_name: str = "gpt-4", tags: Optional[List[str]] = None) -> ContextFile:
        """
        创建新的上下文文件
        
        Args:
            session_name: 会话名称
            user_id: 用户ID
            model_name: 模型名称
            tags: 标签列表
            
        Returns:
            新创建的 ContextFile 实例
        """
        context = ContextFile()
        context.set_user_info(user_id, session_name, tags)
        context.set_model_info(model_name)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{context.data['metadata']['session_id']}_{timestamp}.ct"
        file_path = self.storage_dir / filename
        
        context.save(str(file_path))
        
        # 添加到活跃上下文
        session_id = context.data["metadata"]["session_id"]
        self.active_contexts[session_id] = context
        
        return context
    
    def load_context(self, file_path: str) -> ContextFile:
        """
        加载现有的上下文文件
        
        Args:
            file_path: .ct 文件路径
            
        Returns:
            加载的 ContextFile 实例
        """
        context = ContextFile(file_path)
        session_id = context.data["metadata"]["session_id"]
        self.active_contexts[session_id] = context
        return context
    
    def get_context(self, session_id: str) -> Optional[ContextFile]:
        """获取活跃的上下文"""
        return self.active_contexts.get(session_id)
    
    def list_contexts(self) -> List[Dict[str, Any]]:
        """列出所有上下文文件"""
        contexts = []
        for ct_file in self.storage_dir.glob("*.ct"):
            try:
                context = ContextFile(str(ct_file))
                contexts.append({
                    "file_path": str(ct_file),
                    "session_id": context.data["metadata"]["session_id"],
                    "session_name": context.data["metadata"]["user_info"]["session_name"],
                    "created_at": context.data["created_at"],
                    "last_modified": context.data["last_modified"]
                })
            except Exception as e:
                print(f"无法读取文件 {ct_file}: {e}")
        
        return sorted(contexts, key=lambda x: x["last_modified"], reverse=True)
    
    def delete_context(self, session_id: str) -> bool:
        """
        删除上下文文件
        
        Args:
            session_id: 会话ID
            
        Returns:
            是否删除成功
        """
        context = self.active_contexts.get(session_id)
        if context and context.file_path:
            try:
                os.remove(context.file_path)
                del self.active_contexts[session_id]
                return True
            except Exception as e:
                print(f"删除文件失败: {e}")
                return False
        return False
    
    def export_context(self, session_id: str, format: str = "json") -> str:
        """
        导出上下文数据
        
        Args:
            session_id: 会话ID
            format: 导出格式 ('json', 'txt')
            
        Returns:
            导出的数据
        """
        context = self.get_context(session_id)
        if not context:
            raise ValueError(f"未找到会话: {session_id}")
        
        if format == "json":
            return json.dumps(context.to_dict(), ensure_ascii=False, indent=2)
        elif format == "txt":
            return self._export_to_text(context)
        else:
            raise ValueError(f"不支持的导出格式: {format}")
    
    def _export_to_text(self, context: ContextFile) -> str:
        """导出为文本格式"""
        lines = []
        lines.append(f"会话: {context.data['metadata']['user_info']['session_name']}")
        lines.append(f"创建时间: {context.data['created_at']}")
        lines.append(f"最后修改: {context.data['last_modified']}")
        lines.append("=" * 50)
        
        if context.data["context"]["summary"]:
            lines.append(f"摘要: {context.data['context']['summary']}")
            lines.append("")
        
        if context.data["context"]["key_points"]:
            lines.append("关键点:")
            for point in context.data["context"]["key_points"]:
                lines.append(f"- {point}")
            lines.append("")
        
        lines.append("对话历史:")
        for msg in context.data["context"]["conversation"]:
            lines.append(f"[{msg['timestamp']}] {msg['role'].upper()}: {msg['content']}")
            lines.append("")
        
        return "\n".join(lines) 