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
    解析代码中的函数定义，返回函数的名称、参数列表和返回值类型。
    """
    tree = ast.parse(source_code)
    function_definitions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_definitions.append(
                {
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "returns": node.returns,
                }
            )
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
