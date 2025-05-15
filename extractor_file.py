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
        """新增：处理 return 语句中的表达式"""
        if node.value:  # 确保 return 后有表达式
            # 将 return 表达式转换为可读字符串
            return_expr = ast.unparse(node.value)
            self.returns.append(return_expr)
            #if isinstance(node, ast.Compare):
            #self.extract_condition(node.value)
        self.generic_visit(node)

    def extract_condition(self, condition):
        """提取条件表达式 固定为三元组<left, op, right>"""
        # 处理比较表达式（如 x > 0）
        if isinstance(condition, ast.Compare):  
            left = ast.unparse(condition.left)
            op = type(condition.ops[0]).__name__
            right = ast.unparse(condition.comparators[0])
            self.conditions.append((left, op, right))
        # 处理 not 表达式：递归解析其操作数并添加 not 标记
        elif isinstance(condition, ast.UnaryOp) and isinstance(condition.op, ast.Not):
            operand = self._extract_operand(condition.operand)
            # self.conditions.append(f"not ({operand})")
            self.conditions.append((operand[0], "not", operand[2]))

        # 处理 and/or
        elif isinstance(condition, ast.BoolOp):  
            for sub_cond in condition.values:
                self.extract_condition(sub_cond)
        # 处理简单变量（如 if x:）        
        elif isinstance(condition, ast.Name):    
            self.conditions.append((condition.id, "is used", ""))

    def _extract_operand(self, condition):
        """辅助方法：提取操作数的字符串表示"""
        if isinstance(condition, ast.Compare):
            left = ast.unparse(condition.left)
            op = type(condition.ops[0]).__name__
            right = ast.unparse(condition.comparators[0])
            return (left, op, right)
        return (ast.unparse(condition), "", "")

def extract_conditions(ast_tree):
    visitor = ConditionVisitor()
    visitor.visit(ast_tree)
    return {
        "functions": [{
            "function_name": visitor.function_name,
            "params": visitor.params,
            "conditions": visitor.conditions,
            "return_exprs": visitor.returns
        }]
    }



def analyze_file(file_path):
    """分析 Python 文件"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        tree = ast.parse(code)
        
        # 分析整个文件
        visitor = ConditionVisitor()
        visitor.visit(tree)

        # 汇总所有函数的信息
        results = []
        for func in visitor.params:
            results.append({
                "function_name": visitor.function_name,
                "params": visitor.params,
                "conditions": visitor.conditions,
                "return_exprs": visitor.returns
            })
        
        return results
    
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python ast_analyzer.py <python_file>")
        print("Example: python ast_analyzer.py example.py")
        return
    
    file_path = sys.argv[1]
    
    result = analyze_file(file_path)
    
    if isinstance(result, str):
        print(result)  # 打印错误信息
    else:
            print("\n=== 分析结果 ===")
            for func in result:
                print(f"\n函数名称: {func['function_name']}")
                print(f"参数列表: {', '.join(func['params'])}")
                print("\n条件表达式:")
                for left, op, right in func['conditions']:
                    print(f" {left} {op} {right}")

                print("\nReturn 表达式:")
                for expr in func['return_exprs']:
                    print(f" {expr}")

if __name__ == "__main__":
    main()