# main.py

import ast
import os

from processor import generate_for_function

file_path = "samples/myfun.py"
if not os.path.exists(file_path):
    print(f"文件 {file_path} 不存在。")


with open(file_path, "r", encoding="utf-8") as file:
    func_code = file.read()


ast_tree = ast.parse(func_code)
for func_ast in ast.walk(ast_tree):
    if isinstance(func_ast, ast.FunctionDef):
        print(f"\n为函数{func_ast.name}生成样例：")
        generate_for_function(func_ast)
