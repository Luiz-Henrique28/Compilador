# ast_nodes.py

class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'{self.token.value}'

class StringNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f'"{self.token.value}"'

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'({self.left} {self.op.value} {self.right})'

class VarDecl:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f'VarDecl(name={self.name}, value={self.value})'

class VarAccess:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'VarAccess(name={self.name})'

class IfNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f'If(condition={self.condition}, body={self.body})'

class BlockNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f'Block({self.statements})'

# UnaryOp pode ser útil no futuro para operadores como '-' (negativo)
class UnaryOp:
    def __init__(self, op, node):
        self.op = op
        self.node = node

    def __repr__(self):
        return f'({self.op.value}{self.node})'
