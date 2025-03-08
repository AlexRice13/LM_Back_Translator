import re
import os
import requests
from tkinter import Tk, filedialog
from tkinter.filedialog import askopenfilename
from typing import Iterator, Optional, Tuple


class MarkdownProcessor:
    DEFAULT_API_URL = "http://localhost:11434/api/generate"
    DEFAULT_MODEL = "hf.co/unsloth/DeepSeek-R1-Distill-Qwen-14B-GGUF:Q6_K"

    def __init__(
        self,
        split_token: int = 128,
        ollama_api_url: str = DEFAULT_API_URL,
        trans_model: str = DEFAULT_MODEL,
        compare_model: str = DEFAULT_MODEL
    ):
        """
        Initialize Markdown Processor with configuration parameters

        :param split_token: Maximum tokens per text segment
        :param ollama_api_url: Ollama API endpoint URL
        :param trans_model: Translation model identifier
        :param compare_model: Comparison model identifier
        """
        self.split_token = split_token
        self.ollama_api_url = ollama_api_url
        self.trans_model = trans_model
        self.compare_model = compare_model

        # Validate input parameters
        if not isinstance(split_token, int) or split_token <= 0:
            raise ValueError("split_token must be a positive integer")

        # Initialize processing state
        self.markdown_content = self._select_and_read_markdown()
        self.markdown_title = ""
        self.result = ""
        self.iter_cnt = 0

        # Initialize document segmentation
        if self.markdown_content:
            self.paragraphs_iter, self.num_paragraphs = self._split_markdown()
            print(f"文档分段数: {self.num_paragraphs}")
        else:
            self.paragraphs_iter = iter([])
            self.num_paragraphs = 0

    def _select_and_read_markdown(self) -> Optional[str]:
        """
        Open file dialog and read selected Markdown file

        :return: File content as string or None
        """
        self.root = Tk(baseName="这个窗口存在代表程序正在运行，我也不知道为什么默认withdraw()隐藏会使得最后的保存窗口蹦不出来")
        self.root.withdraw()
        try:
            file_path = askopenfilename(
                title="选择 Markdown 文件",
                filetypes=[("Markdown 文件", "*.md"), ("所有文件", "*.*")]
            )
            if not file_path:
                print("未选择文件")
                return None

            if content := self._read_file(file_path):
                self.markdown_title = os.path.splitext(
                    os.path.basename(file_path)
                )[0]
                print("文件已读取")
                return content

            print("未读取到文件内容")
            return None
        finally:
            self.root.update()

    @staticmethod
    def _read_file(file_path: str) -> Optional[str]:
        """
        Safely read file contents

        :param file_path: Path to target file
        :return: File content or None
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            print(f"文件未找到: {file_path}")
        except Exception as e:
            print(f"读取文件出错: {str(e)}")
        return None
    
    def _call_api(self, model: str, prompt: str, timeout: int = 3600) -> Optional[str]:
        """
        统一API调用方法，处理请求并过滤推理标签内容
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(
                self.ollama_api_url,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            response_text = response.json().get("response", "").strip()
            
            # 使用正则表达式过滤<THINK>标签内容
            filtered_text = re.sub(
                r'<think>.*?</think>',  # 匹配任意THINK标签内容（包括换行）
                '', 
                response_text,
                flags=re.DOTALL
            )
            return filtered_text
        except requests.exceptions.RequestException as e:
            print(f"API请求失败: {str(e)}")
        except ValueError:
            print("无效的API响应格式")
        return None

    def _translate_text(
        self,
        text: str,
        target_language: str,
        model: str,
        timeout: int = 4096
    ) -> Optional[str]:
        """
        修改后的翻译方法调用统一API接口
        """
        translation_prompt = f"将以下文本翻译为 {target_language}: {text}"
        return self._call_api(model, translation_prompt, timeout)

    def _process_translation_unit(
        self,
        original_text: str,
        source_lang: str = "English",
        target_lang: str = "中文",
        model: str = DEFAULT_MODEL
    ) -> Tuple[str, Optional[str], Optional[str]]:
        """
        Execute bidirectional translation unit

        :return: Tuple of (original, translated, backtranslated)
        """
        # Forward translation
        translated = self._translate_text(original_text, target_lang, model)
        if not translated:
            print(f"{target_lang} 翻译失败")
            return original_text, None, None

        print(f"翻译为 {target_lang}: {translated}")

        # Back translation
        back_translated = self._translate_text(translated, source_lang, model)
        if back_translated:
            print(f"回译为 {source_lang}: {back_translated}")
        else:
            print(f"{source_lang} 回译失败")

        return original_text, translated, back_translated

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Estimate token count using simple heuristic"""
        return int(len(re.findall(r'\b\w+\b', text)) * 0.7)

    def _split_markdown(self) -> Tuple[Iterator[str], int]:
        """
        Split Markdown content into token-limited segments

        :return: Tuple of (paragraph iterator, total count)
        """
        segments = []
        current_segment = []
        current_tokens = 0

        for line in self.markdown_content.split('\n'):
            line_tokens = self._estimate_tokens(line)
            
            if current_tokens + line_tokens > self.split_token:
                if current_segment:
                    segments.append("\n".join(current_segment))
                    current_segment.clear()
                    current_tokens = 0

            current_segment.append(line)
            current_tokens += line_tokens

        if current_segment:
            segments.append("\n".join(current_segment))

        return iter(segments), len(segments)

    def _analyze_differences(
        self,
        original: str,
        back_translated: str,
        translated: str
    ) -> Optional[str]:
        """
        修改后的差异分析方法调用统一API接口
        """
        prompt = (
            "你是一个回译对比助手，请逐句对比原始文本和回翻文本，指出明显不同之处并将其标记在译文上\n"
            f"原始文本: {original}\n"
            f"回译文本: {back_translated}\n"
            f"翻译文本：{translated}"
        )
        return self._call_api(self.compare_model, prompt, timeout=3600)

    def process_translation(
        self,
        source_lang: str = "English",
        target_lang: str = "中文"
    ) -> None:
        """Execute full translation workflow"""
        if not self.markdown_content:
            print("没有可处理的Markdown内容")
            return

        for paragraph in self.paragraphs_iter:
            print("\n--- 处理段落 ---")
            original, translated, back_translated = self._process_translation_unit(
                paragraph, source_lang, target_lang, self.trans_model
            )

            if not translated:
                continue

            analysis = self._analyze_differences(original, back_translated, translated)
            if analysis:
                print(f"差异分析结果: {analysis}")
                self.result += f"{translated}\n{analysis}\n"
            else:
                self.result += f"{translated}\n"

            self.iter_cnt += 1
            print(f"进度: {self.iter_cnt}/{self.num_paragraphs}")
            if (self.iter_cnt == self.num_paragraphs) :
                self._save_result()




    def _save_result(self) -> None:
        """Handle result saving workflow"""
        try:
            save_root = Tk()
            save_root.withdraw()
            save_path = filedialog.asksaveasfilename(
                parent=self.root,
                title="保存翻译结果",
                defaultextension=".md",
                initialfile="zh_translated.md",
                filetypes=[("Markdown文件", "*.md"), ("所有文件", "*.*")]
            )
            if not save_path:
                print("取消保存")
                return

            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(self.result)
                print(f"结果已保存至: {save_path}")
            except IOError as e:
                print(f"保存失败: {str(e)}")
        finally:
            self.root.destroy()


if __name__ == "__main__":
    processor = MarkdownProcessor(split_token=128, trans_model="qwen2.5:14b")
    processor.process_translation()
