import ast
import os

from processor import generate_for_function

file_path = "samples/myfun.py"
if not os.path.exists(file_path):
    print(f"文件 {file_path} 不存在。")
    exit(1)

try:
    with open(file_path, "r", encoding="utf-8") as file:
        func_code = file.read()
except Exception as e:
    print(f"读取文件时发生异常: {e}")
    exit(1)

try:
    ast_tree = ast.parse(func_code)
    for func_ast in ast.walk(ast_tree):
        if isinstance(func_ast, ast.FunctionDef):
            print(f"\n为函数 {func_ast.name} 生成样例：")
            generate_for_function(func_ast)
except Exception as e:
    print(f"解析 AST 或生成样例时发生异常: {e}")