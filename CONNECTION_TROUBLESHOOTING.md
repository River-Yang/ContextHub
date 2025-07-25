# ContextHub 连接故障排除指南

## 🚨 常见连接错误

### 1. "Premature close" 错误

**错误信息示例:**
```
Request ID: ec46eba9-ecb2-4f3a-9807-d35631beb855
ConnectError: [unknown] Premature close
```

**原因:**
- 网络连接不稳定
- API服务器临时不可用
- 防火墙或代理阻止连接
- 请求超时

**解决方案:**

#### 方法1: 使用重试机制（已集成）
现在的转换器已经内置了重试机制，会自动重试失败的请求。

```bash
# 使用多模型转换器（自带重试）
python convert_multi_model.py your_file.py -m kimi
```

#### 方法2: 使用故障转移工具
```bash
# 自动尝试多个模型API
python model_failover.py convert your_file.py
```

#### 方法3: 网络诊断
```bash
# 运行网络诊断工具
python network_diagnostic.py
```

### 2. API密钥错误

**错误信息:**
```
请设置 MOONSHOT_API_KEY 环境变量或传入 api_key 参数
```

**解决方案:**

#### 环境变量方式:
```bash
export MOONSHOT_API_KEY="your-api-key"
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-claude-key"
```

#### 配置文件方式:
编辑 `model_config.yaml`:
```yaml
api_keys:
  kimi:
    api_key: "your-kimi-key"
  openai:
    api_key: "your-openai-key"
  claude:
    api_key: "your-claude-key"
```

### 3. 网络超时

**错误信息:**
```
timeout: The read operation timed out
```

**解决方案:**

1. **检查网络连接**
   ```bash
   python network_diagnostic.py
   ```

2. **使用VPN** (如果在限制网络环境中)

3. **调整超时设置** (已设为60秒)

### 4. SSL证书错误

**错误信息:**
```
SSL certificate verify failed
```

**解决方案:**

1. **更新系统证书**
   ```bash
   # macOS
   brew install ca-certificates
   
   # Ubuntu/Debian
   apt-get update && apt-get install ca-certificates
   ```

2. **检查系统时间** - 确保系统时间正确

## 🛠️ 故障排除工具

### 1. 网络诊断工具
```bash
python network_diagnostic.py
```

功能:
- ✅ 检查互联网连接
- ✅ DNS解析测试
- ✅ SSL证书验证
- ✅ HTTP连接测试
- ✅ 网络路径追踪

### 2. 模型测试工具
```bash
python model_failover.py test
```

功能:
- ✅ 测试所有可用模型
- ✅ 检查API密钥
- ✅ 执行实际转换测试

### 3. 故障转移工具
```bash
python model_failover.py convert your_file.py
```

功能:
- ✅ 自动选择可用模型
- ✅ 失败时自动切换
- ✅ 智能重试机制

## 🔧 手动修复步骤

### 步骤1: 基础检查
```bash
# 1. 检查网络连接
ping 8.8.8.8

# 2. 检查DNS解析
nslookup api.moonshot.cn

# 3. 测试HTTP连接
curl -I https://api.moonshot.cn/v1/models
```

### 步骤2: API测试
```bash
# 测试Kimi API（需要有效的API密钥）
curl -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"moonshot-v1-8k","messages":[{"role":"user","content":"Hello"}],"max_tokens":10}' \
     https://api.moonshot.cn/v1/chat/completions
```

### 步骤3: 使用备选方案
如果Kimi API不可用，尝试其他模型:

```bash
# 使用OpenAI (需要API密钥)
export OPENAI_API_KEY="your-key"
python convert_multi_model.py your_file.py -m openai

# 使用Claude (需要API密钥)  
export ANTHROPIC_API_KEY="your-key"
python convert_multi_model.py your_file.py -m claude
```

## 🌐 网络环境特殊处理

### 公司网络/防火墙环境
```bash
# 设置代理 (如果需要)
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080

# 或者在Python中设置代理
# 修改 convert_multi_model.py 中的请求设置
```

### 中国大陆网络环境
- 优先使用Kimi API (国内服务)
- 使用VPN访问OpenAI/Claude API
- 或使用国内替代模型 (计划中)

## 📊 监控和日志

### 启用详细日志
```bash
export CONTEXTHUB_DEBUG=1
python convert_multi_model.py your_file.py -m kimi
```

### 检查错误日志
错误信息会显示在控制台，包括:
- 🔄 重试尝试次数
- ⚠️ 具体错误信息
- ✅ 成功/失败状态

## 🔗 获取帮助

### 常用诊断命令
```bash
# 完整诊断流程
python network_diagnostic.py
python model_failover.py test
python convert_multi_model.py --list-models

# 查看系统信息
python -c "import sys; print(f'Python: {sys.version}')"
python -c "import openai; print(f'OpenAI SDK: {openai.__version__}')"
```

### 问题报告模板
如果问题依然存在，请提供以下信息:

1. **错误信息:** (完整的错误日志)
2. **操作系统:** (macOS/Windows/Linux + 版本)
3. **Python版本:** `python --version`
4. **网络环境:** (家庭/公司/学校网络)
5. **使用的模型:** (kimi/openai/claude)
6. **诊断结果:** `python network_diagnostic.py` 的输出

## 💡 预防措施

1. **定期测试连接**
   ```bash
   # 添加到定时任务
   python model_failover.py test
   ```

2. **配置多个API密钥** - 确保有备选方案

3. **监控网络状况** - 使用网络诊断工具

4. **保持工具更新** - 定期更新转换器代码

---

🎯 **记住**: 新的转换器具有内置重试机制和故障转移功能，大多数网络问题都会自动处理！ 