def bubble_sort(nums):
    swap = True
    end = len(nums)
    while swap == True:
        swap = False
        for i in range(1, end):
            if nums[i-1] > nums[i]:
                temp = nums[i-1]
                nums[i-1] = nums[i]
                nums[i] = temp
                swap = True
        end -= 1
    return nums
