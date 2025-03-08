import re
import os
import requests
from tkinter import Tk, filedialog
from tkinter.filedialog import askopenfilename 


class MarkdownProcessor:
    def __init__(self, split_token = 128, ollama_api_url = "http://localhost:11434/api/generate", trans_model = "hf.co/unsloth/DeepSeek-R1-Distill-Qwen-14B-GGUF:Q6_K", compare_model = "hf.co/unsloth/DeepSeek-R1-Distill-Qwen-14B-GGUF:Q6_K"):
        # 定义 Ollama API 的 URL
        self.split_token    = split_token
        self.OLLAMA_API_URL = ollama_api_url
        self.trans_model    = trans_model
        self.compare_model  = compare_model
        
        # 初始化时读取 Markdown 文档并分段
        self.markdown_content = self.select_and_read_markdown()
        if self.markdown_content:
            self.paragraphs_iter, self.num_paragraphs = self.split_markdown_by_estimated_tokens(self.markdown_content)
            print(f"文档分段数: {self.num_paragraphs}")
        else:
            self.paragraphs_iter = iter([])
            self.num_paragraphs = 0

        self.result = ""


    def read_markdown_as_string(self, file_path):
        """
        读取 Markdown 文件并将其内容作为字符串返回。

        :param file_path: Markdown 文件的路径
        :return: 文件内容的字符串
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"文件未找到: {file_path}")
            return None
        except Exception as e:
            print(f"读取文件时发生错误: {e}")
            return None

    def select_and_read_markdown(self):
        """
        弹出文件选择对话框，选择 Markdown 文件并读取其内容。
        """
        # 不隐藏 Tkinter 的主窗口
        self.ui_root = Tk()
        #self.ui_root.withdraw()

        # 弹出文件选择对话框，限制文件类型为 Markdown 文件
        file_path = askopenfilename(
            title="选择 Markdown 文件",
            filetypes=[("Markdown 文件", "*.md"), ("所有文件", "*.*")]
        )

        if file_path:
            # 读取文件内容
            markdown_content        =       self.read_markdown_as_string(file_path)
            self.markdown_title     =       base_name = os.path.splitext(os.path.basename(file_path))[0]
            if markdown_content:
                print("文件已读取")
            else:
                print("未读取到文件内容。")
        else:
            print("未选择文件。")
        return markdown_content

    def translate_text(self, text, target_language, trans_model):
        """
        使用 Ollama API 翻译文本。

        :param text: 要翻译的文本
        :param target_language: 目标语言
        :param trans_model: 使用的模型
        :return: 翻译后的文本
        """
        # 构造请求体
        payload = {
            "model": f"{trans_model}",
            "prompt": f"将以下文本翻译为 {target_language}: {text}",
            "stream": False
        }

        # 发送 POST 请求
        response = requests.post(self.OLLAMA_API_URL, json=payload)

        # 检查响应状态
        if response.status_code == 200:
            # 解析响应内容
            result = response.json()
            return result.get("response", "").strip()
        else:
            print(f"Error: {response.status_code}")
            return None

    def trans_unit(self, original_text, original_lang="English", target_lang="中文", model="qwen2.5:14b"):
        """
        翻译单元：将文本翻译为目标语言，然后再翻译回原始语言。

        :param original_text: 原始文本
        :param original_lang: 原始语言
        :param target_lang: 目标语言
        :param model: 使用的模型
        :return: 原始文本、翻译后的文本、回译后的文本
        """
        self.trans_model   = model
        # 翻译成目标语言
        target_t_str = self.translate_text(original_text, target_lang, model)
        if target_t_str:
            print(f"Translated to {target_lang}: {target_t_str}")

            # 翻译回原始语言
            back_t_str = self.translate_text(target_t_str, original_lang, model)
            if back_t_str:
                print(f"Translated back to {original_lang}: {back_t_str}")
            else:
                print(f"Failed to translate back to {original_lang}.")
        else:
            print(f"Failed to translate to {target_lang}.")

        return original_text, target_t_str, back_t_str

    def estimate_tokens(self, text):
        """
        估算文本的 token 数量。

        :param text: 输入的文本
        :return: 估算的 token 数量
        """
        # 统计单词数量
        words = re.findall(r'\b\w+\b', text)
        # 每个单词按 0.7 个 token 估算
        return int(len(words) * 0.7)

    def split_markdown_by_estimated_tokens(self, markdown_text):
        """
        将 Markdown 文档分段，确保每段的 token 数量不超过 max_tokens。

        :param markdown_text: 输入的 Markdown 文档
        :param max_tokens: 每段的最大 token 数量
        :return: 一个包含段落的迭代器和总段数
        """
        paragraphs = []
        current_paragraph = ""
        current_tokens = 0

        # 按行分割 Markdown 文档
        lines = markdown_text.split('\n')

        for line in lines:
            line_tokens = self.estimate_tokens(line)

            # 如果当前段加上新行后超过 token 限制，则结束当前段
            if current_tokens + line_tokens > self.split_token:
                if current_paragraph:
                    paragraphs.append(current_paragraph)
                    current_paragraph = ""
                    current_tokens = 0

            # 添加新行到当前段
            current_paragraph += line + "\n"
            current_tokens += line_tokens

        # 添加最后一段
        if current_paragraph:
            paragraphs.append(current_paragraph)

        return iter(paragraphs), len(paragraphs)

    def compare_diff(self, original_text, back_translated_text, translated_text):
        payload = {
            "model": f"{self.trans_model}",
            "prompt":  f"你是一个回译对比助手，请逐句对比原始文本和回翻文本,指出明显不同之处并将其标记在译文上:\n原始文本: {original_text}\n回译文本: {back_translated_text}\n{translated_text}",
            "stream": False
        }
        response = requests.post(self.OLLAMA_API_URL, json=payload)
        # 检查响应状态
        if response.status_code == 200:
            # 解析响应内容
            compare_result = response.json()
            return compare_result.get("response", "").strip()
        else:
            print(f"Error: {response.status_code}")
            return None

def fetch_result(self, save_to_file: bool = True):
    if (self.iter_cnt >= (self.num_paragraphs - 1)) or (self.paragraphs_iter == None):
        print("对比结果\n" + self.result)
        
        if save_to_file:
            file_path = filedialog.asksaveasfilename(
                parent=self.ui_root,  # 设置父窗口确保对话框置顶
                title="保存翻译结果",
                defaultextension=".md",
                initialfile="zh_translated.md",
                filetypes=[("Markdown文件", "*.md"), ("所有文件", "*.*")]
            )
            # 添加文件保存逻辑
            if file_path:  # 用户没有取消对话框
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(self.result)
                    print(f"结果已保存至：{file_path}")
                except Exception as e:
                    print(f"保存文件时出错：{str(e)}")
        
        return self.result



    def process_translation(self, original_lang="English", target_lang="中文"):
        """
        逐段翻译 Markdown 文档，保留格式。

        :param original_lang: 原始语言
        :param target_lang: 目标语言
        :param model: 使用的模型
        """
        model = self.compare_model
        self.iter_cnt               =   0
        if not self.markdown_content:
            print("未读取到 Markdown 文档。")
            return
        
        for paragraph in self.paragraphs_iter:
            print("\n--- 段落内容 ---")
            print(paragraph)
            original_text, translated_text, back_translated_text = self.trans_unit(paragraph, original_lang, target_lang, model)
            '''
            print("\n--- 翻译结果 ---")
            print(f"原文: {original_text}")
            print(f"翻译: {translated_text}")
            print(f"回译: {back_translated_text}")
           '''
            diff    =   self.compare_diff(original_text, back_translated_text, translated_text)
            print(f"差异：{diff}")
            self.result             +=  translated_text + diff
            self.iter_cnt           +=  1
            print(self.iter_cnt)
            print(self.num_paragraphs)
            self.fetch_result()

    


# 示例用法
if __name__ == "__main__":
    processor = MarkdownProcessor(split_token=128,trans_model="qwen2.5:14b")
    processor.process_translation()
