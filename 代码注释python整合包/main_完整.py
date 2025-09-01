import os
import sys
from pathlib import Path

# 导入我们的模块
sys.path.append('.')

# 导入转PDF模块
from 转pdf import CodeToPDFConverter

# 导入批量注释模块
import 测试批量注释 as batch_analyzer


def get_all_files_from_directory(directory_path, file_extensions=None):
    """
    递归获取目录下的所有文件

    Args:
        directory_path (str): 目录路径
        file_extensions (list): 文件扩展名列表，如 ['.js', '.json', '.wxml', '.wxss']
                               如果为None，则获取所有文件

    Returns:
        list: 文件路径列表
    """
    all_files = []

    # 检查目录是否存在
    if not os.path.exists(directory_path):
        print(f"❌ 目录不存在: {directory_path}")
        return all_files

    if not os.path.isdir(directory_path):
        print(f"❌ 路径不是目录: {directory_path}")
        return all_files

    # 使用 os.walk 递归遍历所有子目录
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)

            # 如果指定了文件扩展名，则进行过滤
            if file_extensions:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in file_extensions:
                    all_files.append(file_path)
            else:
                # 如果没有指定扩展名，添加所有文件
                all_files.append(file_path)

    return all_files


def filter_files_by_type(file_list, include_extensions=None, exclude_extensions=None):
    """
    根据文件类型过滤文件列表

    Args:
        file_list (list): 文件路径列表
        include_extensions (list): 包含的文件扩展名
        exclude_extensions (list): 排除的文件扩展名

    Returns:
        list: 过滤后的文件列表
    """
    filtered_files = []

    for file_path in file_list:
        file_ext = os.path.splitext(file_path)[1].lower()

        # 检查是否在包含列表中
        if include_extensions and file_ext not in include_extensions:
            continue

        # 检查是否在排除列表中
        if exclude_extensions and file_ext in exclude_extensions:
            continue

        filtered_files.append(file_path)

    return filtered_files


def print_file_summary(files_list):
    """打印文件摘要信息"""
    if not files_list:
        print("📄 未找到任何文件")
        return

    # 统计不同类型的文件
    file_types = {}
    for file_path in files_list:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in file_types:
            file_types[ext] = 0
        file_types[ext] += 1

    print(f"📄 找到 {len(files_list)} 个文件:")
    for ext, count in sorted(file_types.items()):
        print(f"   {ext if ext else '(无扩展名)'}: {count} 个")


