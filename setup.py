#!/usr/bin/env python3
"""
ContextHub 安装配置文件
"""

from setuptools import setup, find_packages
import os
import sys

# 读取 README 文件
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取版本号
def get_version():
    version_file = os.path.join(os.path.dirname(__file__), "contexthub", "__init__.py")
    if os.path.exists(version_file):
        with open(version_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"

# 读取依赖
def get_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="contexthub",
    version=get_version(),
    author="ContextHub Team",
    author_email="your-email@example.com",
    description="AI Context Management System - 专为AI模型设计的上下文管理工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/contexthub",
    packages=find_packages(),
    py_modules=["convert", "create_context", "app"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=get_requirements(),
    extras_require={
        "server": ["Flask>=2.3.0", "Flask-CORS>=4.0.0"],
        "dev": ["pytest>=6.0", "black", "flake8"],
        "all": ["Flask>=2.3.0", "Flask-CORS>=4.0.0", "pytest>=6.0", "black", "flake8"]
    },
    entry_points={
        "console_scripts": [
            "ctx=contexthub.cli:main",
            "contexthub=contexthub.cli:main",
            "contexthub-server=contexthub.server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "contexthub": [
            "*.md",
            "examples/*.ct",
            "frontend/dist/*",
            "frontend/dist/**/*",
        ],
    },
    zip_safe=False,
    keywords="ai context management llm chatgpt claude kimi",
    project_urls={
        "Bug Reports": "https://github.com/your-username/contexthub/issues",
        "Source": "https://github.com/your-username/contexthub",
        "Documentation": "https://github.com/your-username/contexthub/blob/main/README.md",
    },
) 