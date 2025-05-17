from collections import defaultdict

from models import Cst, Expr, Var


def group_constraints(constraints):
    var_constraints = defaultdict(list)

    expr_constraints = []
    for item in constraints:
        if len(item) == 4:
            left, op, right, cond_type = item
        else:
            left, op, right = item
            cond_type = "var"
        if cond_type == "var":
            if isinstance(left, Var):
                var_constraints[left.value].append((left, op, right, cond_type))
            if isinstance(right, Var):
                var_constraints[right.value].append((left, op, right, cond_type))
        elif cond_type == "expr":
            expr_constraints.append((left, op, right, cond_type))
    return var_constraints, expr_constraints
