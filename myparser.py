from models import Cst, Var

op_map = {"Gt": ">", "Eq": "==", "Lt": "<", "GtE": ">=", "LtE": "<=", "Not Eq": "!="}


def parse_node(node_str):
    try:
        # 判断是否为数字常量
        if node_str.isdigit() or (node_str.startswith("-") and node_str[1:].isdigit()):
            return Cst(int(node_str))
        # 判断是否为浮点数常量
        try:
            float_val = float(node_str)
            return Cst(float_val)
        except ValueError:
            pass
        # 判断是否为字符串常量
        if node_str.startswith("'") or node_str.startswith('"'):
            return Cst(node_str.strip("'").strip('"'))
        # 检查是否为形如 m - 1 的表达式
        if " - " in node_str:
            parts = node_str.split(" - ")
            if len(parts) == 2 and parts[1].strip() == "1":
                return ("var_minus_1", parts[0].strip())
        # 判断是否为 AST 格式的常量
        if "Constant" in node_str:
            value_str = node_str.split("value=")[1].split(")")[0]
            if '"' in value_str or "'" in value_str:
                return Cst(value_str.strip("'").strip('"'))
            else:
                return Cst(eval(value_str))
        # 判断是否为变量
        elif "id='" in node_str:
            id_part = node_str.split("id='")[1]
            id_name = id_part.split("'")[0]
            return Var(id_name)
        else:
            # 默认返回变量
            return Var(node_str.strip())
    except Exception as e:
        print(f"解析节点时发生异常: {e}. 输入: {node_str}")
        return None


def parse_constraints(raw_constraints):
    parsed = []
    for item in raw_constraints:
        left, op, right, cond_type = item
        left_var = parse_node(left)
        right_var = parse_node(right)
        # 处理右侧是 m-1 的情况
        if isinstance(right_var, tuple) and right_var[0] == "var_minus_1":
            var_name = right_var[1]
            if op in ("==", "Eq"):
                # i == m-1  => m == i+1
                if isinstance(left_var, Cst):
                    parsed.append((Var(var_name), "==", Cst(left_var.value + 1), cond_type))
                elif isinstance(left_var, Var):
                    parsed.append((Var(var_name), "==", (left_var, "+", 1), cond_type))
            # 你可以根据需要扩展其它操作符
        else:
            parsed.append((left_var, op, right_var, cond_type))
    return parsed
