#!/usr/bin/env python3
"""
ContextHub Backend API Server

提供文件上传、下载和管理的REST API接口
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS

from contexthub import ContextManager, ContextValidator, ContextUtils
from convert_multi_model import create_converter, list_available_models, MODEL_CONFIGS
import yaml

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:5173"])

# 配置
UPLOAD_FOLDER = './my_contexts'
# 支持的源文件类型（将被转换为.ct格式）
ALLOWED_EXTENSIONS = {
    # 代码文件
    'py', 'js', 'ts', 'tsx', 'jsx', 'java', 'cpp', 'c', 'h', 'hpp', 'cs', 'php', 'rb', 'go',
    'rs', 'swift', 'kt', 'scala', 'sh', 'bash', 'zsh',
    # 标记和样式文件
    'html', 'css', 'scss', 'sass', 'md', 'xml', 'vue',
    # 配置文件
    'json', 'yaml', 'yml', 'toml', 'ini', 'cfg',
    # 数据文件
    'sql', 'r', 'm', 'pl', 'lua', 'dart',
    # 文档文件
    'txt', 'md', 'rst',
    # 图像文件
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'
}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 初始化上下文管理器和文件转换器
context_manager = ContextManager(UPLOAD_FOLDER)
# 加载配置文件
def load_config():
    """加载配置文件"""
    try:
        with open('model_config.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return {"default_model": "kimi"}

config = load_config()
default_model = config.get("default_model", "kimi")

# 初始化默认转换器
try:
    converter = create_converter(default_model)
    print(f"✅ 使用默认模型: {MODEL_CONFIGS[default_model]['name']}")
except Exception as e:
    print(f"⚠️ 默认模型 {default_model} 初始化失败: {e}")
    print("尝试使用 Kimi 作为后备模型...")
    try:
        converter = create_converter("kimi")
        print("✅ 使用后备模型: Moonshot Kimi")
    except Exception as e2:
        print(f"❌ 所有模型初始化失败: {e2}")
        converter = None


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_file_info(file_path):
    """获取文件基本信息，支持 v1.0 和 v3.0 格式"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 支持v1.0和v3.0格式
        version = data.get('version')
        if version not in ['1.0', '3.0']:
            raise ValueError(f"不支持的文件版本: {version or 'unknown'}")
        
        metadata = data.get('metadata', {})
        history = data.get('history', [])
        
        # 从文件名生成ID
        filename = os.path.basename(file_path)
        session_id = filename.replace('.ct', '')
        
        # 提取信息
        name = metadata.get('name', filename)
        description = "AI分析结果"
        
        # 从history中提取assistant的content作为描述
        for msg in history:
            if msg.get('role') == 'assistant':
                content = msg.get('content', '')
                description = content[:100] + '...' if len(content) > 100 else content
                break
        
        if not description or description == "AI分析结果":
            description = f"基于 {metadata.get('task_type', 'general_chat')} 任务类型的AI分析"
        
        return {
            'id': session_id,
            'name': filename,
            'description': description,
            'created_at': metadata.get('createdAt', datetime.fromtimestamp(os.path.getctime(file_path)).isoformat()),
            'updated_at': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
            'size': f"{os.path.getsize(file_path) / 1024:.1f} KB",
            'tags': [metadata.get('task_type', 'general_chat')],
            'model': metadata.get('analysis_model', 'kimi-k2-0711-preview'),
            'message_count': len(history),
            'file_path': file_path
        }
            
    except Exception as e:
        # 如果文件解析失败，返回基本信息
        filename = os.path.basename(file_path)
        return {
            'id': str(uuid.uuid4()),
            'name': filename,
            'description': f"文件解析错误: {str(e)}",
            'created_at': datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
            'updated_at': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
            'size': f"{os.path.getsize(file_path) / 1024:.1f} KB",
            'tags': ['error'],
            'model': "unknown",
            'message_count': 0,
            'file_path': file_path,
            'error': str(e)
        }


@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        'status': 'ok',
        'message': 'ContextHub API is running',
        'version': '1.0.0'
    })

