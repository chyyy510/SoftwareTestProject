from collections import defaultdict
import random

from models import Cst, Var


def generate_test_cases(grouped_constraints, params=None, expr_constraints=None):
    test_cases = defaultdict(list)
    # 针对二维数组参数
    matrix_params = [p for p in (params or []) if p in ('A', 'matrix', 'grid')]
    if matrix_params:
        # 默认最小/最大行列
        min_rows = 1
        max_rows = None
        min_cols = 1
        max_cols = None
        special_positions = []

        # 解析 expr_constraints 或 grouped_constraints 里的 'other' 约束
        if expr_constraints:
            for left, op, right, cond_type in expr_constraints:
                # 行数约束
                if str(left) == "len(A)" and op in ("Gt", ">"):
                    min_rows = max(min_rows, right.value + 1)
                elif str(left) == "len(A)" and op in ("Eq", "=="):
                    min_rows = right.value
                    max_rows = right.value
                # 列数约束
                if str(left) == "len(A[1])" and op in ("Gt", ">"):
                    min_cols = max(min_cols, right.value + 1)
                elif str(left) == "len(A[1])" and op in ("Eq", "=="):
                    min_cols = right.value
                    max_cols = right.value
                # 特定元素约束
                if str(left).startswith("A[") and "][" in str(left):
                    idx = str(left)[2:-1].split("][")
                    i, j = int(idx[0]), int(idx[1])
                    special_positions.append((i, j, right.value))

        # 生成满足约束的二维数组
        for param in matrix_params:
            for _ in range(16):
                m = random.randint(min_rows, max_rows) if max_rows else random.randint(min_rows, min_rows + 2)
                n = random.randint(min_cols, max_cols) if max_cols else random.randint(min_cols, min_cols + 2)
                arr = [[random.randint(-10, 10) for _ in range(n)] for _ in range(m)]
                for i, j, val in special_positions:
                    if i < m and j < n:
                        arr[i][j] = val
                test_cases[param].append(arr)
        return test_cases

    # 检查是否有数组参数
    array_params = [p for p in (params or []) if p.endswith('s') or p.startswith('arr') or p == 'nums']
    for param in array_params:
        # 生成一些典型数组样例
        test_cases[param] = [
            [], 
            [0], 
            [1, 2], 
            [-1, 0, 3], 
            [random.randint(-10, 10) for _ in range(3)],
            [random.randint(-100, 100) for _ in range(5)]
        ]
    # 其他变量按原逻辑生成
    for var, conditions in grouped_constraints.items():
        # 跳过 m、n 这种表达式变量（它们的约束右侧是三元组）
        skip = False
        for left, op, right, cond_type in conditions:
            # 如果 right 是三元组，说明这是表达式约束，不直接生成样例
            if isinstance(right, tuple):
                skip = True
                break
        if skip:
            continue
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
        # 只对非list类型去重
        if test_cases[key] and not isinstance(test_cases[key][0], list):
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
    print("生成的 test_cases:", dict(test_cases))
