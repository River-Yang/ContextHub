#!/usr/bin/env python3
"""
ContextHub 转换器使用示例

演示如何使用 convert.py 脚本将各种文件转换为 .ct 格式。
"""

import os
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from convert import KimiConverter


def example_single_file():
    """示例1: 转换单个文件"""
    print("=== 示例1: 转换单个文件 ===")
    
    # 确保设置了 API 密钥
    if not os.environ.get("MOONSHOT_API_KEY"):
        print("警告: 未设置 MOONSHOT_API_KEY 环境变量")
        print("请设置: export MOONSHOT_API_KEY='your-api-key'")
        return
    
    try:
        # 创建转换器
        converter = KimiConverter()
        
        # 转换这个示例文件自身
        current_file = __file__
        print(f"转换文件: {current_file}")
        
        # 转换文件
        output_file = converter.convert_file(
            input_file=current_file,
            output_dir="./my_contexts",  # 输出到 my_contexts 目录
            task_type="code_project"  # 强制指定为代码项目类型
        )
        
        print(f"✅ 转换成功: {output_file}")
        
    except Exception as e:
        print(f"❌ 转换失败: {e}")


def example_batch_convert():
    """示例2: 批量转换目录"""
    print("\n=== 示例2: 批量转换目录 ===")
    
    if not os.environ.get("MOONSHOT_API_KEY"):
        print("警告: 未设置 MOONSHOT_API_KEY 环境变量")
        return
    
    try:
        converter = KimiConverter()
        
        # 批量转换 contexthub 目录中的 Python 文件
        converted_files = converter.convert_directory(
            input_dir="../contexthub",  # 转换 contexthub 目录
            output_dir="./my_contexts",
            recursive=True,
            include_patterns=["*.py"],  # 只处理 Python 文件
            exclude_patterns=["*__pycache__*", "*.pyc"]  # 排除缓存文件
        )
        
        print(f"✅ 批量转换完成，共处理 {len(converted_files)} 个文件:")
        for file in converted_files:
            print(f"  - {file}")
            
    except Exception as e:
        print(f"❌ 批量转换失败: {e}")


def example_document_analysis():
    """示例3: 分析文档文件"""
    print("\n=== 示例3: 分析文档文件 ===")
    
    if not os.environ.get("MOONSHOT_API_KEY"):
        print("警告: 未设置 MOONSHOT_API_KEY 环境变量")
        return
    
    try:
        converter = KimiConverter()
        
        # 转换 README 文件
        readme_file = "../README.md"
        if os.path.exists(readme_file):
            output_file = converter.convert_file(
                input_file=readme_file,
                output_dir="./my_contexts",
                task_type="document_analysis"  # 文档分析类型
            )
            print(f"✅ README 分析完成: {output_file}")
        else:
            print("README.md 文件不存在，跳过此示例")
            
    except Exception as e:
        print(f"❌ 文档分析失败: {e}")


def example_read_converted_file():
    """示例4: 读取转换后的 .ct 文件"""
    print("\n=== 示例4: 读取转换后的 .ct 文件 ===")
    
    try:
        # 查找最新的 .ct 文件
        contexts_dir = Path("./my_contexts")
        if not contexts_dir.exists():
            print("my_contexts 目录不存在，请先运行其他示例")
            return
        
        ct_files = list(contexts_dir.glob("*.ct"))
        if not ct_files:
            print("未找到 .ct 文件，请先运行其他示例")
            return
        
        # 选择最新的文件
        latest_file = max(ct_files, key=lambda f: f.stat().st_mtime)
        print(f"读取文件: {latest_file}")
        
        # 读取并显示基本信息
        import json
        with open(latest_file, 'r', encoding='utf-8') as f:
            ct_data = json.load(f)
        
        print(f"版本: {ct_data['version']}")
        print(f"任务类型: {ct_data['metadata']['task_type']}")
        print(f"名称: {ct_data['metadata']['name']}")
        print(f"创建时间: {ct_data['metadata']['createdAt']}")
        
        # 显示文件资产信息
        assets = ct_data.get('assets', {}).get('files', {})
        print(f"包含文件数: {len(assets)}")
        
        for file_path, asset_info in assets.items():
            state_chain = asset_info.get('state_chain', [])
            if state_chain:
                initial_state = state_chain[0]
                print(f"  文件: {file_path}")
                print(f"    摘要: {initial_state.get('summary', 'N/A')}")
                print(f"    复杂度: {initial_state.get('metadata', {}).get('complexity', 'N/A')}")
        
        # 显示对话历史
        history = ct_data.get('history', [])
        print(f"对话条数: {len(history)}")
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")


def main():
    """主函数 - 运行所有示例"""
    print("ContextHub 转换器使用示例")
    print("=" * 40)
    
    # 检查 API 密钥
    if not os.environ.get("MOONSHOT_API_KEY"):
        print("⚠️  使用前请设置 Kimi API 密钥:")
        print("   export MOONSHOT_API_KEY='your-api-key-here'")
        print()
        print("可以从以下链接获取 API 密钥:")
        print("   https://platform.moonshot.cn/")
        print()
    
    # 创建输出目录
    os.makedirs("./my_contexts", exist_ok=True)
    
    try:
        # 运行示例
        example_single_file()
        example_batch_convert()
        example_document_analysis()
        example_read_converted_file()
        
        print("\n" + "=" * 40)
        print("✅ 所有示例运行完成！")
        print("生成的 .ct 文件保存在 ./my_contexts/ 目录中")
        
    except KeyboardInterrupt:
        print("\n用户中断运行")
    except Exception as e:
        print(f"\n运行示例时出错: {e}")


if __name__ == "__main__":
    main() 