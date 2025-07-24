"""
ContextHub 验证器模块

提供 .ct 文件格式验证和内容检查功能。
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import re


class ContextValidator:
    """ContextHub .ct 文件验证器"""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_file(self, data: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """
        验证 .ct 文件的完整结构
        
        Args:
            data: 要验证的数据字典
            
        Returns:
            (是否有效, 错误列表, 警告列表)
        """
        self.errors = []
        self.warnings = []
        
        # 验证必需字段
        self._validate_required_fields(data)
        
        # 验证文件头
        if "version" in data:
            self._validate_header(data)
        
        # 验证元数据
        if "metadata" in data:
            self._validate_metadata(data["metadata"])
        
        # 验证上下文内容
        if "context" in data:
            self._validate_context(data["context"])
        
        # 验证关联上下文
        if "related_contexts" in data:
            self._validate_related_contexts(data["related_contexts"])
        
        # 验证模型状态
        if "model_state" in data:
            self._validate_model_state(data["model_state"])
        
        # 验证性能指标
        if "performance" in data:
            self._validate_performance(data["performance"])
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_required_fields(self, data: Dict[str, Any]) -> None:
        """验证必需字段"""
        required_fields = ["version", "format", "created_at", "last_modified", "metadata", "context"]
        
        for field in required_fields:
            if field not in data:
                self.errors.append(f"缺少必需字段: {field}")
    
    def _validate_header(self, data: Dict[str, Any]) -> None:
        """验证文件头"""
        # 验证版本格式
        version = data.get("version")
        if version and not re.match(r"^\d+\.\d+\.\d+$", version):
            self.errors.append("版本格式无效，应为 x.y.z 格式")
        
        # 验证格式标识符
        if data.get("format") != "contexthub":
            self.errors.append("格式标识符必须为 'contexthub'")
        
        # 验证时间戳格式
        for time_field in ["created_at", "last_modified"]:
            if time_field in data:
                if not self._is_valid_iso_timestamp(data[time_field]):
                    self.errors.append(f"{time_field} 时间戳格式无效")
        
        # 验证编码
        if "encoding" in data and data["encoding"] != "utf-8":
            self.warnings.append("建议使用 UTF-8 编码")
    
    def _validate_metadata(self, metadata: Dict[str, Any]) -> None:
        """验证元数据"""
        required_metadata = ["session_id", "model_info", "user_info"]
        
        for field in required_metadata:
            if field not in metadata:
                self.errors.append(f"元数据缺少必需字段: {field}")
        
        # 验证会话ID
        session_id = metadata.get("session_id")
        if session_id and not re.match(r"^[a-zA-Z0-9_-]+$", session_id):
            self.errors.append("会话ID只能包含字母、数字、下划线和连字符")
        
        # 验证模型信息
        if "model_info" in metadata:
            self._validate_model_info(metadata["model_info"])
        
        # 验证用户信息
        if "user_info" in metadata:
            self._validate_user_info(metadata["user_info"])
        
        # 验证优先级
        priority = metadata.get("priority")
        if priority and priority not in ["low", "medium", "high", "critical"]:
            self.warnings.append("优先级应为 low/medium/high/critical 之一")
        
        # 验证过期时间
        expires_at = metadata.get("expires_at")
        if expires_at and not self._is_valid_iso_timestamp(expires_at):
            self.errors.append("过期时间格式无效")
    
    def _validate_model_info(self, model_info: Dict[str, Any]) -> None:
        """验证模型信息"""
        required_fields = ["name", "version", "provider"]
        
        for field in required_fields:
            if field not in model_info:
                self.errors.append(f"模型信息缺少必需字段: {field}")
        
        # 验证模型名称
        name = model_info.get("name")
        if name and name == "unknown":
            self.warnings.append("模型名称未指定")
    
    def _validate_user_info(self, user_info: Dict[str, Any]) -> None:
        """验证用户信息"""
        required_fields = ["user_id", "session_name"]
        
        for field in required_fields:
            if field not in user_info:
                self.errors.append(f"用户信息缺少必需字段: {field}")
        
        # 验证会话名称
        session_name = user_info.get("session_name")
        if session_name and len(session_name.strip()) == 0:
            self.errors.append("会话名称不能为空")
        
        # 验证标签
        tags = user_info.get("tags", [])
        if not isinstance(tags, list):
            self.errors.append("标签必须是列表格式")
        else:
            for tag in tags:
                if not isinstance(tag, str):
                    self.errors.append("标签必须是字符串")
    
    def _validate_context(self, context: Dict[str, Any]) -> None:
        """验证上下文内容"""
        required_fields = ["summary", "key_points", "conversation"]
        
        for field in required_fields:
            if field not in context:
                self.errors.append(f"上下文缺少必需字段: {field}")
        
        # 验证摘要
        summary = context.get("summary")
        if summary and not isinstance(summary, str):
            self.errors.append("摘要必须是字符串")
        
        # 验证关键点
        key_points = context.get("key_points", [])
        if not isinstance(key_points, list):
            self.errors.append("关键点必须是列表格式")
        else:
            for point in key_points:
                if not isinstance(point, str):
                    self.errors.append("关键点必须是字符串")
        
        # 验证对话历史
        conversation = context.get("conversation", [])
        if not isinstance(conversation, list):
            self.errors.append("对话历史必须是列表格式")
        else:
            for i, message in enumerate(conversation):
                self._validate_message(message, i)
    
    def _validate_message(self, message: Dict[str, Any], index: int) -> None:
        """验证单条消息"""
        required_fields = ["id", "timestamp", "role", "content"]
        
        for field in required_fields:
            if field not in message:
                self.errors.append(f"消息 {index} 缺少必需字段: {field}")
        
        # 验证消息ID
        msg_id = message.get("id")
        if msg_id and not re.match(r"^msg-\d+$", msg_id):
            self.errors.append(f"消息 {index} ID 格式无效，应为 msg-xxx 格式")
        
        # 验证时间戳
        timestamp = message.get("timestamp")
        if timestamp and not self._is_valid_iso_timestamp(timestamp):
            self.errors.append(f"消息 {index} 时间戳格式无效")
        
        # 验证角色
        role = message.get("role")
        if role and role not in ["user", "assistant", "system"]:
            self.errors.append(f"消息 {index} 角色无效，应为 user/assistant/system")
        
        # 验证内容
        content = message.get("content")
        if content and not isinstance(content, str):
            self.errors.append(f"消息 {index} 内容必须是字符串")
        
        # 验证token数量
        tokens = message.get("tokens")
        if tokens is not None and not isinstance(tokens, int):
            self.errors.append(f"消息 {index} token数量必须是整数")
        
        # 验证元数据
        metadata = message.get("metadata", {})
        if not isinstance(metadata, dict):
            self.errors.append(f"消息 {index} 元数据必须是字典格式")
        else:
            self._validate_message_metadata(metadata, index)
    
    def _validate_message_metadata(self, metadata: Dict[str, Any], msg_index: int) -> None:
        """验证消息元数据"""
        # 验证置信度
        confidence = metadata.get("confidence")
        if confidence is not None:
            if not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
                self.errors.append(f"消息 {msg_index} 置信度必须在 0-1 之间")
        
        # 验证上下文相关性
        context_relevance = metadata.get("context_relevance")
        if context_relevance is not None:
            if not isinstance(context_relevance, (int, float)) or not 0 <= context_relevance <= 1:
                self.errors.append(f"消息 {msg_index} 上下文相关性必须在 0-1 之间")
    
    def _validate_related_contexts(self, related_contexts: List[Dict[str, Any]]) -> None:
        """验证关联上下文"""
        if not isinstance(related_contexts, list):
            self.errors.append("关联上下文必须是列表格式")
            return
        
        for i, context in enumerate(related_contexts):
            if not isinstance(context, dict):
                self.errors.append(f"关联上下文 {i} 必须是字典格式")
                continue
            
            required_fields = ["context_id", "relationship", "relevance_score"]
            for field in required_fields:
                if field not in context:
                    self.errors.append(f"关联上下文 {i} 缺少必需字段: {field}")
            
            # 验证相关性分数
            relevance_score = context.get("relevance_score")
            if relevance_score is not None:
                if not isinstance(relevance_score, (int, float)) or not 0 <= relevance_score <= 1:
                    self.errors.append(f"关联上下文 {i} 相关性分数必须在 0-1 之间")
    
    def _validate_model_state(self, model_state: Dict[str, Any]) -> None:
        """验证模型状态"""
        # 验证温度
        temperature = model_state.get("temperature")
        if temperature is not None:
            if not isinstance(temperature, (int, float)) or not 0 <= temperature <= 2:
                self.warnings.append("温度值通常应在 0-2 之间")
        
        # 验证最大token数
        max_tokens = model_state.get("max_tokens")
        if max_tokens is not None:
            if not isinstance(max_tokens, int) or max_tokens <= 0:
                self.errors.append("最大token数必须是正整数")
        
        # 验证系统提示
        system_prompt = model_state.get("system_prompt")
        if system_prompt and not isinstance(system_prompt, str):
            self.errors.append("系统提示必须是字符串")
        
        # 验证内存使用
        memory_usage = model_state.get("memory_usage", {})
        if isinstance(memory_usage, dict):
            current = memory_usage.get("current")
            max_memory = memory_usage.get("max")
            
            if current is not None and not isinstance(current, int):
                self.errors.append("当前内存使用必须是整数")
            
            if max_memory is not None and not isinstance(max_memory, int):
                self.errors.append("最大内存必须是整数")
            
            if current is not None and max_memory is not None:
                if current > max_memory:
                    self.errors.append("当前内存使用不能超过最大内存")
    
    def _validate_performance(self, performance: Dict[str, Any]) -> None:
        """验证性能指标"""
        # 验证响应时间
        response_time = performance.get("response_time")
        if response_time is not None:
            if not isinstance(response_time, (int, float)) or response_time < 0:
                self.errors.append("响应时间必须是非负数")
        
        # 验证token效率
        token_efficiency = performance.get("token_efficiency")
        if token_efficiency is not None:
            if not isinstance(token_efficiency, (int, float)) or not 0 <= token_efficiency <= 1:
                self.errors.append("token效率必须在 0-1 之间")
        
        # 验证上下文保留率
        context_retention = performance.get("context_retention")
        if context_retention is not None:
            if not isinstance(context_retention, (int, float)) or not 0 <= context_retention <= 1:
                self.errors.append("上下文保留率必须在 0-1 之间")
        
        # 验证用户满意度
        user_satisfaction = performance.get("user_satisfaction")
        if user_satisfaction is not None:
            if not isinstance(user_satisfaction, (int, float)) or not 0 <= user_satisfaction <= 5:
                self.errors.append("用户满意度必须在 0-5 之间")
    
    def _is_valid_iso_timestamp(self, timestamp: str) -> bool:
        """验证ISO时间戳格式"""
        try:
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return True
        except ValueError:
            return False
    
    def get_validation_report(self) -> str:
        """生成验证报告"""
        report = []
        report.append("ContextHub 文件验证报告")
        report.append("=" * 40)
        
        if self.errors:
            report.append(f"\n错误 ({len(self.errors)}):")
            for error in self.errors:
                report.append(f"❌ {error}")
        
        if self.warnings:
            report.append(f"\n警告 ({len(self.warnings)}):")
            for warning in self.warnings:
                report.append(f"⚠️  {warning}")
        
        if not self.errors and not self.warnings:
            report.append("\n✅ 文件验证通过，没有发现错误或警告")
        
        return "\n".join(report) 