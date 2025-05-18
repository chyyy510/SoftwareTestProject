import ast
import json
import re

from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
from qianfan import ChatCompletion
import requests  # 用于发送HTTP请求到DeepSeek

from processor import generate_for_function

app = Flask(__name__)
CORS(app)

client = OpenAI(
    api_key="bce-v3/ALTAK-d55pFn5tOlc45cpLjNjA1/e9bb1eb5b9f3de6e92ef1f846471f214e210bb35",
    base_url="https://qianfan.baidubce.com/v2",
)


def parse_ai_response(raw_answer: str):
    try:
        # 把 Python 风格字符串（带有 None）变成 Python 对象
        data = ast.literal_eval(raw_answer)
    except Exception as e:
        print("🛑 解析失败：", e)
        return {"error": "Invalid format"}

    # 然后再转成 JSON 格式，None → null
    return data


def analyze(code):
    """ours"""
    response = {"ours": {}, "ai": {}, "ai_error": False, "ours_error": False}

    ast_tree = ast.parse(code)
    for func_ast in ast.walk(ast_tree):
        if isinstance(func_ast, ast.FunctionDef):
            print(f"\n为函数 {func_ast.name} 生成样例：")
            ret = generate_for_function(func_ast)
            response["ours"][func_ast.name] = ret
            # print(f"====\n{response}\n====")

    # return response
    """ai"""
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
{code}
"""
        answer = chat_comp.do(
            model="ERNIE-3.5-8K", messages=[{"role": "user", "content": prompt}]
        )
    except Exception as e:
        print(f"调用 OpenAI 接口时发生错误: {e}")
        return None

    if answer is None:
        print("OpenAI 分析失败，未返回结果。")
        return None

    answer = answer.get("result", "").strip()
    pattern = r"```json\s*(.*?)\s*```"
    match = re.search(pattern, answer, re.DOTALL)
    if not match:
        return None
    json_str = match.group(1)

    ret = parse_ai_response(json_str)
    if "error" in ret:
        response["ai"] = json_str
        response["ai_error"] = True
    else:
        response["ai"] = ret

    return response


@app.route("/upload/file/", methods=["POST"])
def upload_file():

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    file_content = file.read().decode("utf-8")

    response = analyze(file_content)
    if response is None:
        return jsonify({"error": "分析函数时出错"}), 400
    print(response)
    # 最后将生成的测试用例返回给用户
    return jsonify(response)


@app.route("/upload/code/", methods=["POST"])
def upload_code():
    try:
        # 假设前端发送的是 JSON 格式的代码数据
        data = request.get_json()
        print(data)
        code = data.get("code") if data else None

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # 返回结构
    response = analyze(code)
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
