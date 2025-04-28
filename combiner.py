import itertools
import random

# 设置上限
MAX_COMBINATIONS = 10000
# 想采样的个数（如果超出上限）
SAMPLE_SIZE = 100


def generate_combinations(lists):
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
