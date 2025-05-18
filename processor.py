from collections import defaultdict
from itertools import product
import os
import random

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

    ret["final"] = [combo for combo in combinations]
    return ret
