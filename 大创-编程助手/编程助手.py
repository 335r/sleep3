import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv
import base64
import re

# 加载环境变量
load_dotenv()

# 设置页面配置
st.set_page_config(
    page_title="AI代码助手",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 设置页面样式 - 白色主题
def set_custom_style():
    st.markdown("""
    <style>
        /* 主容器样式 - 白色背景 */
        .stApp {
            background-color: #ffffff;
            color: #333333;
        }

        /* 对话框容器 */
        .dialog-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        }

        .dialog-content {
            background-color: #ffffff;
            border: 2px solid #4ec9b0;
            border-radius: 10px;
            padding: 25px;
            width: 80%;
            max-width: 600px;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
        }

        .dialog-header {
            color: #4ec9b0;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e0e0e0;
        }

        .dialog-footer {
            margin-top: 20px;
            text-align: right;
        }

        /* 标题样式 */
        h1, h2, h3, h4, h5, h6 {
            color: #2c7bb6 !important;
        }

        /* 侧边栏样式 */
        [data-testid="stSidebar"] {
            background-color: #f5f7fa !important;
            border-right: 1px solid #e0e0e0;
        }

        /* 文本区域样式 - 代码编辑器 */
        .stTextArea textarea {
            background-color: #f8f9fa !important;
            color: #333333 !important;
            font-family: 'Consolas', 'Courier New', monospace !important;
            font-size: 16px !important;
            border: 1px solid #ced4da !important;
        }

        /* 按钮样式 */
        .stButton>button {
            background-color: #2c7bb6 !important;
            color: white !important;
            border: none !important;
            border-radius: 4px !important;
            padding: 8px 16px !important;
            font-weight: bold !important;
            margin-bottom: 10px !important;
            width: 100% !important;
        }

        .stButton>button:hover {
            background-color: #1a5a8e !important;
        }

        .stButton>button:disabled {
            background-color: #8fb3d9 !important;
        }

        /* 对话框按钮 */
        .dialog-button {
            background-color: #4ec9b0 !important;
            color: #ffffff !important;
            font-weight: bold !important;
            min-width: 100px;
        }

        /* 容器样式 */
        [data-testid="stVerticalBlock"] {
            gap: 1rem;
        }

        /* 建议面板样式 */
        .suggestion-item {
            background-color: #f0f8ff;
            border: 1px solid #cce6ff;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
            transition: background-color 0.2s;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .suggestion-item:hover {
            background-color: #e1f0fa;
            cursor: pointer;
        }

        .suggestion-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }

        .suggestion-actions {
            display: flex;
            gap: 10px;
        }

        /* 代码块样式 */
        pre {
            background-color: #f8f9fa !important;
            border-radius: 6px !important;
            padding: 12px !important;
            overflow-x: auto !important;
            border: 1px solid #e0e0e0 !important;
        }

        /* 页脚样式 */
        .footer {
            text-align: center;
            padding: 15px;
            color: #6c757d;
            font-size: 0.9em;
            border-top: 1px solid #e0e0e0;
            margin-top: 20px;
            background-color: #f5f7fa;
        }

        /* 问答样式 */
        .question-bubble {
            background-color: #2c7bb6;
            color: white;
            border-radius: 15px 15px 0 15px;
            padding: 10px 15px;
            margin: 5px 0;
            align-self: flex-end;
            max-width: 80%;
            margin-left: 20%;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .answer-bubble {
            background-color: #f0f8ff;
            color: #333333;
            border-radius: 15px 15px 15px 0;
            padding: 10px 15px;
            margin: 5px 0;
            align-self: flex-start;
            max-width: 80%;
            margin-right: 20%;
            border: 1px solid #cce6ff;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }

        .qa-container {
            display: flex;
            flex-direction: column;
            margin-top: 15px;
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            background-color: #f8f9fa;
        }

        .code-block {
            background-color: #f8f9fa;
            border-radius: 6px;
            padding: 12px;
            overflow-x: auto;
            border: 1px solid #e0e0e0;
            margin: 10px 0;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 14px;
        }

        /* 输入框样式 */
        .stTextInput>div>div>input {
            background-color: #ffffff !important;
            border: 1px solid #ced4da !important;
            color: #333333 !important;
        }

        /* 选择框样式 */
        .stSelectbox>div>div>div>div {
            background-color: #ffffff !important;
            border: 1px solid #ced4da !important;
            color: #333333 !important;
        }

        /* 标签样式 */
        .stMarkdown p, .stMarkdown div {
            color: #333333 !important;
        }

        /* 信息框样式 */
        .stAlert {
            background-color: #e1f0fa !important;
            border: 1px solid #cce6ff !important;
            color: #333333 !important;
        }

        /* 侧边栏链接样式 */
        .sidebar-link {
            display: block;
            text-align: center;
            padding: 8px 16px;
            background-color: #2c7bb6;
            color: white !important;
            border-radius: 4px;
            text-decoration: none;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .sidebar-link:hover {
            background-color: #1a5a8e;
        }

        /* 侧边栏按钮容器 */
        .sidebar-buttons {
            margin-top: 20px;
        }

        /* 分割布局 */
        .editor-container {
            border-right: 1px solid #e0e0e0;
            padding-right: 20px;
        }

        .suggestions-container {
            padding-left: 20px;
            max-height: calc(100vh - 200px);
            overflow-y: auto;
        }

        /* 应用按钮 */
        .apply-btn {
            background-color: #4ec9b0 !important;
            color: #1e1e1e !important;
            font-weight: bold !important;
            padding: 6px 12px !important;
            font-size: 0.9em !important;
        }

        .apply-btn:hover {
            background-color: #3db8a0 !important;
        }

        .copy-btn {
            background-color: #6c757d !important;
            color: white !important;
            padding: 6px 12px !important;
            font-size: 0.9em !important;
        }

        .copy-btn:hover {
            background-color: #5a6268 !important;
        }

        /* 隐藏对话框关闭按钮 */
        [data-testid="baseButton-dialog_close_button"] {
            display: none !important;
        }

        /* 修改位置提示样式 */
        .modify-hint {
            background-color: #fff9db;
            border: 1px solid #ffd43b;
            border-radius: 4px;
            padding: 3px 6px;
            color: #e67700;
            font-weight: bold;
            font-size: 0.85em;
        }

        /* 光标标记样式 */
        .cursor-mark {
            background-color: #fff9db;
            border: 1px dashed #ffd43b;
            padding: 0 2px;
            color: #e67700;
            font-weight: bold;
        }

        /* 建议已应用消息 */
        .suggestion-applied {
            background-color: #e6f7e6;
            border-left: 4px solid #4caf50;
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

set_custom_style()

# 硅基流动API配置
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")  # 移除硬编码的默认值
API_URL = "https://api.siliconflow.cn/v1/chat/completions"

# 初始化会话状态
def init_session_state():
    default_code = {
        "javascript": "// 输入你的JavaScript代码\nfunction hello() {\n  {{cursor}}\n}",
        "python": "# 输入你的Python代码\ndef hello():\n    {{cursor}}",
        "java": "// 输入你的Java代码\npublic class Main {\n    public static void main(String[] args) {\n        {{cursor}}\n    }\n}",
        "html": "<!-- 输入你的HTML代码 -->\n<!DOCTYPE html>\n<html>\n<head>\n    <title>Page</title>\n</head>\n<body>\n    {{cursor}}\n</body>\n</html>",
        "css": "/* 输入你的CSS代码 */\nbody {\n    margin: 0;\n    padding: 0;\n    {{cursor}}\n}",
        "typescript": "// 输入你的TypeScript代码\nfunction hello(name: string): void {\n  {{cursor}}\n}",
        "cpp": "// 输入你的C++代码\n#include <iostream>\n\nint main() {\n    {{cursor}}\n    return 0;\n}"
    }

    if 'code' not in st.session_state:
        st.session_state.code = default_code["javascript"]

    if 'language' not in st.session_state:
        st.session_state.language = "javascript"

    if 'suggestions' not in st.session_state:
        st.session_state.suggestions = []

    if 'loading' not in st.session_state:
        st.session_state.loading = False

    if 'api_key' not in st.session_state:
        st.session_state.api_key = SILICONFLOW_API_KEY

    # 添加对话框状态
    if 'show_dialog' not in st.session_state:
        st.session_state.show_dialog = False

    if 'dialog_title' not in st.session_state:
        st.session_state.dialog_title = ""

    if 'dialog_content' not in st.session_state:
        st.session_state.dialog_content = ""

    # 初始化问答状态
    if 'qa_history' not in st.session_state:
        st.session_state.qa_history = []

    if 'current_question' not in st.session_state:
        st.session_state.current_question = ""

    if 'qa_loading' not in st.session_state:
        st.session_state.qa_loading = False

    # 复制状态
    if 'copied_index' not in st.session_state:
        st.session_state.copied_index = -1

init_session_state()

# 关闭对话框的函数
def close_dialog():
    st.session_state.show_dialog = False

# 显示对话框的函数
def show_dialog(title, content):
    st.session_state.show_dialog = True
    st.session_state.dialog_title = title
    st.session_state.dialog_content = content

# 页面标题
st.title("💻 AI代码助手")
st.caption("使用硅基流动API和Qwen2.5-72B模型提供智能代码补全建议和编程问答")

# 辅助函数 - 解析AI响应并添加修改提示
def parse_ai_suggestions(ai_response):
    suggestions = []
    # 尝试从格式化的响应中提取建议
    suggestion_regex = r"建议\d+:\s*([\s\S]*?)(?=(建议\d+:|$))"
    matches = re.finditer(suggestion_regex, ai_response)

    for match in matches:
        suggestion_text = match.group(1).strip()
        # 移除代码块标记
        if suggestion_text.startswith("```") and suggestion_text.endswith("```"):
            suggestion_text = suggestion_text[3:-3].strip()
            if "\n" in suggestion_text:
                # 移除语言标签
                suggestion_text = suggestion_text.split("\n", 1)[1]

        # 添加修改位置提示 - 使用特殊标记
        suggestion_text = re.sub(
            r'(\b(?:需要修改|请替换|请提供|请输入|请设置|请更改|请调整|请配置|请定义|请指定)\b.*?:?\s*)',
            r'<span class="modify-hint">\g<0></span>',
            suggestion_text,
            flags=re.IGNORECASE
        )

        suggestions.append(suggestion_text)

    # 如果没有匹配到格式化的建议，返回整个响应作为单个建议
    if not suggestions:
        # 尝试移除多余的代码块标记
        cleaned_response = ai_response
        if cleaned_response.startswith("```") and cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[3:-3].strip()
            if "\n" in cleaned_response:
                cleaned_response = cleaned_response.split("\n", 1)[1]

        # 添加修改位置提示
        cleaned_response = re.sub(
            r'(\b(?:需要修改|请替换|请提供|请输入|请设置|请更改|请调整|请配置|请定义|请指定)\b.*?:?\s*)',
            r'<span class="modify-hint">\g<0></span>',
            cleaned_response,
            flags=re.IGNORECASE
        )
        return [cleaned_response]

    return suggestions[:3]  # 最多返回3个建议

# 应用建议到代码
def apply_suggestion(suggestion):
    # 移除HTML标记，只保留纯文本
    clean_suggestion = re.sub(r'<[^>]+>', '', suggestion)

    # 在建议末尾添加新的光标标记
    clean_suggestion += "{{cursor}}"

    if "{{cursor}}" in st.session_state.code:
        # 分割光标前的代码和光标后的代码
        before_cursor, after_cursor = st.session_state.code.split("{{cursor}}", 1)

        # 移除光标后部分中可能存在的其他光标标记
        after_cursor = after_cursor.replace("{{cursor}}", "")

        # 组合新代码
        st.session_state.code = before_cursor + clean_suggestion + after_cursor
    else:
        st.session_state.code += clean_suggestion

    # 使用 Markdown 模拟成功消息并包含 HTML
    st.markdown("""
    <div class="suggestion-applied">
        ✅ 建议已应用! 请检查标记为<span class="modify-hint">黄色</span>的部分并根据需要进行修改
    </div>
    """, unsafe_allow_html=True)

# 复制建议到剪贴板
def copy_suggestion(suggestion, index):
    # 移除HTML标记，只保留纯文本
    clean_suggestion = re.sub(r'<[^>]+>', '', suggestion)

    st.session_state.copied_index = index
    js = f"""
    <script>
        function copyToClipboard() {{
            const text = `{clean_suggestion.replace('`', '`')}`;
            navigator.clipboard.writeText(text)
                .then(() => console.log('Text copied to clipboard'))
                .catch(err => console.error('Error in copying text: ', err));
        }}
        copyToClipboard();
    </script>
    """
    st.components.v1.html(js)

# 生成下载链接
def get_download_link():
    code = st.session_state.code
    language = st.session_state.language

    # 根据语言确定文件扩展名
    extensions = {
        "javascript": "js",
        "python": "py",
        "java": "java",
        "html": "html",
        "css": "css",
        "typescript": "ts",
        "cpp": "cpp"
    }
    ext = extensions.get(language, "txt")
    filename = f"code.{ext}"

    # 创建下载链接
    b64 = base64.b64encode(code.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}" class="sidebar-link">下载代码</a>'

# 获取AI建议
def get_ai_suggestions():
    # 检查API密钥
    if not st.session_state.api_key:
        show_dialog("API密钥错误", "请提供有效的硅基流动API密钥")
        return

    code = st.session_state.code
    language = st.session_state.language
    api_key = st.session_state.api_key

    # 检查光标标记
    if "{{cursor}}" not in code:
        show_dialog("缺少光标标记",
                    "请在代码中添加 <span class='cursor-mark'>{{cursor}}</span> 标记以指示AI辅助位置<br><br>"
                    "您可以在侧边栏使用'添加光标标记'按钮快速添加",
                    unsafe_allow_html=True)
        return

    # 创建提示词 - 要求AI标注需要修改的位置
    prompt = f"""你是一个{language}代码专家。用户正在编辑代码，当前光标位置标记为`{{cursor}}`。
以下是当前代码：
```{language}
{code}

请提供最多3个简洁的代码补全建议，每个建议只包含需要插入到光标位置的代码片段（不需要包含完整代码）。
每个建议应该以"建议X:"开头，后面跟着代码片段（用代码块包裹）。

在建议中：
1. 对于需要用户自定义的部分（如变量名、参数值等），使用注释明确标注，例如：
   // 请替换为你的变量名
   # 请设置合适的参数值
2. 对于需要用户添加逻辑的位置，使用TODO注释标注
3. 使用清晰的标注语言提示用户需要修改的位置
"""

    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "Qwen/Qwen2.5-72B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 500,
            "temperature": 0.2
        }

        st.session_state.loading = True
        st.session_state.suggestions = []
        st.session_state.copied_index = -1

        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        ai_response = response.json()["choices"][0]["message"]["content"].strip()
        st.session_state.suggestions = parse_ai_suggestions(ai_response)

    except requests.exceptions.RequestException as e:
        error_msg = f"API错误: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_msg = f"{error_msg}\n详细信息: {error_details.get('error', {}).get('message', '未知错误')}"
            except:
                pass
        show_dialog("API错误", error_msg)

    except Exception as e:
        show_dialog("发生错误", f"处理请求时出错: {str(e)}")

    finally:
        st.session_state.loading = False

# 获取AI回答
def get_ai_answer():
    # 检查API密钥
    if not st.session_state.api_key:
        show_dialog("API密钥错误", "请提供有效的硅基流动API密钥")
        return

    if not st.session_state.current_question:
        show_dialog("问题为空", "请输入您的问题")
        return

    api_key = st.session_state.api_key
    language = st.session_state.language

    # 构建提示词
    prompt = f"""你是一个专业的{language}开发工程师。请回答以下编程问题：
问题：{st.session_state.current_question}

请提供：
1. 清晰的问题分析
2. 解决方案（包含代码示例）
3. 代码说明和最佳实践建议
4. 相关资源推荐（如有）"""

    try:
        st.session_state.qa_loading = True

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "Qwen/Qwen2.5-72B-Instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1024,
            "temperature": 0.3
        }

        response = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()

        ai_response = response.json()["choices"][0]["message"]["content"].strip()

        # 添加到问答历史
        st.session_state.qa_history.append({
            "role": "user",
            "content": st.session_state.current_question
        })
        st.session_state.qa_history.append({
            "role": "assistant",
            "content": ai_response
        })

        # 清空当前问题
        st.session_state.current_question = ""

    except requests.exceptions.RequestException as e:
        error_msg = f"API错误: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_msg = f"{error_msg}\n详细信息: {error_details.get('error', {}).get('message', '未知错误')}"
            except:
                pass
        show_dialog("API错误", error_msg)

    except Exception as e:
        show_dialog("发生错误", f"处理请求时出错: {str(e)}")

    finally:
        st.session_state.qa_loading = False

# 语言选择
languages = {
    "JavaScript": "javascript",
    "Python": "python",
    "Java": "java",
    "HTML": "html",
    "CSS": "css",
    "TypeScript": "typescript",
    "C++": "cpp"
}

# 侧边栏配置
with st.sidebar:
    st.subheader("配置")

    # 语言选择
    selected_lang_name = st.selectbox(
        "编程语言",
        list(languages.keys()),
        index=0
    )
    st.session_state.language = languages[selected_lang_name]

    # 在侧边栏中添加重置按钮
    if st.button("重置代码模板", use_container_width=True):
        templates = {
            "javascript": "// 输入你的JavaScript代码\nfunction hello() {\n {{cursor}}\n}",
            "python": "# 输入你的Python代码\ndef hello():\n {{cursor}}",
            "java": "// 输入你的Java代码\npublic class Main {\n public static void main(String[] args) {\n {{cursor}}\n }\n}",
            "html": "<!-- 输入你的HTML代码 -->\n<!DOCTYPE html>\n<html>\n<head>\n <title>Page</title>\n</head>\n<body>\n {{cursor}}\n</body>\n</html>",
            "css": "/* 输入你的CSS代码 */\nbody {\n margin: 0;\n padding: 0;\n {{cursor}}\n}",
            "typescript": "// 输入你的TypeScript代码\nfunction hello(name: string): void {\n {{cursor}}\n}",
            "cpp": "// 输入你的C++代码\n#include <iostream>\n\nint main() {\n {{cursor}}\n return 0;\n}"
        }
        st.session_state.code = templates[st.session_state.language]
        st.markdown("""
        <div class="suggestion-applied">
            ✅ 代码模板已重置!
        </div>
        """, unsafe_allow_html=True)

    # API密钥配置
    api_key = st.text_input(
        "硅基流动API密钥",
        value=st.session_state.api_key,
        type="password",
        help="从硅基流动平台获取API密钥"
    )
    st.session_state.api_key = api_key

    st.divider()

    # 添加关于对话框按钮
    if st.button("关于此应用", key="about_app", use_container_width=True):
        show_dialog("关于 AI 代码助手", """
        **版本 1.7**

        **安全更新:**
        - 移除了硬编码的API密钥，确保安全
        - 增强API密钥验证机制

        **功能改进:**
        - 应用建议后自动添加新的光标标记
        - 优化光标位置管理
        - 增强用户界面提示

        **功能说明:**
        - 支持多种编程语言的代码编辑
        - 使用 Qwen2.5-72B 模型提供智能代码补全建议
        - 在代码中标记光标位置以获取上下文相关的建议
        - 下载生成的代码文件
        - 编程问答功能

        **使用指南:**
        1. 在代码编辑器中编写代码
        2. 在需要 AI 帮助的位置添加 {{cursor}} 标记
        4. 点击"获取AI建议"按钮
        5. 从建议中选择一个插入
        6. 检查黄色高亮部分并根据需要进行修改

        **技术栈:**
        - Streamlit 前端框架
        - SiliconFlow API
        - Qwen2.5-72B 模型

        **快捷键:**
        - Ctrl+Enter: 获取AI建议

        © 2024 AI 代码助手 | 由硅基流动提供技术支持
        """)

    st.info("使用Qwen2.5-72B模型提供代码建议和编程问答", icon="🤖")

    # 使用指南
    st.divider()
    st.subheader("使用指南")
    st.markdown("""
    1. 在代码编辑器中编写代码

    2. 在需要AI帮助的位置添加 <span class='cursor-mark'>{{cursor}}</span> 标记

    3. 点击"获取AI建议"按钮

    4. 从建议中选择一个插入

    5. 检查黄色高亮部分并根据需要进行修改

    6. 在问答区域输入编程问题获取解答
    """, unsafe_allow_html=True)

    st.markdown("快捷键:")
    st.markdown("- Ctrl+Enter: 获取AI建议")

    # 编辑器操作按钮
    st.divider()
    st.subheader("编辑器操作")

    if st.button("添加光标标记", key="add_marker", use_container_width=True):
        st.session_state.code += "{{cursor}}"
        st.markdown("""
        <div class="suggestion-applied">
            ✅ 光标标记已添加!
        </div>
        """, unsafe_allow_html=True)

    st.button(
        "获取AI建议",
        on_click=get_ai_suggestions,
        disabled=st.session_state.loading,
        use_container_width=True
    )

    if st.button("清除建议", disabled=st.session_state.loading, use_container_width=True):
        st.session_state.suggestions = []
        st.markdown("""
        <div class="suggestion-applied">
            ✅ 建议已清除!
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.caption("由硅基流动提供AI支持 • 基于Streamlit构建")
    st.caption(f"版本 1.7 • {time.strftime('%Y-%m-%d')}")

# 创建主布局 - 分割为左右两半
col_editor, col_suggestions = st.columns([1, 1])

# 左侧：代码编辑器
with col_editor:
    st.subheader("代码编辑器")
    st.caption(
        "提示：在代码中添加 <span class='cursor-mark'>{{cursor}}</span> 标记以指示AI辅助位置，然后点击侧边栏的'获取AI建议'按钮",
        unsafe_allow_html=True)

    st.session_state.code = st.text_area(
        "编辑代码",
        value=st.session_state.code,
        height=500,
        key="code_editor",
        label_visibility="collapsed",
        placeholder=f"在这里输入你的{st.session_state.language}代码..."
    )

    if st.session_state.loading:
        st.info("AI正在思考中... 请稍候")

    st.markdown(get_download_link(), unsafe_allow_html=True)

    # 添加问答功能
    st.divider()
    st.subheader("编程问答")
    st.write(f"向AI咨询关于{selected_lang_name}编程的问题")

    question_col, button_col = st.columns([5, 1])
    with question_col:
        st.text_input(
            "输入您的编程问题",
            key="current_question",
            placeholder=f"例如：如何在{selected_lang_name}中实现排序算法？",
            label_visibility="collapsed"
        )

    with button_col:
        st.button(
            "提问",
            on_click=get_ai_answer,
            disabled=st.session_state.qa_loading,
            use_container_width=True
        )

    if st.session_state.qa_history:
        st.markdown("<div class='qa-container'>", unsafe_allow_html=True)

        for item in st.session_state.qa_history:
            if item["role"] == "user":
                st.markdown(f"<div class='question-bubble'>{item['content']}</div>", unsafe_allow_html=True)
            else:
                content = item['content']

                code_blocks = re.findall(r'```(.*?)```', content, re.DOTALL)
                for i, code_block in enumerate(code_blocks):
                    content = content.replace(f"```{code_block}```", f"{{{{CODE_BLOCK_{i}}}}}", 1)

                parts = re.split(r'{{CODE_BLOCK_\d+}}', content)

                for part in parts:
                    if part.strip():
                        st.markdown(f"<div class='answer-bubble'>{part}</div>", unsafe_allow_html=True)

                for i, code_block in enumerate(code_blocks):
                    if code_block.strip():
                        lang = st.session_state.language
                        if '\n' in code_block:
                            first_line, rest = code_block.split('\n', 1)
                            if first_line.strip() in languages.values():
                                lang = first_line.strip()
                                code_block = rest
                            else:
                                code_block = first_line + '\n' + rest

                        st.code(code_block, language=lang)

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("清空问答历史", key="clear_qa_history"):
            st.session_state.qa_history = []

    elif st.session_state.qa_loading:
        st.info("AI正在思考中... 请稍候")
    else:
        st.info("在此输入您的编程问题，AI将为您提供专业解答")

# 右侧：AI建议
with col_suggestions:
    st.subheader("AI建议")
    st.caption("建议中的<span class='modify-hint'>黄色标记</span>表示需要您修改或自定义的部分", unsafe_allow_html=True)

    if st.session_state.suggestions:
        st.info(f"找到 {len(st.session_state.suggestions)} 个建议，选择一个应用到代码中")

        for i, suggestion in enumerate(st.session_state.suggestions):
            with st.container():
                st.markdown("<div class='suggestion-item'>", unsafe_allow_html=True)

                st.markdown("<div class='suggestion-header'>", unsafe_allow_html=True)
                st.markdown(f"**建议 #{i + 1}**")

                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    st.button(f"应用", key=f"apply_{i}",
                              help="将此建议应用到代码中光标位置",
                              use_container_width=True,
                              type="primary",
                              on_click=apply_suggestion, args=(suggestion,))

                with col2:
                    st.button(f"复制", key=f"copy_{i}",
                              help="复制建议到剪贴板",
                              use_container_width=True,
                              on_click=copy_suggestion, args=(suggestion, i))

                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown(f"""
                <div class="code-block">
                    <pre><code>{suggestion}</code></pre>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                if st.session_state.copied_index == i:
                    st.success("建议已复制到剪贴板!")

    elif st.session_state.loading:
        st.info("正在生成建议...")
    else:
        st.info("点击侧边栏的'获取AI建议'按钮获取代码建议")

# 创建对话框容器
if st.session_state.show_dialog:
    dialog_container = st.container()
    with dialog_container:
        st.markdown(
            f"""
            <div class="dialog-container">
                <div class="dialog-content">
                    <div class="dialog-header">{st.session_state.dialog_title}</div>
                    <div>{st.session_state.dialog_content}</div>
                    <div class="dialog-footer">
                        <button class="dialog-button" onclick="window.closeDialog()">关闭</button>
                    </div>
                </div>
            </div>
            <script>
                function closeDialog() {{
                    // 使用 Streamlit 的 setComponentValue 方法关闭对话框
                    window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'dialog_close'}}, '*');
                }}
            </script>
            """,
            unsafe_allow_html=True
        )

# 添加 JavaScript 回调处理
st.components.v1.html(
    """
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'streamlit:setComponentValue' && event.data.value === 'dialog_close') {
            // 发送关闭对话框的请求到 Streamlit
            const data = {value: "dialog_close"};
            window.parent.postMessage({
                type: 'streamlit:componentMessage',
                componentId: 'dialog_handler',
                data: data
            }, '*');
        }
    });
    </script>
    """,
    height=0
)

# 处理对话框关闭事件
if "dialog_handler" in st.session_state and st.session_state.dialog_handler == 'dialog_close':
    close_dialog()
    st.session_state.dialog_handler = None