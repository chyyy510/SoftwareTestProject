import ast

from flask import Flask, jsonify, request
import requests  # 用于发送HTTP请求到DeepSeek

app = Flask(__name__)

from openai import OpenAI

client = OpenAI(
    api_key="bce-v3/ALTAK-d55pFn5tOlc45cpLjNjA1/e9bb1eb5b9f3de6e92ef1f846471f214e210bb35",
    base_url="https://qianfan.baidubce.com/v2",
)


# 代码解析模块
def parse_code(source_code):
    """
    解析代码中的函数定义，返回函数的名称、参数列表、返回值类型、装饰器、文档字符串等信息。
    """
    # 解析源代码为 AST 树
    tree = ast.parse(source_code)
    function_definitions = []

    for node in ast.walk(tree):
        # 只处理函数定义的节点
        if isinstance(node, ast.FunctionDef):
            function_info = {
                "name": node.name,  # 函数名称
                "args": [],  # 参数列表
                "returns": None,  # 返回类型注解
                "decorators": [],  # 装饰器列表
                "docstring": ast.get_docstring(node),  # 文档字符串
                "default_args": [],  # 默认参数列表
                "arg_types": [],  # 参数类型注解
            }

            # 获取参数列表
            for arg in node.args.args:
                arg_info = {"name": arg.arg}

                # 获取每个参数的默认值（如果有的话）
                if arg.arg in [d.arg for d in node.args.defaults]:
                    default_value = node.args.defaults[node.args.args.index(arg)]
                    arg_info["default"] = default_value
                else:
                    arg_info["default"] = None

                # 获取每个参数的类型注解（如果有的话）
                if arg.annotation:
                    arg_info["type"] = arg.annotation
                else:
                    arg_info["type"] = None

                function_info["args"].append(arg_info)

            # 获取返回类型注解
            if node.returns:
                function_info["returns"] = node.returns

            # 获取函数的装饰器（如果有的话）
            if node.decorator_list:
                function_info["decorators"] = [
                    decorator.id if isinstance(decorator, ast.Name) else str(decorator)
                    for decorator in node.decorator_list
                ]

            # 获取函数的默认参数值（如果有的话）
            function_info["default_args"] = [
                (arg.arg, ast.dump(default))
                for arg, default in zip(
                    node.args.args[-len(node.args.defaults) :], node.args.defaults
                )
            ]

            # 将函数信息添加到结果列表
            function_definitions.append(function_info)

    return function_definitions


# 使用 OpenAI 客户端进行代码分析（百度云的接口）
def analyze_code_with_openai(source_code):
    """
    使用 OpenAI 的客户端接口分析代码并返回分析结果。
    """
    # 假设 messages 为包含代码的消息格式
    messages = [{"role": "user", "content": source_code}]

    # 调用 OpenAI 客户端的 completions API
    response = client.chat.completions.create(
        model="ernit-4.0-turbo-128k", messages=messages, temperature=0.7, stream=False
    )
    return response


# 文件上传和处理
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # 读取文件内容并解析代码
    file_content = file.read().decode("utf-8")
    function_definitions = parse_code(file_content)

    # 调用 OpenAI 客户端进行代码分析
    openai_analysis_result = analyze_code_with_openai(file_content)

    # 生成测试用例（假设 OpenAI 返回了相关的测试用例建议）
    test_cases = []
    for func in function_definitions:
        function_name = func["name"]
        args = func["args"]

        # 假设 OpenAI 返回了自动生成的测试用例
        if "choices" in openai_analysis_result:
            test_case = openai_analysis_result["choices"][0]["message"]["content"]
            test_cases.append(
                {
                    "function": function_name,
                    "args": args,
                    "test_case": test_case,
                }
            )

    # 最后将生成的测试用例返回给用户
    return jsonify(
        {
            "test_cases": test_cases,  # 返回生成的测试用例
            "openai_analysis": openai_analysis_result,  # 将 OpenAI 分析结果一并返回
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
