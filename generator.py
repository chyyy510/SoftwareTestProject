from collections import defaultdict
import random

from models import Cst, Var


def generate_test_cases(grouped_constraints):

    # 基于变量的约束生成测试样例
    print("\n基于每个变量的测试样例：")

    test_cases = defaultdict(list)

    for var, conditions in grouped_constraints.items():

        ok = True
        for left, op, right in conditions:
            # 确定表达式
            if isinstance(left, Var):
                if left.value == var:
                    if isinstance(right, Cst):  # 与常数的约束
                        value = right.value
                        if isinstance(value, str):
                            test_cases[var].append(value)
                            test_cases[var].append(value + "1234")
                            test_cases[var].append(value[:-1] if value else value)
                        else:
                            test_cases[var].append(value)
                            test_cases[var].append(value - 1)
                            test_cases[var].append(value + 1)
                    else:  # 与其他变量的约束
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
    for key in test_cases:
        test_cases[key] = list(set(test_cases[key]))

    return test_cases
