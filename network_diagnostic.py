#!/usr/bin/env python3
"""
ContextHub 网络诊断工具

用于诊断和调试AI模型API的连接问题
"""

import requests
import socket
import time
import ssl
from urllib.parse import urlparse
import subprocess
import platform

def check_internet_connection():
    """检查基本的互联网连接"""
    print("🌐 检查互联网连接...")
    
    test_hosts = [
        "8.8.8.8",  # Google DNS
        "1.1.1.1",  # Cloudflare DNS
        "baidu.com",  # 国内站点
    ]
    
    for host in test_hosts:
        try:
            socket.create_connection((host, 80 if host.endswith('.com') else 53), timeout=5)
            print(f"✅ {host} 连接正常")
            return True
        except Exception as e:
            print(f"❌ {host} 连接失败: {e}")
    
    print("❌ 互联网连接异常")
    return False

def check_dns_resolution(hostname):
    """检查DNS解析"""
    print(f"🔍 检查DNS解析: {hostname}")
    
    try:
        ip = socket.gethostbyname(hostname)
        print(f"✅ DNS解析成功: {hostname} -> {ip}")
        return ip
    except Exception as e:
        print(f"❌ DNS解析失败: {e}")
        return None

def check_ssl_certificate(hostname, port=443):
    """检查SSL证书"""
    print(f"🔒 检查SSL证书: {hostname}:{port}")
    
    try:
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print(f"✅ SSL证书有效")
                print(f"   颁发给: {cert.get('subject', [{}])[0].get('commonName', 'Unknown')}")
                print(f"   颁发者: {cert.get('issuer', [{}])[-1].get('commonName', 'Unknown')}")
                return True
    except Exception as e:
        print(f"❌ SSL证书检查失败: {e}")
        return False

def test_http_connection(url, timeout=30):
    """测试HTTP连接"""
    print(f"🌐 测试HTTP连接: {url}")
    
    try:
        start_time = time.time()
        response = requests.get(url, timeout=timeout)
        end_time = time.time()
        
        print(f"✅ HTTP连接成功")
        print(f"   状态码: {response.status_code}")
        print(f"   响应时间: {end_time - start_time:.2f}秒")
        print(f"   服务器: {response.headers.get('Server', 'Unknown')}")
        return True
        
    except requests.exceptions.Timeout:
        print(f"❌ 连接超时 (>{timeout}秒)")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def test_api_endpoint(api_url, api_key, model_name):
    """测试特定的API端点"""
    print(f"🤖 测试 {model_name} API端点...")
    
    if "moonshot" in api_url:
        # Kimi API 测试
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "moonshot-v1-8k",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }
        
        test_url = f"{api_url}/chat/completions"
        
    elif "api.openai.com" in api_url:
        # OpenAI API 测试
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 10
        }
        
        test_url = f"{api_url}/chat/completions"
        
    elif "api.anthropic.com" in api_url:
        # Claude API 测试
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        data = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "Hello"}]
        }
        
        test_url = f"{api_url}/v1/messages"
    else:
        print(f"❌ 不支持的API: {api_url}")
        return False
    
    try:
        response = requests.post(test_url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ {model_name} API 测试成功")
            return True
        elif response.status_code == 401:
            print(f"❌ {model_name} API 认证失败 (401) - 检查API密钥")
            return False
        elif response.status_code == 429:
            print(f"⚠️ {model_name} API 速率限制 (429) - 稍后重试")
            return False
        else:
            print(f"❌ {model_name} API 测试失败 (状态码: {response.status_code})")
            print(f"   响应: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ {model_name} API 测试异常: {e}")
        return False

def run_traceroute(hostname):
    """运行traceroute诊断网络路径"""
    print(f"🛣️ 网络路径追踪: {hostname}")
    
    try:
        if platform.system().lower() == "windows":
            cmd = ["tracert", "-h", "10", hostname]
        else:
            cmd = ["traceroute", "-m", "10", hostname]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ 路径追踪完成")
            lines = result.stdout.split('\n')[:5]  # 只显示前5跳
            for line in lines:
                if line.strip():
                    print(f"   {line}")
        else:
            print(f"❌ 路径追踪失败: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("❌ 路径追踪超时")
    except FileNotFoundError:
        print("❌ traceroute/tracert 命令不可用")
    except Exception as e:
        print(f"❌ 路径追踪异常: {e}")

def main():
    """运行完整的网络诊断"""
    print("🔧 ContextHub 网络诊断工具")
    print("=" * 50)
    
    # 基本连接检查
    if not check_internet_connection():
        print("\n❌ 基本互联网连接异常，请检查网络设置")
        return
    
    print("\n" + "=" * 50)
    
    # API端点配置
    api_endpoints = {
        "kimi": {
            "url": "https://api.moonshot.cn/v1",
            "hostname": "api.moonshot.cn"
        },
        "openai": {
            "url": "https://api.openai.com/v1", 
            "hostname": "api.openai.com"
        },
        "claude": {
            "url": "https://api.anthropic.com",
            "hostname": "api.anthropic.com"
        }
    }
    
    # 检查每个API端点
    for model_name, config in api_endpoints.items():
        print(f"\n📡 检查 {model_name.upper()} API...")
        print("-" * 30)
        
        hostname = config["hostname"]
        
        # DNS检查
        ip = check_dns_resolution(hostname)
        if not ip:
            continue
        
        # SSL检查
        check_ssl_certificate(hostname)
        
        # HTTP连接检查
        test_http_connection(config["url"] + "/models" if model_name != "claude" else config["url"])
        
        # 网络路径追踪
        run_traceroute(hostname)
    
    print("\n" + "=" * 50)
    print("🔧 诊断完成")
    print("\n💡 解决建议:")
    print("1. 如果DNS解析失败，尝试更换DNS服务器 (8.8.8.8, 1.1.1.1)")
    print("2. 如果SSL证书检查失败，可能是网络代理或防火墙问题")
    print("3. 如果连接超时，尝试使用VPN或检查防火墙设置")
    print("4. 确保API密钥正确且有效")

if __name__ == "__main__":
    main() 