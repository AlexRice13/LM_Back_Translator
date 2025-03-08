

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
