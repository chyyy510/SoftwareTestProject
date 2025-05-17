import ast
import json
import os
import re
import time

from dotenv import load_dotenv

# from flask import Flask, jsonify, request
from qianfan import ChatCompletion  # 确保已正确导入

load_dotenv()
# app = Flask(__name__)


# 代码解析模块
def parse_code(source_code):
    """
    解析代码中的函数定义，返回函数的名称、参数列表、返回值类型、装饰器、文档字符串等信息。
    """
    tree = ast.parse(source_code)
    function_definitions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_info = {
                "name": node.name,
                "args": [],
                "returns": None,
                "decorators": [],
                "docstring": ast.get_docstring(node),
                "default_args": [],
                "arg_types": [],
            }

            for arg in node.args.args:
                arg_info = {"name": arg.arg}
                arg_info["type"] = ast.dump(arg.annotation) if arg.annotation else None
                function_info["args"].append(arg_info)

            if node.returns:
                function_info["returns"] = ast.dump(node.returns)

            if node.decorator_list:
                function_info["decorators"] = [
                    (
                        decorator.id
                        if isinstance(decorator, ast.Name)
                        else ast.dump(decorator)
                    )
                    for decorator in node.decorator_list
                ]

            defaults = node.args.defaults
            for default in defaults:
                function_info["default_args"].append(ast.dump(default))

            function_definitions.append(function_info)

    return function_definitions


# 使用百度云的 qianfan.ChatCompletion 接口分析代码
def analyze_code_with_openai(source_code):
    """
    使用百度云的 qianfan.ChatCompletion 接口分析代码并返回分析结果。
    """
    try:
        chat_comp = ChatCompletion()
        prompt = f"""
以下是一些 Python 函数的代码片段，请为每个函数生成 3 组测试用例。
测试用例应包括：
1. 输入参数
2. 期望的输出结果
3. 参数的类型尽可能多样丰富，不局限于整型，可以是浮点数、字符串、矩阵等
4. 不要给出任何其他回复，即使代码有不规范
请以严格的 JSON 格式返回每一个测试用例，格式如下：
[
    {{
        "function": "函数名",
        "inputs": [输入参数列表],
        "expected": "期望的输出结果"
    }},
    ...
]
以下是代码片段：
{source_code}
"""
        response = chat_comp.do(
            model="ERNIE-3.5-8K", messages=[{"role": "user", "content": prompt}]
        )
        return response

    except Exception as e:
        print(f"调用 OpenAI 接口时发生错误: {e}")
        return None


def test_local_file_directly(file_path):
    """
    直接读取本地文件并进行代码解析和分析。
    """
    print(f"正在分析文件: {file_path}")
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在。")
        return
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        # 解析代码
        function_definitions = parse_code(file_content)

        # 调用 OpenAI 接口生成测试用例
        openai_analysis_result = analyze_code_with_openai(file_content)

        if openai_analysis_result is None:
            print("OpenAI 分析失败，未返回结果。")
            return

        # 提取测试用例
        test_cases = []
        try:
            # 从返回的字典中提取 result 字段
            raw_content = openai_analysis_result.get("result", "").strip()
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]  # 去掉开头的 ```json
            if raw_content.endswith("```"):
                raw_content = raw_content[:-3]  # 去掉结尾的 ```
            # 清洗json
            # 替换 np.array 为 Python 列表
            # 先替换 np.array(...)
            raw_content = re.sub(
                r"np\.array\((.*?)\)", r"\1", raw_content, flags=re.DOTALL
            )
            # 再替换 np.matrix(...)
            raw_content = re.sub(
                r"np\.matrix\((.*?)\)", r"\1", raw_content, flags=re.DOTALL
            )
            # 使用 json.loads 解析 JSON 格式
            test_cases = json.loads(raw_content)
        except Exception as e:
            print(f"解析测试用例时发生错误: {e}")
            print("OpenAI 返回的原始内容:", openai_analysis_result)
            return

        # 打印测试用例
        print("测试用例生成结果:")
        for case in test_cases:
            print(f"函数: {case['function']}")
            print(f"输入: {case['inputs']}")
            print(f"期望输出: {case['expected']}")
            print("-" * 40)

    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    file_path = "samples/test.py"
    test_local_file_directly(file_path)
