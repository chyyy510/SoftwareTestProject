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
        "final": {
            "valid_combinations": [],
            "all_combinations": [],
        },
        "info": {
            "total_valid": 0,
            "total_all": 0,
        },
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
    test_cases = generate_test_cases(grouped_constraints, params)
    print("\n满足条件的测试样例：")
    for var in params:
        if var in test_cases:
            ret["condition"][var] = sorted(test_cases[var])
            print(f"{var} {sorted(test_cases[var])}")
    combinations = generate_combinations(test_cases)
    # 用expr_constraints过滤组合
    filtered = []
    for combo in combinations:
        ok = True
        for left, op, right, cond_type in expr_constraints:
            # 这里需要动态计算表达式的值
            try:
                # left 形如 "x + y"，right 形如 Cst(0)
                env = dict(combo)
                # 支持变量名直接用
                expr_val = eval(left, {}, env)
                if op == ">":
                    ok = ok and (expr_val > right.value)
                elif op == ">=":
                    ok = ok and (expr_val >= right.value)
                elif op == "<":
                    ok = ok and (expr_val < right.value)
                elif op == "<=":
                    ok = ok and (expr_val <= right.value)
                elif op == "==":
                    ok = ok and (expr_val == right.value)
                elif op == "!=" or op == "not eq":
                    ok = ok and (expr_val != right.value)
            except Exception as e:
                ok = False
        if ok:
            filtered.append(combo)
    print("\n最终满足所有约束的测试样例：")
    for f in filtered:
        ret["final"]["valid_combinations"] = filtered
        ret["info"]["total_valid"] = len(filtered)
        print(f)
    if filtered:
        ret["final"]["all_combinations"] = filtered
        ret["info"]["total_all"] = len(filtered)
        print(f"总组合数：{len(filtered)}")
        for combo in filtered:
            print(combo)
    else:
        # 输出所有变量测试样例的笛卡尔积
        keys = [var for var in params if var in test_cases]
        values_product = product(*(test_cases[k] for k in keys))
        all_combos = [dict(zip(keys, vals)) for vals in values_product]
        print(f"总组合数：{len(all_combos)}")
        ret["final"]["all_combinations"] = all_combos
        ret["info"]["total_all"] = len(all_combos)
        for combo in all_combos:
            print(combo)

    return ret
