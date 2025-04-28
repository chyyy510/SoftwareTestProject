def process_numbers(nums):
    result = []
    i = 0
    while i < len(nums):
        num = nums[i]
        if num < 0:
            # 忽略负数
            i += 1
            continue
        elif num == 0:
            # 遇到0提前结束
            break
        else:
            for j in range(num):
                if j % 2 == 0:
                    result.append(j)
        i += 1
    return result
