"""
 生成多个列表元素的所有可能组合，并在组合数过多时随机采样一部分组合。
 根据输入的字典 lists，计算所有列表元素的笛卡尔积（即所有可能的组合），
 并根据总组合数的大小决定是生成全部组合还是只随机生成一部分。
"""
import itertools
import random

# 设置上限
MAX_COMBINATIONS = 10000
# 想采样的个数（如果超出上限）
SAMPLE_SIZE = 100


def generate_combinations(test_cases):
    from itertools import product
    keys = list(test_cases.keys())
    values = [test_cases[k] for k in keys]
    combos = []
    for prod in product(*values):
        combos.append(dict(zip(keys, prod)))
    return combos

    all_lists = list(lists.values())

    # 计算总组合数
    total = 1
    for l in all_lists:
        total *= len(l)

    print(f"总组合数：{total}")

    # 如果总数不大，全部生成
    if total <= MAX_COMBINATIONS:
        combos = list(itertools.product(*all_lists))
        result = []
        for c in combos:
            named = {name: value for name, value in zip(lists.keys(), c)}
            result.append(named)
        return result

    else:
        # 否则随机采样一部分
        sample_size = min(SAMPLE_SIZE, total)
        sample_indices = set(random.sample(range(total), k=sample_size))

        result = []
        for idx, combo in enumerate(itertools.product(*all_lists)):
            if idx in sample_indices:
                named = {name: value for name, value in zip(lists.keys(), combo)}
                result.append(named)
            if len(result) >= sample_size:
                break
        return result

def add_matrix_params(test_cases, matrix_params, m_n_pairs):
    """
    为测试用例添加矩阵参数的随机值。
    :param test_cases: 原始测试用例
    :param matrix_params: 矩阵参数的名称列表
    :param m_n_pairs: 每个矩阵参数对应的 (m, n) 值的列表
    :return: 更新后的测试用例
    """
    for param in matrix_params:
        for m, n in m_n_pairs:
            arr = [[random.randint(-10, 10) for _ in range(n)] for _ in range(m)]
            test_cases[param].append(arr)
    return test_cases
