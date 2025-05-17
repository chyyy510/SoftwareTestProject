import ast
import os
import argparse
from processor import generate_for_function

# 设置命令行参数解析器
parser = argparse.ArgumentParser(description="解析并生成函数样例")
parser.add_argument('file_path', type=str, help="Python 文件的路径，包含函数定义")
args = parser.parse_args()

file_path = args.file_path

# 检查文件是否存在
if not os.path.exists(file_path):
    print(f"文件 {file_path} 不存在。")
    exit(1)

# 读取文件内容
try:
    with open(file_path, "r", encoding="utf-8") as file:
        func_code = file.read()
except Exception as e:
    print(f"读取文件时发生异常: {e}")
    exit(1)

# 解析 AST 树并生成样例
try:
    ast_tree = ast.parse(func_code)
    for func_ast in ast.walk(ast_tree):
        if isinstance(func_ast, ast.FunctionDef):
            print(f"\n为函数 {func_ast.name} 生成样例：")
            generate_for_function(func_ast)
except Exception as e:
    print(f"解析 AST 或生成样例时发生异常: {e}")