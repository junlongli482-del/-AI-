import requests
import json
import os
import mimetypes
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# 全局配置变量
ADD_TXT_EXTENSION = True  # 默认加.txt扩展名

def set_file_paths(new_file_paths):
    """设置要处理的文件列表"""
    global file_paths, total_count, processed_count
    file_paths = new_file_paths
    total_count = len(file_paths)
    processed_count = 0
    print(f"设置文件列表，共 {total_count} 个文件")

def set_output_format(add_txt_extension):
    """设置输出文件名格式"""
    global ADD_TXT_EXTENSION
    ADD_TXT_EXTENSION = add_txt_extension
    format_text = "加.txt扩展名" if add_txt_extension else "不加.txt扩展名"
    print(f"设置输出格式: {format_text}")

api_url = "http://erp.miraclink.com:5200/v1/chat-messages"
upload_url = "http://erp.miraclink.com:5200/v1/files/upload"
api_key = "app-6cbo3OjMIvCaw9AQGitTZGH7"
user_id = "abc-123"

# 输出文件夹名称
OUTPUT_FOLDER = "注释完成代码文件"

# 需要处理的文件列表
file_paths = [
    # "dify使用.pdf",
    # "Dify+与企业微信集成开发文档.pdf",
    # "main.js.pdf"
    # "healtherreservationMain/main.js",
    # "healtherreservationMain/main.json",
    # "healtherreservationMain/main.wxml",
    # "healtherreservationMain/main.wxss"
]

# 线程安全的计数器
processed_count = 0
total_count = len(file_paths)
lock = threading.Lock()


def get_file_type(filename):
    """根据文件扩展名确定文件类型"""
    extension = os.path.splitext(filename)[1].lower().replace('.', '')

    # 文档类型
    document_extensions = ['txt', 'md', 'markdown', 'pdf', 'html', 'xlsx', 'xls', 'docx', 'csv', 'eml', 'msg', 'pptx',
                           'ppt', 'xml', 'epub']
    # 图片类型
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg']
    # 音频类型
    audio_extensions = ['mp3', 'm4a', 'wav', 'webm', 'amr']
    # 视频类型
    video_extensions = ['mp4', 'mov', 'mpeg', 'mpga']

    if extension in document_extensions:
        return 'document'
    elif extension in image_extensions:
        return 'image'
    elif extension in audio_extensions:
        return 'audio'
    elif extension in video_extensions:
        return 'video'
    else:
        return 'custom'


def upload_file(file_path):
    """
    上传本地文件到服务器 - 直接使用您的成功代码
    """
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return None

    try:
        filename = os.path.basename(file_path)
        file_type = get_file_type(filename)

        # 获取文件的MIME类型
        mime_type, _ = mimetypes.guess_type(file_path)
        if not mime_type:
            mime_type = 'application/octet-stream'

        # 准备上传文件
        files = {
            'file': (filename, open(file_path, 'rb'), mime_type)
        }
        data = {
            'user': user_id
        }

        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        print(f"正在上传文件: {file_path}")
        print(f"文件类型: {file_type}, MIME类型: {mime_type}")

        response = requests.post(
            upload_url,
            headers=headers,
            files=files,
            data=data
        )

        # 修复：201状态码也表示成功（创建成功）
        if response.status_code in [200, 201]:
            upload_data = response.json()
            file_id = upload_data.get("id")
            print(f"✅ 文件上传成功! 文件ID: {file_id}")
            print(f"文件名: {upload_data.get('name')}")
            print(f"文件大小: {upload_data.get('size')} bytes")
            return file_id
        else:
            print(f"❌ 文件上传失败，状态码: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None

    except Exception as e:
        print(f"上传文件时发生错误: {e}")
        return None
    finally:
        if 'files' in locals() and files['file'][1]:
            files['file'][1].close()


def chat_with_file(query, file_ids=None, file_types=None):
    """
    与AI对话，可以包含文件 - 直接使用您的成功代码
    """
    # 准备请求数据
    payload = {
        "inputs": {},
        "query": query,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": user_id,
        "files": []
    }

    # 如果有文件ID，添加到files数组中
    if file_ids and file_types:
        for file_id, file_type in zip(file_ids, file_types):
            payload["files"].append({
                "type": file_type,
                "transfer_method": "local_file",
                "upload_file_id": file_id
            })

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print(f"\n📤 发送请求到AI...")
    print(f"问题: {query}")
    if file_ids:
        print(f"使用文件ID: {file_ids}")

    # 发送请求
    response = requests.post(
        api_url,
        headers=headers,
        data=json.dumps(payload)
    )

    # 处理响应
    if response.status_code == 200:
        print("✅ 请求成功！")
        response_data = response.json()
        answer = response_data.get("answer", "未找到回答")
        print("🤖 AI回复:", answer[:200] + "..." if len(answer) > 200 else answer)  # 只显示前200字符
        return answer
    else:
        print(f"❌ 请求失败，状态码: {response.status_code}")
        print("错误信息:", response.text)
        return None


def get_original_path_from_pdf(pdf_path):
    """
    从PDF路径反推出原始文件路径
    例如: converted_pdfs/healtherreservationMain/main.js.pdf -> healtherreservationMain/main.js
    """
    pdf_path = Path(pdf_path)

    # 移除 converted_pdfs 前缀和 .pdf 后缀
    relative_path = pdf_path.relative_to("converted_pdfs") if str(pdf_path).startswith("converted_pdfs") else pdf_path

    # 移除最后的 .pdf 扩展名
    if str(relative_path).endswith('.pdf'):
        original_path = str(relative_path)[:-4]  # 移除 .pdf
    else:
        original_path = str(relative_path)

    return original_path


def save_response(response, original_file_path):
    """
    保存API响应到TXT文件，保持原始目录结构和文件名区别
    """
    try:
        # 确保输出文件夹存在
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)
            print(f"📁 创建输出文件夹: {OUTPUT_FOLDER}")

        # 🔥 关键修改：从PDF路径反推原始路径
        original_path = get_original_path_from_pdf(original_file_path)

        # 解析路径
        original_path_obj = Path(original_path)

        # 获取目录和完整文件名（包含扩展名）
        directory = original_path_obj.parent
        full_filename = original_path_obj.name  # 包含扩展名的完整文件名

        # 🔥 关键修改：根据用户选择创建输出文件名
        if ADD_TXT_EXTENSION:
            output_filename = f"{full_filename}.txt"  # 加.txt扩展名
        else:
            output_filename = f"{full_filename}"  # 不加.txt扩展名

        # 构建完整的输出路径，保持目录结构
        if directory and str(directory) != '.':
            output_subdir = os.path.join(OUTPUT_FOLDER, str(directory))
            if not os.path.exists(output_subdir):
                os.makedirs(output_subdir, exist_ok=True)
            output_path = os.path.join(output_subdir, output_filename)
        else:
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        # 处理响应内容：去掉代码块标记
        lines = response.strip().split('\n')
        filtered_lines = []

        for line in lines:
            stripped_line = line.strip()
            # 跳过代码块开始和结束标记
            if (stripped_line.startswith('```') and
                    (len(stripped_line) == 3 or stripped_line[3:].isalpha())):  # ```或```javascript等
                continue
            # 跳过只有```的行
            if stripped_line == '```':
                continue
            filtered_lines.append(line)

        # 重新组合内容
        filtered_content = '\n'.join(filtered_lines)

        # 去掉开头和结尾的空行
        filtered_content = filtered_content.strip()

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(filtered_content)

        print(f"💾 响应已保存到: {output_path}")
        print(f"📄 原始行数: {len(lines)}, 过滤后行数: {len(filtered_lines)}")
        return output_path

    except Exception as e:
        print(f"❌ 保存文件时发生错误: {e}")
        return None


