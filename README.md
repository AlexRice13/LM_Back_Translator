
# 基于大语言模型的翻译-回译对比工具 🔄

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

支持双向验证的Markdown智能翻译工具，集成AI差异分析功能。

## 功能特性 ✨
- ✂️ 智能分块处理（支持自定义token限制）
- 🔄 双向翻译校验机制
- 🔍 AI驱动的差异分析
- 🖼️ 图形化文件选择界面
- 🤖 多模型支持（兼容Ollama）
- 🚨 完善的错误处理机制
- 📈 实时进度跟踪与报告

## 环境要求 📋
- Python 3.8+
- Tkinter（通常随Python安装）
- `requests` 包
- 可访问的Ollama API或兼容AI模型

## 安装指南 ⚙️

```bash
# 克隆仓库
git clone https://github.com/your-username/markdown-translator.git

# 安装依赖
cd markdown-translator
pip install requests
```

## 使用说明 🚀

1. 启动翻译工具：
```python
python markdown_processor.py
```

2. 通过图形界面选择Markdown文件

3. 查看实时处理日志：
   - 原文显示
   - 翻译进度
   - 回译校验结果
   - 差异分析报告

4. 通过保存对话框保存翻译结果

## 配置参数 🔧

### 类初始化参数
```python
MarkdownProcessor(
    split_token=128,           # 最大分块token数
    ollama_api_url="http://localhost:11434/api/generate",  # API端点
    trans_model="hf.co/unsloth/DeepSeek-R1-Distill-Qwen-14B-GGUF:Q6_K",  # 默认翻译模型
    compare_model="hf.co/unsloth/DeepSeek-R1-Distill-Qwen-14B-GGUF:Q6_K"  # 分析模型
)
```

### 环境准备
1. 确保本地Ollama服务正在运行
2. 验证模型可用性：
```bash
ollama list
```

## 贡献指南 🤝
欢迎贡献代码！请按以下流程操作：
1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/新特性`)
3. 提交修改 (`git commit -m '添加新特性'`)
4. 推送分支 (`git push origin feature/新特性`)
5. 发起Pull Request

## 许可协议 📄
本项目采用MIT许可证，详见[LICENSE](LICENSE)文件。

---

**重要提示：**
- 🚦 开始前请确保Ollama服务已启动
- 📦 请确认本地Ollama实例中模型可用
- ⚠️ 根据模型上下文窗口调整`split_token`参数
- 💾 处理大文件前请先保存现有工作


# LM_Back_Translator Toolkit 🔄

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)

A sophisticated Markdown translation tool with bidirectional verification and AI-powered analysis.

## Features ✨
- ✂️ Smart Markdown segmentation with token limits
- 🔄 Bidirectional translation verification
- 🔍 AI-powered difference analysis
- 🖼️ GUI file selection interface
- 🤖 Multi-model support (Ollama compatible)
- 🚨 Error handling and retry mechanisms
- 📈 Progress tracking and status reporting

## Requirements 📋
- Python 3.8+
- Tkinter (usually included with Python)
- `requests` package
- Access to Ollama API or compatible AI models

## Installation ⚙️

```bash
# Clone repository
git clone https://github.com/your-username/markdown-translator.git

# Install dependencies
cd markdown-translator
pip install requests
```

## Usage 🚀

1. Start the translation tool:
```python
python markdown_processor.py
```

2. Select a Markdown file through the GUI dialog

3. Watch real-time processing in the console:
   - Original text display
   - Translation progress
   - Back-translation verification
   - Difference analysis results

4. Save translated file through the final dialog

## Configuration 🔧

### Class Initialization Parameters
```python
MarkdownProcessor(
    split_token=128,           # Max tokens per segment
    ollama_api_url="http://localhost:11434/api/generate",  # API endpoint
    trans_model="hf.co/unsloth/DeepSeek-R1-Distill-Qwen-14B-GGUF:Q6_K",  # Default model
    compare_model="hf.co/unsloth/DeepSeek-R1-Distill-Qwen-14B-GGUF:Q6_K"  # Analysis model
)
```

### Environment Preparation
1. Ensure Ollama service is running locally
2. Verify model availability:
```bash
ollama list
```

## Contributing 🤝

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄
This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

**Important Notes:**
- 🚦 Ensure your Ollama service is running before starting
- 📦 Verify model availability in your local Ollama instance
- ⚠️ Adjust `split_token` based on your model's context window
- 💾 Save your work before processing large files
```