@app.route('/api/models', methods=['GET'])
def get_available_models():
    """获取所有可用的AI模型"""
    try:
        models = []
        for key, config in MODEL_CONFIGS.items():
            models.append({
                'id': key,
                'name': config['name'],
                'supports_vision': config['supports_vision'],
                'available': key in ['kimi', 'openai', 'claude']  # 已实现的模型
            })
        
        return jsonify({
            'success': True,
            'models': models,
            'default_model': default_model
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/models/switch', methods=['POST'])
def switch_model():
    """切换当前使用的AI模型"""
    try:
        data = request.get_json()
        model_name = data.get('model')
        
        if not model_name:
            return jsonify({
                'success': False,
                'error': '请指定模型名称'
            }), 400
        
        if model_name not in MODEL_CONFIGS:
            return jsonify({
                'success': False,
                'error': f'不支持的模型: {model_name}'
            }), 400
        
        # 尝试创建新的转换器
        global converter, default_model
        new_converter = create_converter(model_name, data.get('api_key'))
        
        # 切换成功
        converter = new_converter
        default_model = model_name
        
        return jsonify({
            'success': True,
            'message': f'已切换到 {MODEL_CONFIGS[model_name]["name"]}',
            'model': model_name
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'切换模型失败: {str(e)}'
        }), 500


@app.route('/api/contexts', methods=['GET'])
def list_contexts():
    """获取所有上下文文件列表"""
    try:
        contexts = []
        upload_path = Path(UPLOAD_FOLDER)
        
        for ct_file in upload_path.glob("*.ct"):
            file_info = get_file_info(str(ct_file))
            contexts.append(file_info)
        
        # 按更新时间排序
        contexts.sort(key=lambda x: x['updated_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'data': contexts,
            'count': len(contexts)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/contexts/<context_id>', methods=['GET'])
def get_context(context_id):
    """获取特定上下文文件详情，支持 v1.0 和 v3.0 格式"""
    try:
        upload_path = Path(UPLOAD_FOLDER)
        
        # 查找对应的文件，使用文件名匹配
        context_file = None
        for ct_file in upload_path.glob("*.ct"):
            filename = ct_file.stem  # 去掉.ct扩展名
            if filename == context_id or filename.startswith(context_id):
                context_file = str(ct_file)
                break
        
        if not context_file:
            return jsonify({
                'success': False,
                'error': 'Context not found'
            }), 404
        
        # 读取并验证文件内容
        with open(context_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 验证版本格式（支持1.0和3.0）
        version = data.get('version')
        if version not in ['1.0', '3.0']:
            return jsonify({
                'success': False,
                'error': f'Unsupported file version: {version or "unknown"}'
            }), 400
        
        return jsonify({
            'success': True,
            'data': data
        })
    
    except json.JSONDecodeError:
        return jsonify({
            'success': False,
            'error': 'Invalid JSON file'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/create', methods=['POST'])
def create_context_from_files():
    """新建ct文件端点 - 将上传的文件转换为.ct格式"""
    try:
        # 检查是否有文件在请求中
        if 'files' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No files provided'
            }), 400
        
        files = request.files.getlist('files')
        if not files or all(f.filename == '' for f in files):
            return jsonify({
                'success': False,
                'error': 'No files selected'
            }), 400
        
        results = []
        created_contexts = []
        
        for file in files:
            if file and file.filename:
                original_filename = secure_filename(file.filename)
                
                # 检查文件类型
                if not allowed_file(original_filename):
                    results.append({
                        'filename': original_filename,
                        'status': 'error',
                        'error': f'File type not supported. Supported types: {", ".join(sorted(ALLOWED_EXTENSIONS))}'
                    })
                    continue
                
                # 创建临时文件路径
                temp_dir = os.path.join(UPLOAD_FOLDER, 'temp')
                os.makedirs(temp_dir, exist_ok=True)
                temp_file_path = os.path.join(temp_dir, original_filename)
                
                try:
                    # 保存临时文件
                    file.save(temp_file_path)
                    
                    # 检查转换器是否可用
                    if converter is None:
                        raise Exception("转换器未正确初始化，请检查API密钥配置")
                    
                    # 使用转换器将文件转换为.ct格式
                    print(f"开始转换文件: {original_filename}")
                    ct_file_path = converter.convert_file(temp_file_path, UPLOAD_FOLDER)
                    
                    # 获取转换后的文件信息
                    file_info = get_file_info(ct_file_path)
                    created_contexts.append(file_info)
                    
                    results.append({
                        'filename': original_filename,
                        'status': 'success',
                        'id': file_info['id'],
                        'ct_filename': os.path.basename(ct_file_path),
                        'message': f'Successfully converted {original_filename} to .ct format'
                    })
                    
                    print(f"✅ 转换成功: {original_filename} -> {os.path.basename(ct_file_path)}")
                    
                except Exception as e:
                    error_msg = str(e)
                    print(f"❌ 转换失败 {original_filename}: {error_msg}")
                    results.append({
                        'filename': original_filename,
                        'status': 'error',
                        'error': f'Conversion failed: {error_msg}'
                    })
                
                finally:
                    # 清理临时文件
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        
        return jsonify({
            'success': success_count > 0,
            'message': f'Created {success_count}/{len(results)} context files successfully',
            'results': results,
            'created_contexts': created_contexts
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Upload failed: {str(e)}'
        }), 500


@app.route('/api/download/<context_id>', methods=['GET'])
def download_context(context_id):
    """下载特定上下文文件，支持 v1.0 和 v3.0 格式"""
    try:
        upload_path = Path(UPLOAD_FOLDER)
        
        # 查找对应的文件，使用文件名匹配
        context_file = None
        for ct_file in upload_path.glob("*.ct"):
            filename = ct_file.stem
            if filename == context_id or filename.startswith(context_id):
                context_file = str(ct_file)
                break
        
        if not context_file:
            return jsonify({
                'success': False,
                'error': 'Context not found'
            }), 404
        
        # 验证文件格式（支持1.0和3.0版本）
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            version = data.get('version')
            if version not in ['1.0', '3.0']:
                return jsonify({
                    'success': False,
                    'error': f'Unsupported file version: {version or "unknown"}'
                }), 400
        except json.JSONDecodeError:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON file'
            }), 400
        
        return send_file(
            context_file,
            as_attachment=True,
            download_name=os.path.basename(context_file),
            mimetype='application/json'
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/contexts/<context_id>', methods=['DELETE'])
def delete_context(context_id):
    """删除特定上下文文件，支持 v1.0 和 v3.0 格式"""
    try:
        upload_path = Path(UPLOAD_FOLDER)
        
        # 查找对应的文件，使用文件名匹配
        context_file = None
        for ct_file in upload_path.glob("*.ct"):
            filename = ct_file.stem
            if filename == context_id or filename.startswith(context_id):
                context_file = str(ct_file)
                break
        
        if not context_file:
            return jsonify({
                'success': False,
                'error': 'Context not found'
            }), 404
        
        # 验证文件格式（可选，删除前确认，支持1.0和3.0版本）
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            version = data.get('version')
            if version not in ['1.0', '3.0']:
                return jsonify({
                    'success': False,
                    'error': f'Unsupported file version: {version or "unknown"}'
                }), 400
        except json.JSONDecodeError:
            # 如果是无效JSON，也允许删除
            pass
        
        # 删除文件
        os.remove(context_file)
        
        return jsonify({
            'success': True,
            'message': 'Context deleted successfully'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/validate', methods=['POST'])
def validate_context():
    """验证上下文文件格式"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # 读取文件内容
        content = file.read().decode('utf-8')
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            return jsonify({
                'success': False,
                'error': 'Invalid JSON format'
            })
        
        # 验证格式
        validator = ContextValidator()
        is_valid, errors, warnings = validator.validate_file(data)
        
        return jsonify({
            'success': True,
            'is_valid': is_valid,
            'errors': errors,
            'warnings': warnings,
            'report': validator.get_validation_report()
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(413)
def too_large(e):
    """文件过大错误处理"""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413


@app.errorhandler(404)
def not_found(e):
    """404错误处理"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """500错误处理"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500


if __name__ == '__main__':
    print("🚀 Starting ContextHub API Server...")
    print(f"📁 Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"🌐 Server will run on: http://localhost:5001")
    print(f"📚 API Documentation:")
    print(f"  GET  /api/contexts          - List all contexts")
    print(f"  GET  /api/contexts/<id>     - Get specific context")
    print(f"  POST /api/create            - Create context from files")
    print(f"  GET  /api/download/<id>     - Download context")
    print(f"  DELETE /api/contexts/<id>   - Delete context")
    print(f"  POST /api/validate          - Validate context file")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5001) 