#!/usr/bin/env python3
"""
ContextHub 演示脚本
"""

from contexthub import ContextValidator, ContextUtils
import json

def main():
    print("=== ContextHub 功能演示 ===\n")
    
    # 加载一个上下文文件进行验证
    try:
        with open('contexts/session-0fb1b121_20250724_132410.ct', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("1. 上下文文件验证")
        print("-" * 30)
        
        # 验证文件
        validator = ContextValidator()
        is_valid, errors, warnings = validator.validate_file(data)
        
        print(f"验证结果: {'通过' if is_valid else '失败'}")
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
        
        print("\n2. 工具类功能演示")
        print("-" * 30)
        
        # 基本信息
        print(f"会话ID: {data['metadata']['session_id']}")
        print(f"会话名称: {data['metadata']['user_info']['session_name']}")
        print(f"模型: {data['metadata']['model_info']['name']}")
        print(f"标签: {', '.join(data['metadata']['user_info']['tags'])}")
        
        # 计算对话指标
        conversation = data['context']['conversation']
        metrics = ContextUtils.calculate_conversation_metrics(conversation)
        
        print(f"\n对话指标:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
        
        # 提取关键点
        key_points = ContextUtils.extract_key_points(conversation)
        print(f"\n提取的关键点:")
        for point in key_points:
            print(f"  - {point}")
        
        # 生成摘要
        summary = ContextUtils.generate_summary(conversation)
        print(f"\n生成的摘要: {summary}")
        
        # 计算哈希
        context_hash = ContextUtils.calculate_context_hash(data)
        print(f"\n上下文哈希: {context_hash[:16]}...")
        
        # 生成Markdown
        markdown = ContextUtils.export_to_markdown(data)
        print(f"\nMarkdown导出长度: {len(markdown)} 字符")
        print("Markdown预览:")
        print(markdown[:300] + "..." if len(markdown) > 300 else markdown)
        
        print("\n3. 上下文优化演示")
        print("-" * 30)
        
        # 优化上下文
        optimized = ContextUtils.optimize_context_for_model(data, max_tokens=50)
        original_tokens = sum(msg.get('tokens', 0) for msg in data['context']['conversation'])
        optimized_tokens = sum(msg.get('tokens', 0) for msg in optimized['context']['conversation'])
        
        print(f"原始token数: {original_tokens}")
        print(f"优化后token数: {optimized_tokens}")
        print(f"压缩比例: {optimized_tokens/original_tokens:.2%}")
        
        if 'extensions' in optimized and 'compression_info' in optimized['extensions']:
            comp_info = optimized['extensions']['compression_info']
            print(f"保留消息数: {comp_info['messages_kept']}")
            print(f"移除消息数: {comp_info['messages_removed']}")
        
        print("\n=== 演示完成 ===")
        print("ContextHub 所有功能运行正常！")
        
    except Exception as e:
        print(f"演示过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 