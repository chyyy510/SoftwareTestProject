# main.py

import os
from parser import parse_constraints

from combiner import generate_combinations
from extractor import extract_conditions
from generator import generate_test_cases
from grouper import group_constraints
from models import Cst, Var

file_path = "samples/process_numbers.py"
if not os.path.exists(file_path):
    print(f"文件 {file_path} 不存在。")


with open(file_path, "r", encoding="utf-8") as file:
    func_code = file.read()

"""func_code = 
def example_function(acc, b):
    if acc > b:
        print("acc is greater")
    elif acc == b:
        print("acc equals b")
    while b > 0:
        b -= 1
    for i in range(acc):
        print(i)
    if acc>"":
        print("hhh")
"""

# 分析条件
raw_constraints = extract_conditions(func_code)
print("原始条件：")
for c in raw_constraints:
    print(c)

# 解析条件
parsed_constraints = parse_constraints(raw_constraints)
print("\n解析后条件：")
for c in parsed_constraints:
    print(c)

# 按变量分组
print("\n分组后约束：")
grouped_constraints = group_constraints(parsed_constraints)
for var, conditions in grouped_constraints.items():
    print(f"Variable: {var}")
    for left, op, right in conditions:
        print(f"  {left} {op} {right}")

from collections import defaultdict

# 生成测试样例
import itertools
import random

test_cases = generate_test_cases(grouped_constraints)
print("\n满足条件的测试样例：")
for var, case in test_cases.items():
    print(var, " ", case)

# 正式生成组合
combinations = generate_combinations(test_cases)

# 打印
for combo in combinations:
    print(combo)
