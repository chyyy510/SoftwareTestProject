from collections import defaultdict
import random

from models import Cst, Var


def generate_test_cases(grouped_constraints, params=None):
    print("\n基于每个变量的测试样例：")
    test_cases = defaultdict(list)
    for var, conditions in grouped_constraints.items():
        for left, op, right, cond_type in conditions:
            if isinstance(left, Var):
                if left.value == var:
                    if isinstance(right, Cst):
                        value = right.value
                        if isinstance(value, str):
                            test_cases[var].append(value)
                            test_cases[var].append(value + "1234")
                            test_cases[var].append(value[:-1] if value else value)
                        else:
                            test_cases[var].append(value)
                            test_cases[var].append(value - 1)
                            test_cases[var].append(value + 1)
                    else:
                        value = random.randint(0, 100)
                        test_cases[var].append(value)
                        test_cases[right.value].append(value)
                        test_cases[right.value].append(value - 1)
                        test_cases[right.value].append(value + 1)
            else:
                if isinstance(right, Var) and right.value == var:
                    value = left.value
                    test_cases[var].append(value)
                    test_cases[var].append(value - 1)
                    test_cases[var].append(value + 1)
    if params:
        for param in params:
            if param not in test_cases:
                test_cases[param] = random.sample(range(-100, 100), 4)
    for key in test_cases:
        test_cases[key] = list(set(test_cases[key]))
    return test_cases

    # 在 processor.py 的输出部分
    print("\n最终满足所有约束的测试样例：")
    if not filtered:
        print("没有任何变量组合能同时满足所有约束。")
    else:
        for f in filtered:
            print(f)
    print(f"总组合数：{len(filtered)}")
