"""
ContextHub 工具模块

提供各种实用的上下文处理功能。
"""

import json
import hashlib
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
import re
from pathlib import Path


class ContextUtils:
    """ContextHub 工具类"""
    
    @staticmethod
    def generate_session_id(prefix: str = "session") -> str:
        """
        生成唯一的会话ID
        
        Args:
            prefix: ID前缀
            
        Returns:
            唯一的会话ID
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = hashlib.md5(f"{timestamp}".encode()).hexdigest()[:6]
        return f"{prefix}-{timestamp}-{random_suffix}"
    
    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        估算文本的token数量
        
        Args:
            text: 要估算的文本
            
        Returns:
            估算的token数量
        """
        # 简单的token估算：按空格分割单词
        words = text.split()
        return len(words)
    
    @staticmethod
    def calculate_context_hash(context_data: Dict[str, Any]) -> str:
        """
        计算上下文数据的哈希值
        
        Args:
            context_data: 上下文数据
            
        Returns:
            哈希值
        """
        # 移除可变字段
        data_copy = context_data.copy()
        data_copy.pop("last_modified", None)
        data_copy.pop("created_at", None)
        
        # 转换为JSON字符串并计算哈希
        json_str = json.dumps(data_copy, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(json_str.encode('utf-8')).hexdigest()
    
    @staticmethod
    def extract_key_points(conversation: List[Dict[str, Any]], 
                          min_relevance: float = 0.7) -> List[str]:
        """
        从对话中提取关键点
        
        Args:
            conversation: 对话历史
            min_relevance: 最小相关性阈值
            
        Returns:
            关键点列表
        """
        key_points = []
        
        for message in conversation:
            if message.get("role") == "assistant":
                content = message.get("content", "")
                relevance = message.get("metadata", {}).get("context_relevance", 0.5)
                
                if relevance >= min_relevance:
                    # 简单的关键点提取：提取包含关键词的句子
                    sentences = re.split(r'[。！？.!?]', content)
                    for sentence in sentences:
                        sentence = sentence.strip()
                        if len(sentence) > 10 and any(keyword in sentence for keyword in 
                                                     ["建议", "应该", "需要", "重要", "关键", "必须"]):
                            key_points.append(sentence)
        
        return list(set(key_points))  # 去重
    
    @staticmethod
    def generate_summary(conversation: List[Dict[str, Any]], 
                        max_length: int = 200) -> str:
        """
        生成对话摘要
        
        Args:
            conversation: 对话历史
            max_length: 最大摘要长度
            
        Returns:
            生成的摘要
        """
        if not conversation:
            return ""
        
        # 提取用户的主要问题
        user_messages = [msg for msg in conversation if msg.get("role") == "user"]
        if user_messages:
            main_question = user_messages[0].get("content", "")
            if len(main_question) > max_length:
                main_question = main_question[:max_length] + "..."
            return main_question
        
        return "对话摘要生成失败"
    
    @staticmethod
    def calculate_conversation_metrics(conversation: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        计算对话指标
        
        Args:
            conversation: 对话历史
            
        Returns:
            对话指标字典
        """
        if not conversation:
            return {
                "total_messages": 0,
                "user_messages": 0,
                "assistant_messages": 0,
                "total_tokens": 0,
                "average_tokens_per_message": 0,
                "conversation_duration": 0
            }
        
        user_messages = [msg for msg in conversation if msg.get("role") == "user"]
        assistant_messages = [msg for msg in conversation if msg.get("role") == "assistant"]
        
        total_tokens = sum(msg.get("tokens", 0) for msg in conversation)
        avg_tokens = total_tokens / len(conversation) if conversation else 0
        
        # 计算对话时长
        duration = 0
        if len(conversation) >= 2:
            first_time = datetime.fromisoformat(conversation[0]["timestamp"].replace('Z', '+00:00'))
            last_time = datetime.fromisoformat(conversation[-1]["timestamp"].replace('Z', '+00:00'))
            duration = (last_time - first_time).total_seconds()
        
        return {
            "total_messages": len(conversation),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "total_tokens": total_tokens,
            "average_tokens_per_message": round(avg_tokens, 2),
            "conversation_duration": round(duration, 2)
        }
    
    @staticmethod
    def find_related_contexts(context_data: Dict[str, Any], 
                            search_dir: str = "./contexts",
                            min_similarity: float = 0.3) -> List[Dict[str, Any]]:
        """
        查找相关上下文
        
        Args:
            context_data: 当前上下文数据
            search_dir: 搜索目录
            min_similarity: 最小相似度阈值
            
        Returns:
            相关上下文列表
        """
        related_contexts = []
        search_path = Path(search_dir)
        
        if not search_path.exists():
            return related_contexts
        
        current_tags = set(context_data.get("metadata", {}).get("user_info", {}).get("tags", []))
        current_summary = context_data.get("context", {}).get("summary", "")
        
        for ct_file in search_path.glob("*.ct"):
            try:
                with open(ct_file, 'r', encoding='utf-8') as f:
                    other_context = json.load(f)
                
                # 计算相似度
                other_tags = set(other_context.get("metadata", {}).get("user_info", {}).get("tags", []))
                other_summary = other_context.get("context", {}).get("summary", "")
                
                # 标签相似度
                tag_similarity = len(current_tags & other_tags) / len(current_tags | other_tags) if current_tags | other_tags else 0
                
                # 摘要相似度（简单的关键词匹配）
                current_words = set(re.findall(r'\w+', current_summary.lower()))
                other_words = set(re.findall(r'\w+', other_summary.lower()))
                summary_similarity = len(current_words & other_words) / len(current_words | other_words) if current_words | other_words else 0
                
                # 综合相似度
                overall_similarity = (tag_similarity + summary_similarity) / 2
                
                if overall_similarity >= min_similarity:
                    related_contexts.append({
                        "context_id": other_context.get("metadata", {}).get("session_id"),
                        "relationship": "similar",
                        "relevance_score": overall_similarity,
                        "file_path": str(ct_file),
                        "similarity_breakdown": {
                            "tag_similarity": tag_similarity,
                            "summary_similarity": summary_similarity
                        }
                    })
                    
            except Exception as e:
                print(f"读取文件 {ct_file} 时出错: {e}")
        
        # 按相似度排序
        related_contexts.sort(key=lambda x: x["relevance_score"], reverse=True)
        return related_contexts
    
    @staticmethod
    def optimize_context_for_model(context_data: Dict[str, Any], 
                                 max_tokens: int = 4000,
                                 model_name: str = "gpt-4") -> Dict[str, Any]:
        """
        为模型优化上下文数据
        
        Args:
            context_data: 原始上下文数据
            max_tokens: 最大token数
            model_name: 模型名称
            
        Returns:
            优化后的上下文数据
        """
        optimized = context_data.copy()
        conversation = optimized.get("context", {}).get("conversation", [])
        
        if not conversation:
            return optimized
        
        # 计算当前token数
        current_tokens = sum(msg.get("tokens", 0) for msg in conversation)
        
        if current_tokens <= max_tokens:
            return optimized
        
        # 需要压缩上下文
        # 策略：保留最重要的消息（基于相关性分数）
        sorted_messages = sorted(conversation, 
                               key=lambda x: x.get("metadata", {}).get("context_relevance", 0.5),
                               reverse=True)
        
        compressed_messages = []
        total_tokens = 0
        
        for message in sorted_messages:
            message_tokens = message.get("tokens", 0)
            if total_tokens + message_tokens <= max_tokens:
                compressed_messages.append(message)
                total_tokens += message_tokens
            else:
                break
        
        # 按时间顺序重新排列
        compressed_messages.sort(key=lambda x: x["timestamp"])
        
        # 更新上下文
        optimized["context"]["conversation"] = compressed_messages
        
        # 添加压缩信息
        if "extensions" not in optimized:
            optimized["extensions"] = {}
        optimized["extensions"]["compression_info"] = {
            "original_tokens": current_tokens,
            "compressed_tokens": total_tokens,
            "compression_ratio": round(total_tokens / current_tokens, 2),
            "messages_kept": len(compressed_messages),
            "messages_removed": len(conversation) - len(compressed_messages)
        }
        
        return optimized
    
    @staticmethod
    def export_to_markdown(context_data: Dict[str, Any]) -> str:
        """
        导出上下文为Markdown格式
        
        Args:
            context_data: 上下文数据
            
        Returns:
            Markdown格式的文本
        """
        lines = []
        
        # 标题
        session_name = context_data.get("metadata", {}).get("user_info", {}).get("session_name", "未命名会话")
        lines.append(f"# {session_name}")
        lines.append("")
        
        # 基本信息
        metadata = context_data.get("metadata", {})
        lines.append("## 基本信息")
        lines.append(f"- **会话ID**: {metadata.get('session_id', 'N/A')}")
        lines.append(f"- **创建时间**: {context_data.get('created_at', 'N/A')}")
        lines.append(f"- **最后修改**: {context_data.get('last_modified', 'N/A')}")
        lines.append(f"- **模型**: {metadata.get('model_info', {}).get('name', 'N/A')}")
        lines.append("")
        
        # 摘要
        summary = context_data.get("context", {}).get("summary", "")
        if summary:
            lines.append("## 摘要")
            lines.append(summary)
            lines.append("")
        
        # 关键点
        key_points = context_data.get("context", {}).get("key_points", [])
        if key_points:
            lines.append("## 关键点")
            for point in key_points:
                lines.append(f"- {point}")
            lines.append("")
        
        # 对话历史
        conversation = context_data.get("context", {}).get("conversation", [])
        if conversation:
            lines.append("## 对话历史")
            for msg in conversation:
                role = msg.get("role", "unknown").upper()
                content = msg.get("content", "")
                timestamp = msg.get("timestamp", "")
                
                lines.append(f"### {role} ({timestamp})")
                lines.append(content)
                lines.append("")
        
        return "\n".join(lines)
    
    @staticmethod
    def merge_contexts(contexts: List[Dict[str, Any]], 
                      merge_strategy: str = "append") -> Dict[str, Any]:
        """
        合并多个上下文
        
        Args:
            contexts: 要合并的上下文列表
            merge_strategy: 合并策略 ('append', 'merge', 'replace')
            
        Returns:
            合并后的上下文
        """
        if not contexts:
            return {}
        
        if len(contexts) == 1:
            return contexts[0].copy()
        
        # 以第一个上下文为基础
        merged = contexts[0].copy()
        
        if merge_strategy == "append":
            # 简单追加对话
            all_conversations = []
            for ctx in contexts:
                all_conversations.extend(ctx.get("context", {}).get("conversation", []))
            
            # 按时间排序
            all_conversations.sort(key=lambda x: x["timestamp"])
            merged["context"]["conversation"] = all_conversations
            
        elif merge_strategy == "merge":
            # 智能合并
            all_key_points = set()
            all_conversations = []
            
            for ctx in contexts:
                key_points = ctx.get("context", {}).get("key_points", [])
                all_key_points.update(key_points)
                
                conversations = ctx.get("context", {}).get("conversation", [])
                all_conversations.extend(conversations)
            
            merged["context"]["key_points"] = list(all_key_points)
            merged["context"]["conversation"] = all_conversations
            
        # 更新元数据
        merged["metadata"]["session_id"] = ContextUtils.generate_session_id("merged")
        merged["created_at"] = datetime.now(timezone.utc).isoformat()
        merged["last_modified"] = datetime.now(timezone.utc).isoformat()
        
        return merged 