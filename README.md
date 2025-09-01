🚀 代码分析工具使用指南

📋 项目简介

这是一个智能代码分析工具，能够自动将代码文件转换为PDF并通过AI进行详细分析，生成带注释的代码文档。

主要功能：
- 📁 批量扫描指定目录下的代码文件
- 这里可以调整 测试批量注释.py 文件里的main主程序手动更改并行数量提高效率
- 📄 将代码文件转换为格式化的PDF文档
- 🤖 使用AI智能分析代码并生成详细注释
- 💾 支持多种输出格式和目录结构保持
- 我们使用的AI平台为本地部署的DIFY平台

---

🛠️ 环境要求与依赖安装

系统要求
- Python版本： Python 3.7 或更高版本
- 操作系统： Windows、macOS、Linux
必需依赖包

包名
版本要求
用途说明
reportlab
≥3.6.0
PDF文档生成和格式化
requests
≥2.25.0
HTTP请求处理，用于AI接口调用
pygments
≥2.10.0
代码语法高亮（可选，推荐安装）

安装方法

方法一：直接安装
pip install reportlab requests pygments

方法二：使用requirements.txt
创建 requirements.txt 文件：
reportlab>=3.6.0
requests>=2.25.0
pygments>=2.10.0

然后执行：
pip install -r requirements.txt

方法三：使用国内镜像（解决网络问题）
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple reportlab requests pygments


---

📁 项目文件结构
这个结构无需在意，只需知道你需要解析的代码文件或整个目录放进来即可，使用时粘贴目录的相对路径。

代码分析项目/
├── main.py                    # 🎯 主程序文件（程序入口）
├── 转pdf.py                   # 📄 PDF转换模块
├── 测试批量注释.py              # 🤖 AI分析模块
├── requirements.txt           # 📦 依赖包列表
├── healtherreservationMain/   # 📂 源代码目录（示例）
│   ├── main.js               # JavaScript文件
│   ├── main.json             # JSON配置文件
│   ├── main.wxml             # 微信小程序模板文件
│   └── main.wxss             # 微信小程序样式文件
├── converted_pdfs/            # 📑 PDF输出目录（自动创建）
│   └── healtherreservationMain/
│       ├── main.js.pdf
│       ├── main.json.pdf
│       ├── main.wxml.pdf
│       └── main.wxss.pdf
└── ai_analysis_results/       # 📊 AI分析结果目录（自动创建）
    └── healtherreservationMain/
        ├── main.js.txt
        ├── main.json.txt
        ├── main.wxml.txt
        └── main.wxss.txt


---

💻 VS Code 使用指南

第1步：环境准备

1.1 安装VS Code
- 📥 下载地址：https://code.visualstudio.com/
- 选择对应操作系统版本并安装
1.2 安装Python扩展
1. 打开VS Code
2. 按 Ctrl+Shift+X 打开扩展面板
3. 搜索 "Python"
4. 安装 Microsoft 官方的Python扩展
第2步：项目设置

2.1 打开项目
方法一：通过菜单
- 文件 → 打开文件夹 → 选择项目文件夹
方法二：通过命令行
cd 你的项目路径
code .

2.2 配置Python解释器
这一步可能有点问题，你应该去创建一个虚拟环境会比较好。
5. 按 Ctrl+Shift+P 打开命令面板
6. 输入 "Python: Select Interpreter"
7. 选择Python 3.7+版本
第3步：安装依赖

