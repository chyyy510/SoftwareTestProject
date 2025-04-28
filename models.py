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
