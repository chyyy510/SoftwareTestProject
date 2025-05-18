import ast
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from openai import OpenAI
import requests  # 用于发送HTTP请求到DeepSeek

from processor import generate_for_function

app = Flask(__name__)
CORS(app)
client = OpenAI(
    api_key="bce-v3/ALTAK-d55pFn5tOlc45cpLjNjA1/e9bb1eb5b9f3de6e92ef1f846471f214e210bb35",
    base_url="https://qianfan.baidubce.com/v2",
)


@app.route("/upload/file/", methods=["POST"])
def upload_file():
    response = {"ours": {}, "ai": {}}
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # 读取文件内容并解析代码
    """自己的"""
    file_content = file.read().decode("utf-8")
    ast_tree = ast.parse(file_content)
    for func_ast in ast.walk(ast_tree):
        if isinstance(func_ast, ast.FunctionDef):
            print(f"\n为函数 {func_ast.name} 生成样例：")
            ret = generate_for_function(func_ast)
            response["ours"][func_ast.name] = ret

    """AI"""

    # 最后将生成的测试用例返回给用户
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
