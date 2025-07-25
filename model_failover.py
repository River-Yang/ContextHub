#!/usr/bin/env python3
"""
ContextHub 模型故障转移工具

当主要模型API出现问题时，自动切换到其他可用的模型
"""

from convert_multi_model import create_converter, MODEL_CONFIGS, list_available_models
import yaml
import time

class ModelFailover:
    """模型故障转移管理器"""
    
    def __init__(self, preferred_models=None):
        """
        初始化故障转移管理器
        
        Args:
            preferred_models: 优先使用的模型列表，按优先级排序
        """
        self.preferred_models = preferred_models or ["kimi", "openai", "claude"]
        self.available_models = ["kimi", "openai", "claude"]  # 已实现的模型
        self.current_model = None
        self.current_converter = None
        self.failed_models = set()  # 记录失败的模型
        
    def load_config(self):
        """加载配置文件"""
        try:
            with open('model_config.yaml', 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {}
    
    def get_api_key(self, model_name):
        """获取指定模型的API密钥"""
        config = self.load_config()
        
        # 从配置文件获取
        if config.get('api_keys', {}).get(model_name, {}).get('api_key'):
            return config['api_keys'][model_name]['api_key']
        
        # 从环境变量获取
        import os
        env_key = MODEL_CONFIGS.get(model_name, {}).get('env_key')
        if env_key:
            return os.environ.get(env_key)
        
        return None
    
    def test_model(self, model_name):
        """测试指定模型是否可用"""
        try:
            print(f"🧪 测试模型: {model_name}")
            
            # 检查API密钥
            api_key = self.get_api_key(model_name)
            if not api_key:
                print(f"❌ {model_name}: 缺少API密钥")
                return False
            
            # 尝试创建转换器
            converter = create_converter(model_name, api_key)
            
            # 进行简单的测试转换
            import tempfile
            import os
            
            # 创建临时测试文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write("# 测试文件\ndef hello():\n    return 'Hello World'\n")
                temp_file = f.name
            
            try:
                # 尝试转换
                with tempfile.TemporaryDirectory() as temp_dir:
                    output_file = converter.convert_file(temp_file, temp_dir)
                    print(f"✅ {model_name}: 测试成功")
                    return True
            finally:
                os.unlink(temp_file)
                
        except Exception as e:
            print(f"❌ {model_name}: 测试失败 - {e}")
            return False
    
    def find_working_model(self):
        """查找第一个可用的模型"""
        print("🔍 查找可用模型...")
        
        # 按优先级测试模型
        for model_name in self.preferred_models:
            if model_name in self.failed_models:
                continue
                
            if model_name in self.available_models:
                if self.test_model(model_name):
                    return model_name
                else:
                    self.failed_models.add(model_name)
        
        return None
    
    def get_converter(self, force_refresh=False):
        """获取当前可用的转换器"""
        if self.current_converter and not force_refresh:
            return self.current_converter
        
        working_model = self.find_working_model()
        
        if not working_model:
            raise Exception("没有可用的模型API")
        
        api_key = self.get_api_key(working_model)
        self.current_converter = create_converter(working_model, api_key)
        self.current_model = working_model
        
        print(f"🎯 使用模型: {MODEL_CONFIGS[working_model]['name']}")
        return self.current_converter
    
    def convert_with_failover(self, file_path, output_dir="./my_contexts"):
        """
        使用故障转移机制转换文件
        
        Args:
            file_path: 输入文件路径
            output_dir: 输出目录
            
        Returns:
            转换后的文件路径
        """
        max_attempts = len(self.available_models)
        
        for attempt in range(max_attempts):
            try:
                converter = self.get_converter(force_refresh=(attempt > 0))
                return converter.convert_file(file_path, output_dir)
                
            except Exception as e:
                print(f"⚠️ 转换失败 (尝试 {attempt + 1}/{max_attempts}): {e}")
                
                # 将当前模型标记为失败
                if self.current_model:
                    self.failed_models.add(self.current_model)
                    self.current_converter = None
                    self.current_model = None
                
                if attempt == max_attempts - 1:
                    raise Exception(f"所有模型都失败了: {e}")
                
                print("🔄 尝试切换到其他模型...")
                time.sleep(2)  # 等待2秒后重试
        
        raise Exception("转换失败，所有模型都不可用")
    
    def reset_failed_models(self):
        """重置失败模型列表（例如网络恢复后）"""
        print("🔄 重置失败模型列表")
        self.failed_models.clear()
        self.current_converter = None
        self.current_model = None
    
    def get_status(self):
        """获取当前状态"""
        return {
            "current_model": self.current_model,
            "failed_models": list(self.failed_models),
            "available_models": self.available_models,
            "preferred_models": self.preferred_models
        }


def main():
    """命令行工具"""
    import argparse
    
    parser = argparse.ArgumentParser(description='ContextHub 模型故障转移工具')
    parser.add_argument('action', choices=['test', 'convert'], help='操作类型')
    parser.add_argument('input', nargs='?', help='输入文件路径 (convert时必需)')
    parser.add_argument('-o', '--output', default='./my_contexts', help='输出目录')
    parser.add_argument('--models', nargs='+', default=['kimi', 'openai', 'claude'], 
                       help='优先模型列表')
    
    args = parser.parse_args()
    
    failover = ModelFailover(preferred_models=args.models)
    
    if args.action == 'test':
        print("🧪 测试所有可用模型...")
        print("-" * 50)
        
        for model_name in failover.available_models:
            failover.test_model(model_name)
        
        print("\n📊 状态报告:")
        status = failover.get_status()
        print(f"  可用模型: {status['available_models']}")
        print(f"  失败模型: {status['failed_models']}")
        
    elif args.action == 'convert':
        if not args.input:
            parser.error('convert 操作需要指定输入文件')
        
        try:
            print(f"📄 转换文件: {args.input}")
            output_file = failover.convert_with_failover(args.input, args.output)
            print(f"✅ 转换完成: {output_file}")
            
        except Exception as e:
            print(f"❌ 转换失败: {e}")
            return 1


if __name__ == "__main__":
    main() 