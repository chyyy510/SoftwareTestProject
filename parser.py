from models import Cst, Var

op_map = {"Gt": ">", "Eq": "==", "Lt": "<", "GtE": ">=", "LtE": "<=", "NotEq": "!="}


def parse_node(node_str):
    if "Constant" in node_str:
        # 处理常量，可以进一步判断是字符串常量还是数字常量
        value_str = node_str.split("value=")[1].split(")")[0]
        # 判断常量的类型是否为字符串
        if '"' in value_str or "'" in value_str:
            return Cst(value_str.strip("'").strip('"'))  # 返回字符串常量
        else:
            return Cst(eval(value_str))  # 返回数字常量
    else:
        # 处理变量名
        id_part = node_str.split("id='")[1]
        id_name = id_part.split("'")[0]
        return Var(id_name)


def parse_constraints(raw_constraints):
    parsed = []
    for left, op, right in raw_constraints:
        left_var = parse_node(left)
        right_var = parse_node(right)
        parsed.append((left_var, op_map.get(op, op), right_var))
    return parsed
