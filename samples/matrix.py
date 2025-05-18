def is_square(matrix):
    # 判断二维数组是否为方阵（行数和列数相等）
    if not matrix:  # 空数组的情况
        return False
    rows = len(matrix)
    cols = len(matrix[0])
    # 检查每一行的列数是否相同，以及行数是否等于列数
    for row in matrix:
        if len(row) != cols:
            return False
    return rows == cols

# 示例
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

if is_square(matrix):
    print("行数和列数相等，数组是方阵。")
else:
    print("行数和列数不相等，数组不是方阵。")