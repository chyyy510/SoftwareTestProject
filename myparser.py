from models import Cst, Var

op_map = {"Gt": ">", "Eq": "==", "Lt": "<", "GtE": ">=", "LtE": "<=", "NotEq": "!="}


def parse_node(node_str):
    # 处理常量
    if "Constant" in node_str:
        value_str = node_str.split("value=")[1].split(")")[0]
        # 判断常量的类型是否为字符串
        if '"' in value_str or "'" in value_str:
            return Cst(value_str.strip("'").strip('"'))  # 返回字符串常量
        else:
            return Cst(eval(value_str))  # 返回数字常量
    # 处理变量，改进判断逻辑，支持简单变量格式（如 'x' 或 'y'）
    elif "id='" in node_str:
        id_part = node_str.split("id='")[1]
        id_name = id_part.split("'")[0]
        return Var(id_name)
    else:
        # 对于没有 'id=' 的变量字符串，直接返回变量名
        return Var(node_str.strip())

def parse_constraints(raw_constraints):
    parsed = []
    for left, op, right in raw_constraints:
        left_var = parse_node(left)
        right_var = parse_node(right)
        parsed.append((left_var, op_map.get(op, op), right_var))
    return parsed
