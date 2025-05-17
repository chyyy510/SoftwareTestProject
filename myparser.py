from models import Cst, Var

op_map = {"Gt": ">", "Eq": "==", "Lt": "<", "GtE": ">=", "LtE": "<=", "NotEq": "!="}


def parse_node(node_str):
    # 判断是否为数字常量
    if node_str.isdigit() or (node_str.startswith('-') and node_str[1:].isdigit()):
        return Cst(int(node_str))  # 返回整数常量
    # 判断是否为浮点数常量
    try:
        float_val = float(node_str)
        return Cst(float_val)  # 返回浮点数常量
    except ValueError:
        pass
    # 判断是否为字符串常量
    if node_str.startswith("'") or node_str.startswith('"'):
        return Cst(node_str.strip("'").strip('"'))  # 返回字符串常量
    # 判断是否为 AST 格式的常量
    if "Constant" in node_str:
        value_str = node_str.split("value=")[1].split(")")[0]
        if '"' in value_str or "'" in value_str:
            return Cst(value_str.strip("'").strip('"'))  # 返回字符串常量
        else:
            return Cst(eval(value_str))  # 返回数字常量
    # 判断是否为变量
    elif "id='" in node_str:
        id_part = node_str.split("id='")[1]
        id_name = id_part.split("'")[0]
        return Var(id_name)
    else:
        # 默认返回变量
        return Var(node_str.strip())

def parse_constraints(raw_constraints):
    parsed = []
    for left, op, right in raw_constraints:
        left_var = parse_node(left)
        right_var = parse_node(right)
        parsed.append((left_var, op_map.get(op, op), right_var))
    return parsed
