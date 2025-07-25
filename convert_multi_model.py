#!/usr/bin/env python3
"""
ContextHub 多模型文件转换器

支持多个AI模型API来分析各种文件并转换为规范的 .ct 格式文件 (v1.0)。

支持的模型提供商:
- Kimi (Moonshot AI)
- OpenAI GPT
- Anthropic Claude
- 阿里云通义千问
- 百度文心一言
- 智谱AI GLM
"""

import json
import os
import base64
import mimetypes
import time
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Type
from abc import ABC, abstractmethod
import uuid
import argparse
import yaml

# 模型配置
MODEL_CONFIGS = {
    "kimi": {
        "name": "Moonshot Kimi",
        "text_model": "moonshot-v1-8k",
        "vision_model": "moonshot-v1-8k-vision-preview",
        "base_url": "https://api.moonshot.cn/v1",
        "env_key": "MOONSHOT_API_KEY",
        "supports_vision": True
    },
    "openai": {
        "name": "OpenAI GPT",
        "text_model": "gpt-4o-mini",
        "vision_model": "gpt-4o-mini",
        "base_url": "https://api.openai.com/v1",
        "env_key": "OPENAI_API_KEY",
        "supports_vision": True
    },
    "claude": {
        "name": "Anthropic Claude",
        "text_model": "claude-3-5-sonnet-20241022",
        "vision_model": "claude-3-5-sonnet-20241022",
        "base_url": "https://api.anthropic.com",
        "env_key": "ANTHROPIC_API_KEY",
        "supports_vision": True
    },
    "qwen": {
        "name": "阿里云通义千问",
        "text_model": "qwen-turbo",
        "vision_model": "qwen-vl-plus",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "env_key": "DASHSCOPE_API_KEY",
        "supports_vision": True
    },
    "ernie": {
        "name": "百度文心一言",
        "text_model": "ERNIE-4.0-8K",
        "vision_model": "ERNIE-Vision-8K",
        "base_url": "https://aip.baidubce.com",
        "env_key": "BAIDU_API_KEY",
        "supports_vision": True
    },
    "glm": {
        "name": "智谱AI GLM",
        "text_model": "glm-4",
        "vision_model": "glm-4v",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "env_key": "ZHIPUAI_API_KEY",
        "supports_vision": True
    }
}


