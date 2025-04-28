"""
该代码的核心功能是从一个 Python 源代码的 AST 中提取出条件表达式(if)和循环(for,while)的迭代部分，
同时还能够提取函数的参数信息。
提取的条件表达式包含了比较操作符(><=)和涉及的变量或常量。
"""

import ast


class ConditionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.conditions = []
        self.params = []

    def visit_If(self, node):
        self.extract_condition(node.test)
        self.generic_visit(node)

    def visit_While(self, node):
        self.extract_condition(node.test)
        self.generic_visit(node)

    def visit_For(self, node):
        if node.iter:
            self.extract_condition(node.iter)
        self.generic_visit(node)

    def extract_condition(self, condition):
        if isinstance(condition, ast.Compare):
            left = ast.dump(condition.left)
            op = type(condition.ops[0]).__name__
            right = ast.dump(condition.comparators[0])
            self.conditions.append((left, op, right))
        elif isinstance(condition, ast.Name):
            self.conditions.append((condition.id, "is used", ""))

    def visit_FunctionDef(self, node):
        self.params = [arg.arg for arg in node.args.args]
        self.generic_visit(node)


def extract_conditions(ast_tree):
    # tree = ast.parse(func_code)
    visitor = ConditionVisitor()
    visitor.visit(ast_tree)
    return visitor.conditions
