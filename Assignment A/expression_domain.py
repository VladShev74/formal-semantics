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
