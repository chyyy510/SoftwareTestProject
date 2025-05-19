from collections import defaultdict
from itertools import product
import random
import json 
import argparse
import ast
import os
import coverage
from combiner import generate_combinations
from extractor import (  # filepath: c:\Users\25876\SoftwareTestProject\processor.py
    ConditionVisitor,
    extract_conditions,
)
from generator import generate_test_cases
from grouper import group_constraints
from myparser import parse_constraints


def generate_for_function(func_ast):

    ret = {
        "initial": [],
        "parse": [],
        "group": defaultdict(list),
        "condition": {},
        "final": {},
        "total": 0,
    }
    raw_constraints = extract_conditions(func_ast)

    print("原始条件：")
    for c in raw_constraints:
        ret["initial"].append(str(c))
        print(c)
    parsed_constraints = parse_constraints(raw_constraints)

    print("\n解析后条件：")
    for c in parsed_constraints:
        ret["parse"].append(str(c))
        print(c)

    print("\n分组后约束：")
    grouped_constraints, expr_constraints = group_constraints(parsed_constraints)
    for var, conditions in grouped_constraints.items():
        ret["group"][var] = [str(cond) for cond in conditions]
        print(var, conditions)
    visitor = ConditionVisitor()
    visitor.visit(func_ast)
    params = visitor.params
    print("params:", params)
    test_cases = generate_test_cases(grouped_constraints, params)
   

    print("\n满足条件的测试样例：")
    for var in params:
        if var in test_cases:
            ret["condition"][var] = sorted(test_cases[var])
            print(f"{var} {sorted(test_cases[var])}")
    combinations = generate_combinations(test_cases)

    print(f"总组合数：{len(combinations)}")
    ret["total"] = len(combinations)
    for combo in combinations:
        print(combo)
    # 将 JSON 写入到文件
    with open("test_combo.json", "w") as f:
        json.dump(combo, f, indent=4)

    ret["final"] = [combo for combo in combinations]
    # 计算覆盖率
    analyze_coverage(func_ast,test_cases)
    return ret

def analyze_coverage(func_ast, test_cases):
    """
    分析生成的测试用例对程序语句的覆盖率。
    """
    # 获取源代码文件路径（假设文件路径可以从AST中获得）
    file_path = "samples/test.py"  # 替换为实际文件路径
    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在，无法进行覆盖率分析。")
        return

    # 启动coverage.py
    cov = coverage.Coverage(source=[file_path])  # 指定要覆盖的源文件
    cov.start()  # 开始覆盖率记录

    # 执行测试用例
    # 假设你有一个执行测试用例的函数（需要根据生成的测试用例进行修改）
    for test_case in test_cases.values():
        execute_test_case(test_case)  # 需要你定义如何执行每个测试用例

    cov.stop()  # 停止记录
    cov.save()  # 保存覆盖率数据

    # 输出覆盖率报告
    cov.report()  # 输出到控制台
    cov.html_report(directory="coverage_report")  # 输出HTML格式报告，存放在 coverage_report 目录下
    print("覆盖率分析完成。请查看控制台和 coverage_report 目录中的报告。")

def execute_test_case(test_case):
    """
    执行给定的测试用例。
    根据你的项目需要进行修改。
    """
    # 此函数需要实现如何根据生成的测试用例运行代码。
    # 比如调用函数并传入参数等，这部分根据你实际的生成逻辑来写。
    pass



def main():
    # 设置命令行参数解析器
    parser = argparse.ArgumentParser(description="解析并生成函数样例")
    parser.add_argument("file_path", type=str, help="Python 文件的路径，包含函数定义")
    args = parser.parse_args()

    file_path = "samples/test.py"

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
                ret = generate_for_function(func_ast)
                # print(ret)
    except Exception as e:
        print(f"解析 AST 或生成样例时发生异常: {e}")




if __name__ == "__main__":
    main()