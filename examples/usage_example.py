#!/usr/bin/env python3
"""
ContextHub 使用示例

展示如何使用 ContextHub 库来管理 AI 模型的上下文。
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contexthub import ContextFile, ContextManager, ContextValidator, ContextUtils


def basic_usage_example():
    """基础使用示例"""
    print("=== ContextHub 基础使用示例 ===\n")
    
    # 1. 创建上下文管理器
    manager = ContextManager("./contexts")
    
    # 2. 创建新的上下文文件
    context = manager.create_context(
        session_name="AI助手对话示例",
        user_id="user-001",
        model_name="gpt-4",
        tags=["示例", "对话", "AI"]
    )
    
    print(f"创建了新会话: {context.data['metadata']['session_id']}")
    
    # 3. 添加对话消息
    context.add_message(
        role="user",
        content="你好，我想了解如何设计一个上下文管理系统",
        confidence=0.95,
        context_relevance=0.9
    )
    
    context.add_message(
        role="assistant",
        content="很高兴为您介绍上下文管理系统的设计。一个好的上下文管理系统应该包含以下几个核心组件：1. 结构化数据存储 2. 元数据管理 3. 上下文关联 4. 性能优化",
        confidence=0.92,
        context_relevance=0.85
    )
    
    context.add_message(
        role="user",
        content="能详细说明一下结构化数据存储吗？",
        confidence=0.9,
        context_relevance=0.8
    )
    
    context.add_message(
        role="assistant",
        content="结构化数据存储是上下文管理的核心。我们使用JSON格式来存储会话信息，包括：- 会话元数据（ID、时间、用户信息）- 对话历史（消息、角色、时间戳）- 模型状态（参数、配置）- 性能指标（响应时间、token使用等）",
        confidence=0.88,
        context_relevance=0.9
    )
    
    # 4. 更新摘要和关键点
    context.update_summary("讨论了上下文管理系统的设计，重点探讨了结构化数据存储的重要性")
    context.add_key_point("结构化数据存储是上下文管理的核心")
    context.add_key_point("JSON格式便于存储和解析")
    context.add_key_point("元数据管理有助于会话追踪")
    
    # 5. 保存上下文
    context.save()
    print(f"上下文已保存到: {context.file_path}")
    
    return context


def validation_example():
    """验证示例"""
    print("\n=== 上下文验证示例 ===\n")
    
    # 创建验证器
    validator = ContextValidator()
    
    # 创建一个有效的上下文
    context = ContextFile()
    context.set_user_info("user-001", "验证测试")
    context.set_model_info("gpt-4")
    
    # 验证上下文
    is_valid, errors, warnings = validator.validate_file(context.data)
    
    print("验证结果:")
    print(f"是否有效: {is_valid}")
    print(f"错误数量: {len(errors)}")
    print(f"警告数量: {len(warnings)}")
    
    if errors:
        print("\n错误:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("\n警告:")
        for warning in warnings:
            print(f"  - {warning}")
    
    # 打印详细验证报告
    print("\n" + validator.get_validation_report())


def utils_example():
    """工具类使用示例"""
    print("\n=== 工具类使用示例 ===\n")
    
    # 创建测试上下文
    context = ContextFile()
    context.set_user_info("user-001", "工具测试")
    context.set_model_info("gpt-4")
    
    # 添加一些测试消息
    context.add_message("user", "这是一个测试消息")
    context.add_message("assistant", "这是AI的回复，包含一些重要信息和建议")
    context.add_message("user", "谢谢你的帮助")
    
    # 1. 生成会话ID
    session_id = ContextUtils.generate_session_id("test")
    print(f"生成的会话ID: {session_id}")
    
    # 2. 估算token数量
    text = "这是一个测试文本，用于估算token数量"
    tokens = ContextUtils.estimate_tokens(text)
    print(f"文本token估算: {tokens}")
    
    # 3. 计算上下文哈希
    context_hash = ContextUtils.calculate_context_hash(context.data)
    print(f"上下文哈希: {context_hash[:16]}...")
    
    # 4. 提取关键点
    key_points = ContextUtils.extract_key_points(context.get_conversation())
    print(f"提取的关键点: {key_points}")
    
    # 5. 生成摘要
    summary = ContextUtils.generate_summary(context.get_conversation())
    print(f"生成的摘要: {summary}")
    
    # 6. 计算对话指标
    metrics = ContextUtils.calculate_conversation_metrics(context.get_conversation())
    print(f"对话指标: {metrics}")
    
    # 7. 导出为Markdown
    markdown = ContextUtils.export_to_markdown(context.data)
    print(f"Markdown导出长度: {len(markdown)} 字符")


def advanced_features_example():
    """高级功能示例"""
    print("\n=== 高级功能示例 ===\n")
    
    # 创建上下文管理器
    manager = ContextManager("./contexts")
    
    # 创建多个上下文文件
    context1 = manager.create_context("项目讨论1", "user-001", tags=["项目", "设计"])
    context1.add_message("user", "我们需要设计一个用户界面")
    context1.add_message("assistant", "建议使用现代化的设计语言，考虑用户体验")
    context1.save()
    
    context2 = manager.create_context("项目讨论2", "user-001", tags=["项目", "实现"])
    context2.add_message("user", "如何实现这个功能？")
    context2.add_message("assistant", "可以使用React框架，配合TypeScript")
    context2.save()
    
    # 列出所有上下文
    contexts = manager.list_contexts()
    print(f"找到 {len(contexts)} 个上下文文件:")
    for ctx in contexts:
        print(f"  - {ctx['session_name']} ({ctx['session_id']})")
    
    # 查找相关上下文
    related = ContextUtils.find_related_contexts(
        context1.data, 
        search_dir="./contexts",
        min_similarity=0.1
    )
    print(f"\n找到 {len(related)} 个相关上下文")
    
    # 优化上下文
    optimized = ContextUtils.optimize_context_for_model(
        context1.data,
        max_tokens=100,
        model_name="gpt-4"
    )
    print(f"优化后的上下文包含 {len(optimized['context']['conversation'])} 条消息")
    
    # 合并上下文
    merged = ContextUtils.merge_contexts([context1.data, context2.data], "append")
    print(f"合并后的上下文包含 {len(merged['context']['conversation'])} 条消息")


def main():
    """主函数"""
    print("ContextHub 使用示例")
    print("=" * 50)
    
    try:
        # 基础使用示例
        context = basic_usage_example()
        
        # 验证示例
        validation_example()
        
        # 工具类示例
        utils_example()
        
        # 高级功能示例
        advanced_features_example()
        
        print("\n=== 示例完成 ===")
        print("所有示例都已成功运行！")
        
    except Exception as e:
        print(f"运行示例时出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 