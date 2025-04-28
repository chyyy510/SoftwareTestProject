def merge_sort(nums):
    if len(nums) < 2:
        return nums
    else:
        list_length = len(nums) // 2
        first_half = merge_sort(nums[:list_length])
        second_half = merge_sort(nums[list_length:])
        return merge(first_half, second_half)


def merge(first, second):
    sorted_result = []
    a = 0
    b = 0 
    
    while a < len(first) and b < len(second):
        if first[a] <= second[b]:
            sorted_result.append(first[a])
            a += 1
        else:
            sorted_result.append(second[b])
            b += 1

    sorted_result.extend(first[a:])
    sorted_result.extend(second[b:])
    return sorted_result
