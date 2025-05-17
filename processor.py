from collections import defaultdict
import itertools
import os
from myparser import parse_constraints
import random

from combiner import generate_combinations
from extractor import extract_conditions, ConditionVisitor  # filepath: c:\Users\25876\SoftwareTestProject\processor.py
from generator import generate_test_cases
from grouper import group_constraints
from models import Cst, Var


def generate_for_function(func_ast):

    # 分析条件
    raw_constraints = extract_conditions(func_ast)
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
    visitor = ConditionVisitor()
    visitor.visit(func_ast)
    params = visitor.params  # 获取参数名列表
    test_cases = generate_test_cases(grouped_constraints, params)
    print("\n满足条件的测试样例：")
    for var, case in test_cases.items():
        print(var, " ", case)

    # 正式生成组合
    combinations = generate_combinations(test_cases)

    # 打印
    for combo in combinations:
        print(combo)
