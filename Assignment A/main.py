from dataclasses import dataclass
from typing import Union

# Expressions
@dataclass
class IntLiteral:
    value: int

@dataclass
class BoolLiteral:
    value: bool

@dataclass
class Var:
    name: str

@dataclass
class BinOp:
    op: str
    left: 'Expr'
    right: 'Expr'

@dataclass
class UnOp:
    op: str
    expr: 'Expr'

Expr = Union[IntLiteral, BoolLiteral, Var, BinOp, UnOp]

# Commands
@dataclass
class Assign:
    var: str
    expr: Expr

@dataclass
class Seq:
    first: 'Cmd'
    second: 'Cmd'

@dataclass
class If:
    cond: Expr
    then_branch: 'Cmd'
    else_branch: 'Cmd'

@dataclass
class While:
    cond: Expr
    body: 'Cmd'

Cmd = Union[Assign, Seq, If, While]

# Type checking functions
def type_check_expr(expr: Expr, context: dict) -> str:
    if isinstance(expr, IntLiteral):
        return 'int'
    elif isinstance(expr, BoolLiteral):
        return 'bool'
    elif isinstance(expr, Var):
        return context.get(expr.name, 'undefined')
    elif isinstance(expr, UnOp):
        et = type_check_expr(expr.expr, context)
        if expr.op == 'not':
            if et != 'bool':
                raise TypeError("Expected bool in 'not'")
            return 'bool'
        elif expr.op == '-':
            if et != 'int':
                raise TypeError("Expected int in unary '-'")
            return 'int'
    elif isinstance(expr, BinOp):
        lt = type_check_expr(expr.left, context)
        rt = type_check_expr(expr.right, context)
        if expr.op in {'+', '-', '*', '/'}:
            if lt == rt == 'int':
                return 'int'
            raise TypeError("Arithmetic operations require int")
        elif expr.op in {'=', '<='}:
            if lt == rt == 'int':
                return 'bool'
            raise TypeError("Comparison requires int")
        elif expr.op in {'and', 'or'}:
            if lt == rt == 'bool':
                return 'bool'
            raise TypeError("Logical operations require bool")
    raise NotImplementedError(f"Unknown expr: {expr}")

def type_check_cmd(cmd: Cmd, context: dict):
    if isinstance(cmd, Assign):
        etype = type_check_expr(cmd.expr, context)
        context[cmd.var] = etype
    elif isinstance(cmd, Seq):
        type_check_cmd(cmd.first, context)
        type_check_cmd(cmd.second, context)
    elif isinstance(cmd, If):
        ctype = type_check_expr(cmd.cond, context)
        if ctype != 'bool':
            raise TypeError("Condition in If must be bool")
        type_check_cmd(cmd.then_branch, context)
        type_check_cmd(cmd.else_branch, context)
    elif isinstance(cmd, While):
        ctype = type_check_expr(cmd.cond, context)
        if ctype != 'bool':
            raise TypeError("Condition in While must be bool")
        type_check_cmd(cmd.body, context)
    else:
        raise TypeError(f"Unknown command type: {type(cmd)}")

if __name__ == "__main__":
    prog = Seq(
        Assign("x", IntLiteral(10)),
        If(
            BinOp("=", Var("x"), IntLiteral(10)),
            Assign("y", BoolLiteral(True)),
            Assign("y", BoolLiteral(False))
        )
    )
    context = {}
    type_check_cmd(prog, context)
    print("Program is well-typed. Context:", context)