class BaseConverter(ABC):
    """文件转换器基础抽象类"""
    
    def __init__(self, api_key: Optional[str] = None, model_config: Dict[str, Any] = None):
        """
        初始化转换器
        
        Args:
            api_key: API 密钥
            model_config: 模型配置信息
        """
        self.model_config = model_config or {}
        
        # 尝试多种方式获取API密钥: 参数 > 环境变量 > 配置文件
        self.api_key = api_key or os.environ.get(self.model_config.get("env_key", ""))
        
        # 如果还没有API密钥，尝试从配置文件读取
        if not self.api_key:
            self.api_key = self._load_api_key_from_config()
        
        if not self.api_key:
            raise ValueError(f"请设置 {self.model_config.get('env_key', 'API_KEY')} 环境变量或传入 api_key 参数")
        
        # 支持的文件类型
        self.text_extensions = {
            '.py', '.js', '.ts', '.tsx', '.jsx', '.html', '.css', '.scss', '.sass',
            '.java', '.cpp', '.c', '.h', '.hpp', '.cs', '.php', '.rb', '.go',
            '.rs', '.swift', '.kt', '.scala', '.sh', '.bash', '.zsh',
            '.md', '.txt', '.json', '.xml', '.yaml', '.yml', '.toml', '.ini',
            '.sql', '.r', '.m', '.pl', '.lua', '.dart', '.vue', '.log'
        }
        
        self.image_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'
        }
        
        self._setup_client()
    
    def _load_api_key_from_config(self) -> Optional[str]:
        """从配置文件加载API密钥"""
        try:
            with open('model_config.yaml', 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            model_name = None
            for key, conf in MODEL_CONFIGS.items():
                if conf == self.model_config:
                    model_name = key
                    break
            
            if model_name and config.get('api_keys', {}).get(model_name, {}).get('api_key'):
                return config['api_keys'][model_name]['api_key']
        except (FileNotFoundError, KeyError, yaml.YAMLError):
            pass
        return None
    
    @abstractmethod
    def _setup_client(self):
        """设置API客户端，子类需实现"""
        pass
    
    @abstractmethod
    def _call_api(self, prompt: str, is_image: bool = False, image_data: str = None) -> Dict[str, Any]:
        """调用具体的API，子类需实现"""
        pass
    
    def _call_api_with_retry(self, prompt: str, is_image: bool = False, image_data: str = None, max_retries: int = 3) -> Dict[str, Any]:
        """
        带重试机制的API调用
        
        Args:
            prompt: 提示词
            is_image: 是否为图像分析
            image_data: base64编码的图像数据
            max_retries: 最大重试次数
            
        Returns:
            API响应结果
        """
        last_error = None
        
        for attempt in range(max_retries):
            try:
                print(f"🔄 API调用尝试 {attempt + 1}/{max_retries}")
                result = self._call_api(prompt, is_image, image_data)
                print("✅ API调用成功")
                return result
                
            except Exception as e:
                last_error = e
                error_msg = str(e).lower()
                
                # 检查是否是网络相关错误
                if any(keyword in error_msg for keyword in ['premature close', 'connection', 'timeout', 'network']):
                    wait_time = (attempt + 1) * 2  # 递增等待时间: 2, 4, 6 秒
                    print(f"⚠️ 网络错误 (尝试 {attempt + 1}/{max_retries}): {e}")
                    
                    if attempt < max_retries - 1:
                        print(f"⏳ {wait_time}秒后重试...")
                        time.sleep(wait_time)
                        continue
                else:
                    # 非网络错误，直接抛出
                    raise e
        
        # 所有重试都失败
        print(f"❌ API调用失败，已重试{max_retries}次")
        raise Exception(f"API调用失败 (已重试{max_retries}次): {last_error}")
    
    def _detect_task_type(self, file_path: str, content: str) -> str:
        """检测任务类型"""
        file_ext = Path(file_path).suffix.lower()
        
        # 代码文件
        if file_ext in {'.py', '.js', '.ts', '.tsx', '.jsx', '.java', '.cpp', '.c', 
                       '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala'}:
            return "code_project"

        # 文档文件
        if file_ext in {'.md', '.txt', '.pdf', '.doc', '.docx'} or 'README' in file_path.upper():
            return "document_analysis"
        
        # 配置文件等也可能是代码项目的一部分
        if file_ext in {'.json', '.xml', '.yaml', '.yml', '.toml', '.ini', '.cfg'}:
            return "code_project"
        
        # 默认为文档分析
        return "document_analysis"
    
    def _generate_analysis_prompt(self, file_path: str, content: str, task_type: str) -> str:
        """生成分析提示词"""
        base_prompt = f"""请分析以下文件并提供详细的分析结果：

文件路径: {file_path}
任务类型: {task_type}

请按照以下格式返回JSON结果：
{{
  "summary": "文件的简要概述",
  "key_points": ["关键点1", "关键点2", "关键点3"],
  "analysis": "详细分析内容",
  "purpose": "文件的主要用途和功能",
  "dependencies": ["依赖项1", "依赖项2"],
  "structure": "文件结构说明",
  "complexity": "low/medium/high",
  "suggestions": ["改进建议1", "改进建议2"]
}}

文件内容：
```
{content}
```
"""
        
        if task_type == "code_project":
            base_prompt += """
请特别关注：
1. 代码功能和逻辑
2. 使用的技术栈和框架
3. 代码质量和结构
4. 潜在的改进点
5. 与其他模块的关系
"""
        elif task_type == "document_analysis":
            base_prompt += """
请特别关注：
1. 文档的主要内容和结构
2. 关键信息和要点
3. 文档类型和用途
4. 信息的组织方式
5. 是否有缺失或需要补充的内容
"""
        
        return base_prompt
    
    def _read_file_content(self, file_path: str) -> Union[str, bytes]:
        """读取文件内容"""
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext in self.image_extensions:
                with open(file_path, 'rb') as f:
                    return f.read()
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
        except Exception as e:
            raise Exception(f"读取文件失败: {str(e)}")
    
    def _create_ct_structure(self, file_path: str, task_type: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """创建 .ct 文件结构"""
        now = datetime.now(timezone.utc).isoformat()
        file_name = Path(file_path).stem
        
        ct_structure = {
            "version": "1.0",
            "metadata": {
                "name": f"{file_name} 分析",
                "task_type": task_type,
                "createdAt": now,
                "source_file": file_path,
                "analysis_model": self.model_config.get("name", "Unknown Model")
            },
            "instructions": {
                "system": f"你是一个专门分析 {task_type} 的AI助手。",
                "context": analysis_result.get("summary", ""),
                "constraints": [
                    "基于提供的文件内容进行分析",
                    "保持客观和准确",
                    "提供实用的建议"
                ]
            },
            "assets": {
                "state_chain": [
                    {
                        "id": str(uuid.uuid4()),
                        "type": "analysis",
                        "content": analysis_result.get("analysis", ""),
                        "metadata": {
                            "complexity": analysis_result.get("complexity", "medium"),
                            "key_points": analysis_result.get("key_points", []),
                            "dependencies": analysis_result.get("dependencies", []),
                            "suggestions": analysis_result.get("suggestions", [])
                        }
                    }
                ]
            },
            "examples": [
                {
                    "input": f"分析这个{task_type}文件",
                    "output": analysis_result.get("purpose", ""),
                    "context": "文件分析示例"
                }
            ],
            "history": [
                {
                    "timestamp": now,
                    "action": "create",
                    "details": f"通过 {self.model_config.get('name', 'AI模型')} 分析创建"
                }
            ]
        }
        
        return ct_structure
    
    def convert_file(self, file_path: str, output_dir: str = "./contexts") -> str:
        """转换单个文件"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        print(f"正在分析文件: {file_path}")
        
        # 读取文件内容
        content = self._read_file_content(file_path)
        file_ext = Path(file_path).suffix.lower()
        
        # 检测任务类型
        if isinstance(content, bytes):
            task_type = "image_analysis"
            print(f"任务类型: {task_type}")
            
            # 转换为 base64
            image_data = base64.b64encode(content).decode('utf-8')
            
            # 生成图像分析提示词
            prompt = f"""请分析这张图片并提供详细的分析结果。

请按照以下格式返回JSON结果：
{{
  "summary": "图片的简要描述",
  "key_points": ["关键点1", "关键点2", "关键点3"],
  "analysis": "详细分析内容",
  "purpose": "图片的主要内容和用途",
  "dependencies": [],
  "structure": "图片构成说明",
  "complexity": "low/medium/high",
  "suggestions": ["建议1", "建议2"]
}}"""
            
            print(f"正在调用 {self.model_config.get('name', 'AI模型')} 进行图像分析...")
            analysis_result = self._call_api_with_retry(prompt, is_image=True, image_data=image_data)
        else:
            task_type = self._detect_task_type(file_path, content)
            print(f"任务类型: {task_type}")
            
            # 生成分析提示词
            prompt = self._generate_analysis_prompt(file_path, content, task_type)
            
            print(f"正在调用 {self.model_config.get('name', 'AI模型')} 进行分析...")
            analysis_result = self._call_api_with_retry(prompt)
        
        # 创建 .ct 文件结构
        ct_structure = self._create_ct_structure(file_path, task_type, analysis_result)
        
        # 保存文件
        os.makedirs(output_dir, exist_ok=True)
        
        file_name = Path(file_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"{file_name}_{timestamp}.ct")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(ct_structure, f, ensure_ascii=False, indent=2)
        
        print(f"转换完成: {output_file}")
        return output_file
    
    def convert_directory(self, dir_path: str, output_dir: str = "./contexts") -> List[str]:
        """批量转换目录中的文件"""
        if not os.path.exists(dir_path):
            raise FileNotFoundError(f"目录不存在: {dir_path}")
        
        output_files = []
        supported_extensions = self.text_extensions | self.image_extensions
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix.lower()
                
                if file_ext in supported_extensions:
                    try:
                        output_file = self.convert_file(file_path, output_dir)
                        output_files.append(output_file)
                    except Exception as e:
                        print(f"转换文件 {file_path} 失败: {str(e)}")
                        continue
        
        return output_files


class KimiConverter(BaseConverter):
    """Kimi (Moonshot) API 转换器"""
    
    def _setup_client(self):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("请安装 OpenAI SDK: pip install openai")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.model_config["base_url"],
            timeout=60.0,  # 设置60秒超时
            max_retries=0  # 禁用内置重试，使用我们自己的重试机制
        )
    
    def _call_api(self, prompt: str, is_image: bool = False, image_data: str = None) -> Dict[str, Any]:
        try:
            if is_image and image_data:
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ]
                model = self.model_config["vision_model"]
            else:
                messages = [{"role": "user", "content": prompt}]
                model = self.model_config["text_model"]
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=4000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            
            # 尝试解析 JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # 如果不是 JSON，创建基本结构
                return {
                    "summary": "AI 分析结果",
                    "key_points": ["分析完成"],
                    "analysis": content,
                    "purpose": "文件分析",
                    "dependencies": [],
                    "structure": "基础分析",
                    "complexity": "medium",
                    "suggestions": []
                }
        except Exception as e:
            raise Exception(f"调用 Kimi API 失败: {str(e)}")


class OpenAIConverter(BaseConverter):
    """OpenAI GPT API 转换器"""
    
    def _setup_client(self):
        try:
            from openai import OpenAI
        except ImportError:
            raise ImportError("请安装 OpenAI SDK: pip install openai")
        
        self.client = OpenAI(
            api_key=self.api_key,
            timeout=60.0,  # 设置60秒超时
            max_retries=0  # 禁用内置重试，使用我们自己的重试机制
        )
    
    def _call_api(self, prompt: str, is_image: bool = False, image_data: str = None) -> Dict[str, Any]:
        try:
            if is_image and image_data:
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ]
            else:
                messages = [{"role": "user", "content": prompt}]
            
            response = self.client.chat.completions.create(
                model=self.model_config["text_model"],
                messages=messages,
                max_tokens=4000,
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "summary": "AI 分析结果",
                    "key_points": ["分析完成"],
                    "analysis": content,
                    "purpose": "文件分析",
                    "dependencies": [],
                    "structure": "基础分析",
                    "complexity": "medium",
                    "suggestions": []
                }
        except Exception as e:
            raise Exception(f"调用 OpenAI API 失败: {str(e)}")


class ClaudeConverter(BaseConverter):
    """Anthropic Claude API 转换器"""
    
    def _setup_client(self):
        try:
            import anthropic
        except ImportError:
            raise ImportError("请安装 Anthropic SDK: pip install anthropic")
        
        self.client = anthropic.Anthropic(
            api_key=self.api_key,
            timeout=60.0  # 设置60秒超时
        )
    
    def _call_api(self, prompt: str, is_image: bool = False, image_data: str = None) -> Dict[str, Any]:
        try:
            if is_image and image_data:
                # Claude 的图像处理方式
                message_content = [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data
                        }
                    },
                    {"type": "text", "text": prompt}
                ]
            else:
                message_content = prompt
            
            response = self.client.messages.create(
                model=self.model_config["text_model"],
                max_tokens=4000,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": message_content}
                ]
            )
            
            content = response.content[0].text
            
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "summary": "AI 分析结果",
                    "key_points": ["分析完成"],
                    "analysis": content,
                    "purpose": "文件分析",
                    "dependencies": [],
                    "structure": "基础分析",
                    "complexity": "medium",
                    "suggestions": []
                }
        except Exception as e:
            raise Exception(f"调用 Claude API 失败: {str(e)}")


# 转换器工厂
CONVERTER_CLASSES = {
    "kimi": KimiConverter,
    "openai": OpenAIConverter,
    "claude": ClaudeConverter,
    # 可以继续添加其他转换器
}


def create_converter(model_name: str, api_key: Optional[str] = None) -> BaseConverter:
    """创建指定模型的转换器"""
    if model_name not in MODEL_CONFIGS:
        available_models = ", ".join(MODEL_CONFIGS.keys())
        raise ValueError(f"不支持的模型: {model_name}。支持的模型: {available_models}")
    
    if model_name not in CONVERTER_CLASSES:
        raise NotImplementedError(f"模型 {model_name} 的转换器尚未实现")
    
    model_config = MODEL_CONFIGS[model_name]
    converter_class = CONVERTER_CLASSES[model_name]
    
    return converter_class(api_key=api_key, model_config=model_config)


def list_available_models():
    """列出所有可用的模型"""
    print("可用的AI模型:")
    for key, config in MODEL_CONFIGS.items():
        status = "✅" if key in CONVERTER_CLASSES else "🚧"
        vision_support = "支持图像" if config["supports_vision"] else "仅文本"
        print(f"  {status} {key}: {config['name']} ({vision_support})")
    
    print("\n✅ = 已实现, 🚧 = 计划中")


def main():
    parser = argparse.ArgumentParser(description='ContextHub 多模型文件转换器')
    parser.add_argument('input', nargs='?', help='输入文件或目录路径')
    parser.add_argument('-o', '--output', default='./my_contexts', help='输出目录 (默认: ./my_contexts)')
    parser.add_argument('-m', '--model', default='kimi', choices=list(MODEL_CONFIGS.keys()), 
                       help='选择AI模型 (默认: kimi)')
    parser.add_argument('-k', '--api-key', help='API密钥 (也可通过环境变量设置)')
    parser.add_argument('--list-models', action='store_true', help='列出所有可用模型')
    
    args = parser.parse_args()
    
    if args.list_models:
        list_available_models()
        return
    
    if not args.input:
        parser.error('需要指定输入文件或目录路径，或使用 --list-models 查看可用模型')
    
    try:
        # 创建转换器
        converter = create_converter(args.model, args.api_key)
        
        # 执行转换
        if os.path.isfile(args.input):
            converter.convert_file(args.input, args.output)
        elif os.path.isdir(args.input):
            output_files = converter.convert_directory(args.input, args.output)
            print(f"\n批量转换完成! 共转换 {len(output_files)} 个文件")
        else:
            print(f"错误: 找不到文件或目录: {args.input}")
            return 1
            
    except Exception as e:
        print(f"转换失败: {str(e)}")
        return 1


if __name__ == "__main__":
    main() 