def process_single_file(file_path):
    """
    处理单个文件的完整流程 - 去掉PDF转换，直接使用原始文件
    """
    global processed_count

    try:
        print(f"\n🔄 开始处理: {file_path}")

        # 如果是目录，跳过（或者您可以改为处理目录）
        if os.path.isdir(file_path):
            print(f"⚠️  跳过目录处理: {file_path}")
            return

        # 1. 直接上传原始文件（不再转换为PDF）
        file_id = upload_file(file_path)
        if not file_id:
            print(f"❌ 上传失败: {file_path}")
            return

        # 获取文件类型
        filename = os.path.basename(file_path)
        file_type = get_file_type(filename)

        # 2. 与AI对话
        # query = "请详细分析这个文件的内容和结构，并提供完整的分析报告"
        query = "只生成完整代码和注释，不要有代码之外的内容，直接生成，也不要说好的，已经为您生成等非代码话语，如果一定要有，也是在代码里面，加上注释去表达。"



        response = chat_with_file(query, [file_id], [file_type])

        # 3. 保存响应
        if response:
            saved_path = save_response(response, file_path)
            if saved_path:
                print(f"📝 分析结果已保存")

        # 更新进度
        with lock:
            processed_count += 1
            print(f"✅ 完成进度: {processed_count}/{total_count}")

    except Exception as e:
        print(f"❌ 处理文件 {file_path} 时发生错误: {e}")


def process_files_parallel(max_workers=3):
    """
    并行处理所有文件
    """
    print("=" * 60)
    print("🚀 开始批量文件分析")
    print(f"📁 输出文件夹: {OUTPUT_FOLDER}")
    print(f"🔧 并行线程数: {max_workers}")
    print("=" * 60)

    start_time = time.time()

    # 使用线程池并行处理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_file = {
            executor.submit(process_single_file, file_path): file_path
            for file_path in file_paths
        }

        # 等待所有任务完成
        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                future.result()  # 获取结果（如果有异常会在这里抛出）
            except Exception as e:
                print(f"❌ 处理 {file_path} 时发生未捕获的错误: {e}")

    end_time = time.time()
    total_time = end_time - start_time

    print(f"\n🎉 批量处理完成！")
    print(f"⏱️  总耗时: {total_time:.2f} 秒")
    print(f"📊 成功处理: {processed_count}/{total_count} 个文件")
    print(f"📁 结果保存在: {os.path.abspath(OUTPUT_FOLDER)}")


# 使用示例
if __name__ == "__main__":
    # 设置并行工作线程数
    process_files_parallel(max_workers=3)