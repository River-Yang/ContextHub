#!/usr/bin/env python3
"""
转换器测试脚本

用于测试 convert.py 的基本功能，无需真实的 API 调用。
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from convert import KimiConverter


class MockConverter(KimiConverter):
    """Mock 版本的转换器，用于测试"""
    
    def __init__(self):
        # 跳过真实的 API 初始化
        self.api_key = "mock-api-key"
        self.client = Mock()
        
        # 设置支持的文件类型
        self.text_extensions = {
            '.py', '.js', '.ts', '.tsx', '.jsx', '.html', '.css', '.scss', '.sass',
            '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.php', '.rb', '.go',
            '.rs', '.swift', '.kt', '.scala', '.sh', '.bash', '.zsh',
            '.md', '.txt', '.json', '.xml', '.yaml', '.yml', '.toml', '.ini',
            '.sql', '.r', '.m', '.pl', '.lua', '.dart', '.vue'
        }
        
        self.image_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'
        }
    
    def _call_kimi_api(self, prompt: str, is_image: bool = False, image_data: str = None) -> dict:
        """Mock API 调用，返回模拟的分析结果"""
        if is_image:
            return {
                "summary": "这是一个测试图像文件的分析结果",
                "key_points": ["图像尺寸", "颜色信息", "格式类型"],
                "analysis": "图像文件包含了丰富的视觉信息，可以用于UI设计或文档说明。",
                "purpose": "用于测试图像分析功能",
                "complexity": "low"
            }
        else:
            # 根据文件内容生成不同的mock结果
            if "def " in prompt or "function " in prompt:
                return {
                    "summary": "这是一个包含函数定义的代码文件",
                    "key_points": ["函数定义", "参数处理", "返回值"],
                    "analysis": "代码结构清晰，包含多个函数定义和逻辑处理。建议添加更多注释和错误处理。",
                    "purpose": "实现特定的业务功能",
                    "dependencies": ["标准库", "第三方包"],
                    "structure": "模块化设计",
                    "complexity": "medium",
                    "suggestions": ["添加类型注解", "增加单元测试"]
                }
            elif "# " in prompt or "## " in prompt:
                return {
                    "summary": "这是一个Markdown文档文件",
                    "key_points": ["文档结构", "标题层级", "内容组织"],
                    "analysis": "文档结构良好，信息组织清晰，适合作为项目说明或技术文档。",
                    "purpose": "提供项目说明和使用指南",
                    "complexity": "low",
                    "suggestions": ["添加更多示例", "完善目录结构"]
                }
            else:
                return {
                    "summary": "通用文件分析结果",
                    "key_points": ["文件内容", "基本结构", "主要特点"],
                    "analysis": "这是一个标准的文本文件，包含了基本的信息和内容。",
                    "purpose": "存储和传递信息",
                    "complexity": "low"
                }


def test_task_type_detection():
    """测试任务类型检测功能"""
    print("=== 测试任务类型检测 ===")
    
    converter = MockConverter()
    
    test_cases = [
        ("test.py", "def hello(): pass", "code_project"),
        ("script.js", "function test() {}", "code_project"),
        ("config.json", '{"name": "test"}', "code_project"),
        ("README.md", "# Project", "document_analysis"),
        ("doc.txt", "This is a document", "document_analysis"),
        ("unknown.xyz", "content", "document_analysis"),
    ]
    
    for file_path, content, expected in test_cases:
        detected = converter._detect_task_type(file_path, content)
        status = "✅" if detected == expected else "❌"
        print(f"{status} {file_path}: {detected} (期望: {expected})")


def test_file_reading():
    """测试文件读取功能"""
    print("\n=== 测试文件读取 ===")
    
    converter = MockConverter()
    
    # 创建临时文件进行测试
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write("#!/usr/bin/env python3\n")
        f.write("def hello():\n")
        f.write("    print('Hello, World!')\n")
        temp_file = f.name
    
    try:
        content, is_image, image_data = converter._read_file_content(temp_file)
        
        if not is_image and "Hello, World!" in content:
            print("✅ 文本文件读取成功")
        else:
            print("❌ 文本文件读取失败")
    
    finally:
        os.unlink(temp_file)


def test_ct_structure_creation():
    """测试.ct文件结构创建"""
    print("\n=== 测试.ct文件结构创建 ===")
    
    converter = MockConverter()
    
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write("def test_function():\n    return 'test'\n")
        temp_file = f.name
    
    try:
        # Mock分析结果
        analysis = {
            "summary": "测试函数文件",
            "key_points": ["函数定义", "返回值"],
            "analysis": "简单的测试函数",
            "purpose": "用于测试",
            "complexity": "low"
        }
        
        ct_data = converter._create_ct_structure(temp_file, analysis, "code_project")
        
        # 验证结构
        checks = [
            ("version", ct_data.get("version") == "1.0"),
            ("task_type", ct_data.get("metadata", {}).get("task_type") == "code_project"),
            ("assets", "files" in ct_data.get("assets", {})),
            ("history", len(ct_data.get("history", [])) >= 2),
            ("instructions", "role_and_goal" in ct_data.get("instructions", {}))
        ]
        
        for check_name, result in checks:
            status = "✅" if result else "❌"  
            print(f"{status} {check_name}: {result}")
    
    finally:
        os.unlink(temp_file)


def test_conversion_process():
    """测试完整转换流程"""
    print("\n=== 测试完整转换流程 ===")
    
    converter = MockConverter()
    
    # 创建临时文件和目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试文件
        test_file = Path(temp_dir) / "test.py"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("#!/usr/bin/env python3\n")
            f.write("def main():\n")
            f.write("    print('Testing convert functionality')\n")
            f.write("\nif __name__ == '__main__':\n")
            f.write("    main()\n")
        
        # 创建输出目录
        output_dir = Path(temp_dir) / "output"
        
        try:
            # 执行转换
            output_file = converter.convert_file(
                str(test_file),
                str(output_dir),
                "code_project"
            )
            
            # 验证输出文件
            if os.path.exists(output_file):
                print("✅ 转换文件创建成功")
                
                # 验证JSON格式
                with open(output_file, 'r', encoding='utf-8') as f:
                    ct_data = json.load(f)
                
                if ct_data.get("version") == "1.0":
                    print("✅ .ct文件格式正确")
                else:
                    print("❌ .ct文件格式错误")
                    
                # 显示部分内容
                print(f"📄 生成的文件: {Path(output_file).name}")
                print(f"📋 任务类型: {ct_data.get('metadata', {}).get('task_type')}")
                print(f"📝 名称: {ct_data.get('metadata', {}).get('name')}")
                
            else:
                print("❌ 转换文件创建失败")
                
        except Exception as e:
            print(f"❌ 转换过程出错: {e}")


def test_batch_conversion():
    """测试批量转换功能"""
    print("\n=== 测试批量转换 ===")
    
    converter = MockConverter()
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建多个测试文件
        test_files = [
            ("test1.py", "def func1(): pass"),
            ("test2.js", "function func2() {}"),
            ("README.md", "# Test Project"),
            ("config.json", '{"test": true}'),
            ("ignore.txt", "should be ignored"),  # 将被exclude
        ]
        
        for filename, content in test_files:
            with open(Path(temp_dir) / filename, 'w', encoding='utf-8') as f:
                f.write(content)
        
        output_dir = Path(temp_dir) / "batch_output"
        
        try:
            # 批量转换，排除txt文件
            converted_files = converter.convert_directory(
                temp_dir,
                str(output_dir),
                recursive=False,
                exclude_patterns=["*.txt"]
            )
            
            print(f"✅ 批量转换完成，处理了 {len(converted_files)} 个文件")
            
            # 验证文件数量（应该是4个，排除了txt文件）
            if len(converted_files) == 4:
                print("✅ 文件过滤功能正常")
            else:
                print(f"❌ 文件过滤异常，期望4个文件，实际{len(converted_files)}个")
                
        except Exception as e:
            print(f"❌ 批量转换出错: {e}")


def main():
    """运行所有测试"""
    print("ContextHub 转换器功能测试")
    print("=" * 40)
    print("注意: 这是Mock测试，不会调用真实的Kimi API")
    print()
    
    try:
        test_task_type_detection()
        test_file_reading()
        test_ct_structure_creation()
        test_conversion_process()
        test_batch_conversion()
        
        print("\n" + "=" * 40)
        print("✅ 所有测试完成！")
        print("\n如需测试真实API功能，请:")
        print("1. 设置 MOONSHOT_API_KEY 环境变量")
        print("2. 运行 python examples/usage_example.py")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 