def main():
    """主处理流程"""

    print("=" * 60)
    print("🚀 代码分析工具 - 交互式配置")
    print("=" * 60)

    # ================================
    # 交互式配置参数
    # ================================

    # 1. 交互式输入源目录
    print("\n📂 请输入源代码目录名称:")
    print("\n(例如: 放置原始代码/healtherreservationMain)")
    print("直接复制该目录的来自内容的根路径粘贴即可")
    while True:
        source_dir_name = input("请输入目录名称: ").strip()
        if source_dir_name:
            source_directory = source_dir_name  # 直接使用输入的目录名
            if os.path.exists(source_directory):
                print(f"✅ 找到目录: {source_directory}")
                break
            else:
                print(f"❌ 目录不存在: {source_directory}")
                retry = input("是否重新输入？(y/n): ").strip().lower()
                if retry != 'y':
                    print("退出程序")
                    return
        else:
            print("❌ 目录名称不能为空")

    # 2. 交互式选择输出文件名格式
    print("\n📝 请选择AI分析结果的文件名格式:")
    print("   1. 不加.txt扩展名 (例如: main.js)")
    print("   2. 加.txt扩展名 (例如: main.js.txt)")

    while True:
        choice = input("请选择 (1 或 2): ").strip()
        if choice == "1":
            add_txt_extension = False
            print("✅ 选择: 不加.txt扩展名")
            break
        elif choice == "2":
            add_txt_extension = True
            print("✅ 选择: 加.txt扩展名")
            break
        else:
            print("❌ 请输入 1 或 2")

    # 将选择传递给批量注释模块
    batch_analyzer.set_output_format(add_txt_extension)

    # ================================
    # 原有的配置参数
    # ================================
    pdf_output_directory = "文件转PDF保存目录"  # PDF输出目录

    # 文件类型过滤配置（可选）
    include_extensions = ['.js', '.json', '.wxml', '.wxss', '.py', '.html', '.css', '.txt', '.md']
    exclude_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.ico', '.svg', '.pdf']  # 排除图片和PDF文件

    print("\n" + "=" * 60)
    print("🚀 开始完整处理流程")
    print("=" * 60)

    # 步骤1: 自动获取目录中的所有文件
    print(f"\n📂 扫描目录: {source_directory}")

    # ... 其余代码保持不变
    all_files = get_all_files_from_directory(source_directory)

    if not all_files:
        print("❌ 目录中没有找到任何文件")
        return

    print(f"📁 原始文件扫描完成，共找到 {len(all_files)} 个文件")

    # 步骤2: 过滤文件类型
    print("\n🔍 过滤文件类型...")
    filtered_files = filter_files_by_type(
        all_files,
        include_extensions=include_extensions,
        exclude_extensions=exclude_extensions
    )

    if not filtered_files:
        print("❌ 过滤后没有找到符合条件的文件")
        return

    print_file_summary(filtered_files)

    # 步骤3: 检查文件是否存在并可读
    print("\n📋 验证文件...")
    valid_files = []
    for file_path in filtered_files:
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                # 尝试读取文件，检查是否可读
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    f.read(1)  # 只读取一个字符来测试
                valid_files.append(file_path)
                print(f"✅ {file_path}")
            except Exception as e:
                print(f"⚠️  文件可能不可读: {file_path} - {str(e)}")
        else:
            print(f"❌ 文件不存在或不是文件: {file_path}")

    if not valid_files:
        print("❌ 没有找到任何有效的源文件，退出程序")
        return

    print(f"\n✅ 验证完成，找到 {len(valid_files)} 个有效文件")

    # 步骤4: 转换为PDF
    print("\n📄 开始转换PDF...")
    converter = CodeToPDFConverter()

    # 确保输出目录存在
    if not os.path.exists(pdf_output_directory):
        os.makedirs(pdf_output_directory)
        print(f"📁 创建PDF输出目录: {pdf_output_directory}")

    # 转换文件
    converted_pdfs = converter.convert_files_list(valid_files, pdf_output_directory)

    if not converted_pdfs:
        print("❌ PDF转换失败，退出程序")
        return

    print(f"\n✅ PDF转换完成，生成了 {len(converted_pdfs)} 个PDF文件:")
    for pdf_file in converted_pdfs:
        print(f"   📄 {pdf_file}")

    # 步骤5: AI分析PDF文件
    print("\n🤖 开始AI分析...")

    # 设置批量注释程序的文件列表
    batch_analyzer.set_file_paths(converted_pdfs)
    batch_analyzer.set_output_format(add_txt_extension)
    # 执行批量分析
    batch_analyzer.process_files_parallel(max_workers=2)  # 减少并行数避免API限制

    print("\n🎉 完整流程执行完成！")
    print(f"📄 PDF文件保存在: {os.path.abspath(pdf_output_directory)}")
    print(f"📊 AI分析结果保存在: {os.path.abspath(batch_analyzer.OUTPUT_FOLDER)}")

    # 显示处理摘要
    print(f"\n📊 处理摘要:")
    print(f"   📂 扫描目录: {source_directory}")
    print(f"   📄 原始文件数: {len(all_files)}")
    print(f"   ✅ 有效文件数: {len(valid_files)}")
    print(f"   📑 生成PDF数: {len(converted_pdfs)}")


if __name__ == "__main__":
    main()