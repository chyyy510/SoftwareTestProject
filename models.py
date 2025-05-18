class Expr:
    def __init__(self, value, expr_type):
        self.value = value  # 存储值
        self.expr_type = expr_type  # 'variable' 或 'constant'

    def __repr__(self):
        return f"{self.expr_type.capitalize()}({self.value})"

    def __str__(self):
        return str(self.value)


class Var(Expr):
    def __init__(self, name):
        super().__init__(name, "var")  # 类型为 'variable'


class Cst(Expr):
    def __init__(self, value):
        super().__init__(value, "cst")  # 类型为 'constant'


def parse_node(node_str):
    # ...原有代码...
    # 检查是否为形如 m - 1 的表达式
    if " - " in node_str:
        parts = node_str.split(" - ")
        if len(parts) == 2 and parts[1].strip() == "1":
            return ("var_minus_1", parts[0].strip())
    # ...原有代码...