3.1 使用VS Code内置终端
8. 按 `Ctrl+`` 打开终端
9. 运行安装命令：
10. 这一步如果2.2没有完成，他会指引你安装虚拟环境，根据指引去做即可。
pip install reportlab requests pygments

3.2 验证安装
pip list | grep reportlab
pip list | grep requests  
pip list | grep pygments

第4步：运行程序

4.1 直接运行（推荐）
11. 打开 main.py 文件
12. 点击右上角 "▶️ Run Python File" 按钮
13. 或按快捷键 Ctrl+F5
4.2 调试模式运行
14. 按 F5 启动调试
15. 首次运行选择 "Python File" 配置
4.3 终端运行
python main.py

第5步：VS Code优化配置
这一步内容无需理会

5.1 创建launch.json（调试配置）
在项目根目录创建 .vscode/launch.json：
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: 运行主程序",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "justMyCode": true,
            "cwd": "${workspaceFolder}"
        }
    ]
}

5.2 创建settings.json（项目设置）
在项目根目录创建 .vscode/settings.json：
{
    "python.defaultInterpreterPath": "python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "files.encoding": "utf8",
    "python.terminal.activateEnvironment": true,
    "files.autoSave": "afterDelay",
    "editor.formatOnSave": true
}

🔧 VS Code实用技巧

功能
快捷键
说明
代码格式化
Shift+Alt+F
自动格式化当前文件
变量重命名
F2
批量重命名选中的变量
跳转定义
F12
跳转到函数/变量定义
多光标编辑
Ctrl+Alt+↑/↓
添加多个编辑光标
命令面板
Ctrl+Shift+P
打开所有命令
文件搜索
Ctrl+P
快速打开文件


---

🔧 PyCharm 使用指南

第1步：环境准备

1.1 安装PyCharm
- 📥 **专业版**：https://www.jetbrains.com/pycharm/
- 📥 **社区版**（免费）：https://www.jetbrains.com/pycharm/download/#section=windows
- 推荐使用专业版，功能更全面
1.2 激活PyCharm（专业版）
- 学生可免费使用：https://www.jetbrains.com/student/
- 或使用30天试用版
第2步：创建项目

2.1 新建项目
16. 启动PyCharm
17. Create New Project
18. 选择项目位置
19. 配置Python解释器
  - New environment using: Virtualenv
  - Base interpreter: 选择Python 3.7+
2.2 导入现有项目
20. Open
21. 选择包含代码文件的文件夹
22. 选择 This Window 或 New Window
第3步：配置Python解释器

3.1 检查解释器设置
23. File → Settings (Windows) / PyCharm → Preferences (Mac)
24. Project → Python Interpreter
25. 确认选择了正确的Python版本
3.2 添加新的解释器（如需要）
26. 点击齿轮图标 ⚙️ → Add
27. 选择 Virtualenv Environment
28. 选择Python基础解释器
第4步：安装依赖包

4.1 使用PyCharm Package Manager（推荐）
29. File → Settings → Project → Python Interpreter
30. 点击 ➕ 按钮
31. 搜索并安装以下包：
  - reportlab
  - requests 
  - pygments
4.2 使用Terminal
32. View → Tool Windows → Terminal
33. 运行安装命令：
pip install reportlab requests pygments

4.3 使用requirements.txt
34. 创建 requirements.txt 文件
35. 右键文件 → Install Requirements
第5步：运行程序

5.1 直接运行
36. 右键 main.py → Run 'main'
37. 或点击代码编辑器右上角的绿色三角形 ▶️
38. 快捷键：Ctrl+Shift+F10
5.2 创建运行配置
39. Run → Edit Configurations
40. 点击 ➕ → Python
41. 配置以下项：
  - Name: 代码分析工具
  - Script path: 选择 main.py
  - Working directory: 项目根目录
5.3 调试模式
42. 在代码行号左边点击添加断点 🔴
43. 右键 main.py → Debug 'main'
44. 或按 Shift+F9
第6步：PyCharm优化配置

6.1 编码设置
45. File → Settings → Editor → File Encodings
46. 设置所有编码为 UTF-8
6.2 代码风格
47. File → Settings → Editor → Code Style → Python
48. 可选择PEP 8标准
6.3 自动保存
49. File → Settings → Appearance & Behavior → System Settings
50. 勾选相关自动保存选项
🔧 PyCharm实用技巧

功能
快捷键
说明
代码格式化
Ctrl+Alt+L
格式化当前文件
优化导入
Ctrl+Alt+O
自动整理import语句
变量重命名
Shift+F6
智能重命名变量
快速修复
Alt+Enter
显示建议修复
运行程序
Shift+F10
运行当前配置
调试程序
Shift+F9
调试当前配置
查找文件
Ctrl+Shift+N
按名称查找文件
全局搜索
Ctrl+Shift+F
在项目中搜索文本


---

🎯 程序使用流程

交互式配置
运行程序后，会有以下交互提示：

============================================================
🚀 代码分析工具 - 交互式配置
============================================================

📂 请输入源代码目录名称:
   (例如: healtherreservationMain)
请输入目录名称: healtherreservationMain
✅ 找到目录: healtherreservationMain

📝 请选择AI分析结果的文件名格式:
   1. 不加.txt扩展名 (例如: main.js)
   2. 加.txt扩展名 (例如: main.js.txt)
请选择 (1 或 2): 1
✅ 选择: 不加.txt扩展名

处理流程
51. 📂 文件扫描: 自动扫描指定目录下的所有代码文件
52. 📄 PDF转换: 将代码文件转换为格式化的PDF文档  
53. 🤖 AI分析: 上传PDF到AI服务进行智能分析
54. 💾 结果保存: 将分析结果保存为文本文件
支持的文件类型
- JavaScript: .js
- JSON: .json  
- 微信小程序: .wxml, .wxss
- Python: .py
- Web: .html, .css
- 文档: .txt, .md

---

❗ 常见问题解决

安装问题

问题
解决方案
pip不是内部或外部命令
重新安装Python，勾选"Add Python to PATH"
权限错误
使用 pip install --user 或管理员权限运行
网络问题
使用国内镜像源：-i https://pypi.tuna.tsinghua.edu.cn/simple
字体错误
确保系统有等宽字体（Consolas/Monaco/DejaVu）

运行问题

问题
解决方案
找不到模块
确认所有.py文件在同一目录，检查import语句
编码错误
在文件开头添加 # -*- coding: utf-8 -*-
中文乱码
设置IDE编码为UTF-8
API调用失败
检查网络连接和API密钥配置

IDE特定问题

VS Code
- Python解释器未找到: Ctrl+Shift+P → "Python: Select Interpreter"
- 终端中文乱码: 设置 → 搜索"encoding" → 设为"utf8"
PyCharm
- 项目结构错误: 右键项目根目录 → "Mark Directory as" → "Sources Root"
- 导入错误: File → Settings → Project Structure → 添加Content Root

---

🎉 预期输出结果

成功运行后的目录结构：
项目目录/
├── converted_pdfs/               # PDF转换结果
│   └── healtherreservationMain/
│       ├── main.js.pdf          # 带行号和格式化的代码PDF
│       ├── main.json.pdf        # JSON格式化PDF
│       ├── main.wxml.pdf        # 模板文件PDF
│       └── main.wxss.pdf        # 样式文件PDF
└── ai_analysis_results/          # AI分析结果  
    └── healtherreservationMain/
        ├── main.js.txt          # AI生成的详细注释代码
        ├── main.json.txt        # 配置文件说明
        ├── main.wxml.txt        # 模板结构分析
        └── main.wxss.txt        # 样式规则解释

控制台输出示例：
🎉 完整流程执行完成！
📄 PDF文件保存在: /项目路径/converted_pdfs
📊 AI分析结果保存在: /项目路径/ai_analysis_results

📊 处理摘要:
   📂 扫描目录: healtherreservationMain
   📄 原始文件数: 4
   ✅ 有效文件数: 4
   📑 生成PDF数: 4
   ⏱️  总耗时: 74.29 秒


---
我来详细说明如何在IntelliJ IDEA中使用这个Python代码项目。

🚀 IntelliJ IDEA Python开发完整指南

第1步：安装和配置IDEA

1.1 安装IntelliJ IDEA
- Ultimate版（推荐）：https://www.jetbrains.com/idea/
- Community版（免费）：功能有限，但可以通过插件支持Python
1.2 安装Python插件
1. 启动IDEA
2. File → Settings → Plugins
3. 搜索 "Python" 
4. 安装 Python 插件（JetBrains官方）
5. 重启IDEA
第2步：创建Python项目
注：执行2.2即可
2.1 新建项目
File → New → Project
├── 选择 "Python" 
├── 设置项目位置
├── 选择Python解释器
└── Create

2.2 导入现有项目
File → Open
├── 选择包含Python文件的文件夹
├── 选择 "This Window" 或 "New Window"
└── IDEA会自动识别为Python项目

第3步：配置Python解释器

3.1 设置项目解释器
6. File → Project Structure → SDKs
7. 点击 ➕ → Add Python SDK
8. 选择以下选项之一：
  - System Interpreter: 使用系统Python
  - Virtualenv Environment: 创建虚拟环境（选择创建虚拟环境这一个）
  - Conda Environment: 使用Anaconda
3.2 验证解释器配置
9. 文件-项目结构-项目设置-项目
[图片]
10. 文件-项目结构-项目设置-模块
[图片]
第4步：项目文件结构设置
注：无需过于关注，大部分运行后自动创建
手动操作：
1.将需要解析的代码放进去即可，最好以文件夹的形式
2.如果没有依赖文件，将依赖文件放进去
3.与main.py同级即可
代码分析项目/
├── .idea/                     # IDEA配置文件（自动生成）
├── venv/                      # 虚拟环境（可选）
├── main.py                    # 主程序文件
├── 转pdf.py                   # PDF转换模块
├── 测试批量注释.py              # AI分析模块
├── requirements.txt           # 依赖列表
├── LICENSE                    # 许可证文件
├── README.md                  # 项目说明
├── healtherreservationMain/   # 源代码目录
│   ├── main.js
│   ├── main.json
│   ├── main.wxml
│   └── main.wxss
├── converted_pdfs/            # PDF输出（自动创建）
└── ai_analysis_results/       # AI分析结果（自动创建）

第5步：安装Python依赖

5.1 使用IDEA内置包管理器
11. File → Settings → Project → Python Interpreter
12. 点击包列表下方的 ➕ 按钮
13. 搜索并安装以下包：
reportlab
requests
pygments
5.2 使用Terminal
14. View → Tool Windows → Terminal
15. 在终端中运行：
pip install reportlab requests pygments
5.3 使用requirements.txt
（选择此方式，若出现pip错误，则为python没有配置好，回去看配置python的两个步骤，项目与模块是否都配置了python）
16. 创建 requirements.txt 文件：
reportlab>=3.6.0
requests>=2.25.0
pygments>=2.10.0
17. 在Terminal中运行：
pip install -r requirements.txt

第6步：运行程序

6.1 直接运行
- 右键 main.py → Run 'main'
- 或点击编辑器右上角的绿色三角形 ▶️
- 快捷键：Ctrl+Shift+F10
❗ 常见问题解决

问题1：Python解释器未配置
解决方案：
File → Project Structure → SDKs → Add Python SDK
选择系统Python或创建虚拟环境

问题2：模块导入错误
解决方案：
1. 确认所有.py文件在项目根目录
2. 右键项目根目录 → Mark Directory as → Sources Root
3. 检查Python解释器路径

问题3：中文编码问题
解决方案：
File → Settings → Editor → File Encodings
设置所有编码为UTF-8

问题4：依赖包安装失败
解决方案：
1. 检查网络连接
2. 使用国内镜像：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple
3. 更新pip：python -m pip install --upgrade pip

🎯 IDEA专属优势

18. 智能代码补全: 强大的代码提示和自动补全
19. 重构支持: 安全的代码重构功能
20. 集成调试器: 功能丰富的调试工具
21. 版本控制: 深度集成Git等版本控制系统
22. 插件生态: 丰富的插件支持
23. 数据库工具: 内置数据库管理工具
24. HTTP客户端: 内置REST客户端测试API
现在你可以在IntelliJ IDEA中愉快地使用这个Python代码分析工具了！如果遇到任何问题，IDEA的智能提示和错误检测会帮助你快速定位和解决问题。




📞 技术支持

如果在使用过程中遇到问题，请提供以下信息：
- 操作系统和版本
- Python版本
- IDE类型和版本
- 具体错误信息
- 项目文件结构
祝您使用愉快！ 🚀

文档主编：李先生（研发部：AI工程师）
时间：2025.9.1
