from collections import defaultdict

from models import Cst, Expr, Var


def group_constraints(constraints):
    var_constraints = defaultdict(list)
    for left, op, right in constraints:
        if not isinstance(left, Expr):
            raise TypeError(
                f"Expected a self-defined Expression for left, got {type(left)}"
            )
        if not isinstance(right, Expr):
            raise TypeError(
                f"Expected a self-defined Expression for right, got {type(right)}"
            )
        # 判断左边和右边是不是变量
        if isinstance(left, Var):
            var_constraints[left.value].append((left, op, right))

        if isinstance(right, Var):
            var_constraints[right.value].append((left, op, right))
            
    return var_constraints
