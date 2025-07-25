#!/usr/bin/env python3
"""
ContextHub 构建和发布脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"🔧 运行命令: {cmd}")
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, cwd=cwd,
            capture_output=True, text=True
        )
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令失败: {e}")
        if e.stderr:
            print(f"错误: {e.stderr}")
        return False


def clean_build():
    """清理构建文件"""
    print("🧹 清理构建文件...")
    
    dirs_to_clean = ["build", "dist", "*.egg-info"]
    for pattern in dirs_to_clean:
        for path in Path(".").glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"删除目录: {path}")
            elif path.is_file():
                path.unlink()
                print(f"删除文件: {path}")


def build_package():
    """构建包"""
    print("📦 构建包...")
    
    # 使用 build 工具
    if not run_command("python -m pip install build twine"):
        return False
        
    if not run_command("python -m build"):
        return False
        
    print("✅ 构建完成")
    return True


def check_package():
    """检查包"""
    print("🔍 检查包...")
    
    if not run_command("python -m twine check dist/*"):
        return False
        
    print("✅ 包检查通过")
    return True


def install_local():
    """本地安装测试"""
    print("🔧 本地安装测试...")
    
    # 卸载已有版本
    run_command("pip uninstall contexthub -y")
    
    # 安装新版本
    if not run_command("pip install dist/*.whl"):
        return False
        
    print("✅ 本地安装成功")
    return True


def test_commands():
    """测试命令"""
    print("🧪 测试命令...")
    
    commands = [
        "ctx --help",
        "contexthub --help", 
        "contexthub-server --help"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print(f"❌ 命令测试失败: {cmd}")
            return False
            
    print("✅ 命令测试通过")
    return True


def upload_to_pypi(test=True):
    """上传到 PyPI"""
    if test:
        print("🚀 上传到 TestPyPI...")
        cmd = "python -m twine upload --repository testpypi dist/*"
    else:
        print("🚀 上传到 PyPI...")
        cmd = "python -m twine upload dist/*"
        
    if not run_command(cmd):
        return False
        
    print("✅ 上传完成")
    return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="构建和发布 ContextHub")
    parser.add_argument("--clean", action="store_true", help="清理构建文件")
    parser.add_argument("--build", action="store_true", help="构建包")
    parser.add_argument("--check", action="store_true", help="检查包")
    parser.add_argument("--install", action="store_true", help="本地安装测试")
    parser.add_argument("--test", action="store_true", help="测试命令")
    parser.add_argument("--upload-test", action="store_true", help="上传到 TestPyPI")
    parser.add_argument("--upload", action="store_true", help="上传到 PyPI")
    parser.add_argument("--all", action="store_true", help="执行完整流程（不包括上传）")
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        return 1
    
    success = True
    
    if args.all or args.clean:
        clean_build()
    
    if args.all or args.build:
        success &= build_package()
        
    if success and (args.all or args.check):
        success &= check_package()
        
    if success and (args.all or args.install):
        success &= install_local()
        
    if success and (args.all or args.test):
        success &= test_commands()
        
    if success and args.upload_test:
        success &= upload_to_pypi(test=True)
        
    if success and args.upload:
        success &= upload_to_pypi(test=False)
    
    if success:
        print("\n🎉 所有操作完成！")
        
        if args.all:
            print("\n📚 后续步骤:")
            print("1. 测试安装: pip install contexthub")
            print("2. 上传测试: python build.py --upload-test")
            print("3. 正式发布: python build.py --upload")
            
        return 0
    else:
        print("\n❌ 操作失败！")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 