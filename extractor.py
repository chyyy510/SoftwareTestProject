"""
该代码的核心功能是从一个 Python 源代码的 AST 中提取出条件表达式(if)和循环(for,while)的迭代部分，
同时还能够提取函数的参数信息。
提取的条件表达式包含了比较操作符(><=)和涉及的变量或常量。
"""

import ast
import sys
from pathlib import Path

class ConditionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.conditions = []  # 存储所有条件表达式
        self.params = []      # 存储函数参数
        self.returns = []     # 新增：存储 return 表达式
        self.function_name = None

    def visit_FunctionDef(self, node):
        """提取函数名和参数"""
        self.function_name = node.name
        self.params = [arg.arg for arg in node.args.args]
        self.generic_visit(node)

    def visit_If(self, node):
        """处理 if 条件"""
        self.extract_condition(node.test)
        self.generic_visit(node)

    def visit_While(self, node):
        """处理 while 条件"""
        self.extract_condition(node.test)
        self.generic_visit(node)

    def visit_For(self, node):
        if node.iter:
            self.extract_condition(node.iter)
        self.generic_visit(node)

    def visit_Return(self, node):
        """处理 return 语句中的表达式"""
        if node.value:
            # 如果 return 表达式是条件表达式，提取条件
            if isinstance(node.value, ast.Compare):
                self.extract_condition(node.value)
            # 你也可以根据需要递归处理更复杂的表达式
            # 其他情况依然保存表达式字符串
            return_expr = ast.unparse(node.value)
            self.returns.append(return_expr)
        self.generic_visit(node)

    def extract_condition(self, condition):
        """提取条件表达式"""
        try:
            # 处理比较表达式（如 x > 0）
            if isinstance(condition, ast.Compare):
                left_node = condition.left
                op = self.get_operator(condition.ops[0])
                right = ast.unparse(condition.comparators[0])
                if isinstance(left_node, ast.BinOp):
                    left = ast.unparse(left_node)
                    self.conditions.append((left, op, right, "expr"))
                elif isinstance(left_node, ast.Name):
                    left = left_node.id
                    self.conditions.append((left, op, right, "var"))
                else:
                    left = ast.unparse(left_node)
                    self.conditions.append((left, op, right, "other"))
            # 处理 not 表达式：递归解析其操作数并添加 not 标记
            elif isinstance(condition, ast.UnaryOp) and isinstance(condition.op, ast.Not):
                operand = condition.operand
                if isinstance(operand, ast.Compare):
                    left_node = operand.left
                    op = self.get_operator(operand.ops[0])
                    right = ast.unparse(operand.comparators[0])
                    negated_op = self.negate_operator(op)
                    if isinstance(left_node, ast.BinOp):
                        left = ast.unparse(left_node)
                        self.conditions.append((left, negated_op, right, "expr"))
                    elif isinstance(left_node, ast.Name):
                        left = left_node.id
                        self.conditions.append((left, negated_op, right, "var"))
                    else:
                        left = ast.unparse(left_node)
                        self.conditions.append((left, negated_op, right, "other"))
                elif isinstance(operand, ast.Name):
                    self.conditions.append((operand.id, "eq", "0", "var"))
                else:
                    self.extract_condition(operand)
            # 处理 and/or
            elif isinstance(condition, ast.BoolOp):
                for sub_cond in condition.values:
                    self.extract_condition(sub_cond)
            # 处理简单变量（如 if x:）        
            elif isinstance(condition, ast.Name):
                self.conditions.append((condition.id, "not eq", "0", "var"))
        except Exception as e:
            print(f"提取条件时发生异常: {e}. 条件: {condition}")

    def negate_operator(self, op):
        """辅助方法：反转比较操作符"""
        negations = {
            "Lt": "GtE",
            "Gt": "LtE",
            "LtE": "Gt",
            "GtE": "Lt",
            "eq": "not eq",
            "not eq": "eq"
        }
        return negations.get(op, "")

    def get_operator(self, op_node):
        """辅助方法：获取操作符的字符串表示"""
        if isinstance(op_node, ast.Lt):
            return "Lt"
        elif isinstance(op_node, ast.Gt):
            return "Gt"
        elif isinstance(op_node, ast.Eq):
            return "eq"
        elif isinstance(op_node, ast.NotEq):
            return "not eq"
        elif isinstance(op_node, ast.LtE):
            return "LtE"
        elif isinstance(op_node, ast.GtE):
            return "GtE"
        return ""

    def _extract_operand(self, condition):
        """辅助方法：提取操作数的字符串表示"""
        if isinstance(condition, ast.Compare):
            left = ast.unparse(condition.left)
            op = self.get_operator(condition.ops[0])
            right = ast.unparse(condition.comparators[0])
            return (left, op, right)
        return ast.unparse(condition)


def extract_conditions(ast_tree):
    visitor = ConditionVisitor()
    visitor.visit(ast_tree)

    return visitor.conditions  # 现在返回四元组
