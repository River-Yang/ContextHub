#!/usr/bin/env python3
"""
ContextHub 命令行接口
"""

import os
import sys
import argparse
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from convert import KimiConverter
except ImportError:
    # 如果直接导入失败，尝试从项目根目录导入
    try:
        sys.path.insert(0, str(Path.cwd()))
        from convert import KimiConverter
    except ImportError:
        print("❌ 错误: 无法导入 KimiConverter。请确保在项目根目录运行此脚本。")
        sys.exit(1)


class ContextHubCLI:
    """ContextHub 命令行接口"""
    
    def __init__(self, hub_directory: str = "./my_contexts"):
        """
        初始化 CLI 工具
        
        Args:
            hub_directory: ContextHub 文件存储目录
        """
        self.hub_directory = Path(hub_directory)
        self.hub_directory.mkdir(exist_ok=True)
        
        try:
            self.converter = KimiConverter()
        except Exception as e:
            print(f"❌ 无法初始化 KimiConverter: {e}")
            print("💡 请确保设置了 MOONSHOT_API_KEY 环境变量")
            sys.exit(1)
    
    def create_from_file(self, file_path: str, task_type: Optional[str] = None) -> bool:
        """
        从单个文件创建上下文
        
        Args:
            file_path: 文件路径
            task_type: 强制指定任务类型
            
        Returns:
            是否成功创建
        """
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            return False
        
        try:
            print(f"🔄 正在处理文件: {file_path}")
            
            # 转换文件
            ct_file_path = self.converter.convert_file(
                file_path, 
                str(self.hub_directory), 
                task_type
            )
            
            # 获取文件信息
            with open(ct_file_path, 'r', encoding='utf-8') as f:
                ct_data = json.load(f)
            
            print(f"✅ 成功创建: {os.path.basename(ct_file_path)}")
            print(f"   📁 位置: {ct_file_path}")
            print(f"   🏷️  任务类型: {ct_data['metadata']['task_type']}")
            print(f"   📝 描述: {ct_data['metadata']['name']}")
            
            return True
            
        except Exception as e:
            print(f"❌ 创建失败: {e}")
            return False
    
    def create_from_directory(self, dir_path: str, recursive: bool = True, 
                            include_patterns: Optional[List[str]] = None,
                            exclude_patterns: Optional[List[str]] = None,
                            task_type: Optional[str] = None) -> int:
        """
        从目录批量创建上下文
        
        Args:
            dir_path: 目录路径
            recursive: 是否递归处理子目录
            include_patterns: 包含的文件模式
            exclude_patterns: 排除的文件模式
            task_type: 强制指定任务类型
            
        Returns:
            成功创建的文件数量
        """
        if not os.path.exists(dir_path):
            print(f"❌ 目录不存在: {dir_path}")
            return 0
        
        try:
            print(f"🔄 正在处理目录: {dir_path}")
            
            # 批量转换
            converted_files = self.converter.convert_directory(
                dir_path,
                str(self.hub_directory),
                recursive,
                include_patterns,
                exclude_patterns
            )
            
            success_count = len(converted_files)
            
            if success_count > 0:
                print(f"✅ 成功创建 {success_count} 个上下文文件:")
                for ct_file in converted_files:
                    print(f"   📄 {os.path.basename(ct_file)}")
            else:
                print("⚠️  没有找到可处理的文件")
            
            return success_count
            
        except Exception as e:
            print(f"❌ 批量创建失败: {e}")
            return 0
    
    def list_contexts(self, limit: Optional[int] = None) -> None:
        """
        列出现有的上下文文件
        
        Args:
            limit: 限制显示数量
        """
        ct_files = list(self.hub_directory.glob("*.ct"))
        
        if not ct_files:
            print("📂 ContextHub 中暂无文件")
            return
        
        # 按修改时间排序
        ct_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if limit:
            ct_files = ct_files[:limit]
        
        print(f"📂 ContextHub 中的文件 ({len(ct_files)} 个):")
        print("=" * 80)
        
        for i, ct_file in enumerate(ct_files, 1):
            try:
                with open(ct_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                name = data.get('metadata', {}).get('name', ct_file.stem)
                task_type = data.get('metadata', {}).get('task_type', 'unknown')
                created_at = data.get('metadata', {}).get('createdAt', 'unknown')
                
                # 格式化时间
                try:
                    if created_at != 'unknown':
                        dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                        created_at = dt.strftime('%Y-%m-%d %H:%M')
                except:
                    pass
                
                print(f"{i:2d}. 📄 {ct_file.name}")
                print(f"    🏷️  {task_type} | 📅 {created_at}")
                print(f"    📝 {name}")
                print()
                
            except Exception as e:
                print(f"{i:2d}. 📄 {ct_file.name} (解析失败: {e})")
                print()
    
    def get_stats(self) -> None:
        """显示统计信息"""
        ct_files = list(self.hub_directory.glob("*.ct"))
        
        if not ct_files:
            print("📊 ContextHub 统计: 暂无文件")
            return
        
        # 统计任务类型
        task_types = {}
        total_size = 0
        
        for ct_file in ct_files:
            try:
                total_size += ct_file.stat().st_size
                
                with open(ct_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                task_type = data.get('metadata', {}).get('task_type', 'unknown')
                task_types[task_type] = task_types.get(task_type, 0) + 1
                
            except:
                task_types['error'] = task_types.get('error', 0) + 1
        
        print("📊 ContextHub 统计:")
        print("=" * 40)
        print(f"📁 总文件数: {len(ct_files)}")
        print(f"💾 总大小: {total_size / 1024:.1f} KB")
        print(f"📂 存储位置: {self.hub_directory.absolute()}")
        print()
        print("🏷️  任务类型分布:")
        for task_type, count in sorted(task_types.items()):
            print(f"   {task_type}: {count} 个")


def main():
    """命令行主入口点"""
    parser = argparse.ArgumentParser(
        description="ContextHub 命令行创建工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s create file.py                    # 创建单个文件的上下文
  %(prog)s create src/ -r                    # 递归处理整个目录
  %(prog)s create *.py                       # 使用通配符处理多个文件
  %(prog)s create file.py -t code_project    # 指定任务类型
  %(prog)s list                              # 列出现有文件
  %(prog)s list -n 5                         # 只显示最近5个文件
  %(prog)s stats                             # 显示统计信息
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='创建上下文文件')
    create_parser.add_argument('input', help='输入文件或目录路径')
    create_parser.add_argument('-t', '--task-type', 
                              choices=['general_chat', 'document_analysis', 'code_project'],
                              help='强制指定任务类型')
    create_parser.add_argument('-r', '--recursive', action='store_true',
                              help='递归处理目录')
    create_parser.add_argument('--include', nargs='+',
                              help='包含的文件模式 (如 *.py *.js)')
    create_parser.add_argument('--exclude', nargs='+',
                              help='排除的文件模式 (如 *test* *.pyc)')
    create_parser.add_argument('--hub-dir', default='./my_contexts',
                              help='ContextHub 目录 (默认: ./my_contexts)')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出现有上下文文件')
    list_parser.add_argument('-n', '--limit', type=int,
                            help='限制显示数量')
    list_parser.add_argument('--hub-dir', default='./my_contexts',
                            help='ContextHub 目录 (默认: ./my_contexts)')
    
    # stats 命令
    stats_parser = subparsers.add_parser('stats', help='显示统计信息')
    stats_parser.add_argument('--hub-dir', default='./my_contexts',
                             help='ContextHub 目录 (默认: ./my_contexts)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        cli = ContextHubCLI(args.hub_dir)
        
        if args.command == 'create':
            if os.path.isfile(args.input):
                # 单文件处理
                success = cli.create_from_file(args.input, args.task_type)
                return 0 if success else 1
            elif os.path.isdir(args.input):
                # 目录处理
                count = cli.create_from_directory(
                    args.input,
                    args.recursive,
                    args.include,
                    args.exclude,
                    args.task_type
                )
                return 0 if count > 0 else 1
            else:
                print(f"❌ 输入路径不存在: {args.input}")
                return 1
                
        elif args.command == 'list':
            cli.list_contexts(args.limit)
            return 0
            
        elif args.command == 'stats':
            cli.get_stats()
            return 0
    
    except KeyboardInterrupt:
        print("\n⚠️  操作已取消")
        return 1
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 