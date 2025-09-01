import os
import sys
import json
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 语法高亮库
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
    from pygments.formatters import TerminalFormatter

    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False
    print("建议安装 pygments 以获得语法高亮: pip install pygments")


class CodeToPDFConverter:
    def __init__(self, font_size=10):
        self.font_size = font_size
        self.setup_fonts()

    def setup_fonts(self):
        """设置等宽字体"""
        try:
            # 尝试注册系统等宽字体
            fonts_to_try = [
                ("C:/Windows/Fonts/consola.ttf", "Consolas"),  # Windows
                ("/System/Library/Fonts/Monaco.ttf", "Monaco"),  # macOS
                ("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "DejaVuSansMono"),  # Linux
            ]

            self.mono_font = "Courier"  # 默认字体
            for font_path, font_name in fonts_to_try:
                if os.path.exists(font_path):
                    pdfmetrics.registerFont(TTFont(font_name, font_path))
                    self.mono_font = font_name
                    break
        except Exception as e:
            print(f"字体设置警告: {e}")
            self.mono_font = "Courier"

    def get_lexer_for_file(self, filename):
        """根据文件扩展名获取语法解析器"""
        try:
            if PYGMENTS_AVAILABLE:
                return guess_lexer_for_filename(filename, "")
        except:
            pass
        return None

    def format_code(self, code, language=None):
        """格式化代码（添加行号和语法高亮信息）"""
        lines = code.split('\n')
        formatted_lines = []

        for i, line in enumerate(lines, 1):
            line_num = f"{i:4d}: "
            formatted_lines.append(line_num + line)

        return '\n'.join(formatted_lines)

    def create_styles(self):
        """创建PDF样式"""
        styles = getSampleStyleSheet()

        # 标题样式
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.darkblue,
            spaceAfter=12,
        )

        # 文件信息样式
        info_style = ParagraphStyle(
            'FileInfo',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            spaceAfter=6,
        )

        # 代码样式
        code_style = ParagraphStyle(
            'CodeStyle',
            parent=styles['Code'],
            fontName=self.mono_font,
            fontSize=self.font_size,
            leftIndent=0,
            rightIndent=0,
            spaceAfter=4,
            leading=self.font_size * 1.2,
            backColor=colors.lightgrey,
        )

        return {
            'title': title_style,
            'info': info_style,
            'code': code_style,
            'normal': styles['Normal']
        }

    def convert_code_file(self, input_file, output_pdf=None):
        """将代码文件转换为PDF"""
        input_path = Path(input_file)

        if not input_path.exists():
            print(f"文件不存在: {input_file}")
            return False

        if output_pdf is None:
            output_pdf = input_path.with_suffix('.pdf')

        try:
            # 读取文件内容
            with open(input_file, 'r', encoding='utf-8') as file:
                content = file.read()

            # 创建PDF文档
            doc = SimpleDocTemplate(
                str(output_pdf),
                pagesize=A4,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=50
            )

            # 获取样式
            styles = self.create_styles()
            story = []

            # 添加标题
            title = Paragraph(f"代码文件: {input_path.name}", styles['title'])
            story.append(title)
            story.append(Spacer(1, 12))

            # 添加文件信息
            file_info = f"文件路径: {input_file}<br/>文件大小: {len(content)} 字符<br/>行数: {len(content.split())}"
            info = Paragraph(file_info, styles['info'])
            story.append(info)
            story.append(Spacer(1, 12))

            # 格式化代码
            formatted_code = self.format_code(content)

            # 分割代码为段落（避免单个段落过长）
            lines = formatted_code.split('\n')
            current_chunk = []

            for line in lines:
                current_chunk.append(line)

                # 每50行或遇到空行时创建一个段落
                if len(current_chunk) >= 50 or (line.strip() == '' and len(current_chunk) > 20):
                    if current_chunk:
                        chunk_text = '\n'.join(current_chunk)
                        code_para = Preformatted(chunk_text, styles['code'])
                        story.append(code_para)
                        story.append(Spacer(1, 6))
                        current_chunk = []

            # 处理剩余的代码
            if current_chunk:
                chunk_text = '\n'.join(current_chunk)
                code_para = Preformatted(chunk_text, styles['code'])
                story.append(code_para)

            # 生成PDF
            doc.build(story)
            print(f"成功转换: {input_file} -> {output_pdf}")
            return True

        except Exception as e:
            print(f"转换失败: {e}")
            return False

    def convert_json_file(self, input_file, output_pdf=None):
        """专门处理JSON文件的转换"""
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            # 格式化JSON
            formatted_json = json.dumps(json_data, indent=2, ensure_ascii=False)

            # 创建临时文件进行转换
            temp_file = input_file + '.formatted'
            with open(temp_file, 'w', encoding='utf-8') as file:
                file.write(formatted_json)

            result = self.convert_code_file(temp_file, output_pdf)

            # 清理临时文件
            os.remove(temp_file)
            return result

        except json.JSONDecodeError as e:
            print(f"JSON格式错误: {e}")
            # 如果JSON格式有误，按普通文本处理
            return self.convert_code_file(input_file, output_pdf)

    def batch_convert(self, input_directory, output_directory=None):
        """批量转换目录中的代码文件"""
        input_path = Path(input_directory)
        if not input_path.exists():
            print(f"目录不存在: {input_directory}")
            return

        if output_directory is None:
            output_directory = input_path / "pdf_output"

        output_path = Path(output_directory)
        output_path.mkdir(exist_ok=True)

        # 支持的代码文件扩展名
        code_extensions = {
            '.js', '.json', '.py', '.java', '.cpp', '.c', '.h', '.css', '.html',
            '.xml', '.yaml', '.yml', '.sql', '.php', '.rb', '.go', '.rs', '.ts',
            '.jsx', '.tsx', '.vue', '.sh', '.bat', '.ps1', '.md', '.txt'
        }

        converted_count = 0
        for file_path in input_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in code_extensions:
                relative_path = file_path.relative_to(input_path)
                output_file = output_path / relative_path.with_suffix('.pdf')

                # 创建输出目录
                output_file.parent.mkdir(parents=True, exist_ok=True)

                print(f"转换: {relative_path}")
                if file_path.suffix.lower() == '.json':
                    success = self.convert_json_file(str(file_path), str(output_file))
                else:
                    success = self.convert_code_file(str(file_path), str(output_file))

                if success:
                    converted_count += 1

        print(f"批量转换完成，共转换 {converted_count} 个文件")

    # 在转pdf.py的CodeToPDFConverter类中添加以下方法：

    def convert_files_list(self, file_list, output_directory="pdf_output"):
        """
        转换指定文件列表为PDF，保持原始目录结构
        """
        output_path = Path(output_directory)
        output_path.mkdir(exist_ok=True)

        converted_files = []

        for file_path in file_list:
            file_path = Path(file_path)
            if not file_path.exists():
                print(f"文件不存在: {file_path}")
                continue

            # 🔥 关键修改：保持原始目录结构
            # 保持相对路径结构
            relative_path = file_path

            # 在输出目录中创建相同的目录结构
            output_file = output_path / relative_path.with_suffix(relative_path.suffix + '.pdf')

            # 确保输出目录存在
            output_file.parent.mkdir(parents=True, exist_ok=True)

            print(f"转换: {file_path} -> {output_file}")

            if file_path.suffix.lower() == '.json':
                success = self.convert_json_file(str(file_path), str(output_file))
            else:
                success = self.convert_code_file(str(file_path), str(output_file))

            if success:
                converted_files.append(str(output_file))

        return converted_files


def main():
    """直接在这里设置文件路径"""
    converter = CodeToPDFConverter()

    # 🔥 直接在这里修改你的文件路径 🔥

    # 单文件转换示例
    input_file = "healtherreservationMain/main.js"  # ← 修改这里：输入文件路径
    output_file = "C:\\Users\\Administrator\\Desktop\\CSPD完整文档\\main.js.pdf"  # ← 修改这里：输出文件路径（可选，不写会自动生成）

    # 批量转换示例（注释掉单文件转换，取消下面注释）
    # input_directory = "D:/code_projects"  # ← 修改这里：输入目录
    # output_directory = "D:/pdf_output"    # ← 修改这里：输出目录

    # ========== 选择转换方式 ==========
    # 方式1：单文件转换
    if input_file.endswith('.json'):
        success = converter.convert_json_file(input_file, output_file)
    else:
        success = converter.convert_code_file(input_file, output_file)

    if success:
        print("转换成功！")
    else:
        print("转换失败！")

    # 方式2：批量转换（使用时取消注释，注释掉上面的单文件转换）
    # converter.batch_convert(input_directory, output_directory)
    # print("批量转换完成！")


if __name__ == "__main__":
    main()