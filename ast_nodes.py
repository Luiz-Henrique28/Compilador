# /home/runner/workspace/ast_nodes.py


class AST:
    pass


class BinOp(AST):

    def __init__(self, esq, op, dir):
        self.esq = esq
        self.token = self.op = op
        self.dir = dir


class Num(AST):

    def __init__(self, token):
        self.token = token
        self.valor = token.valor


class StringNode(AST):

    def __init__(self, token):
        self.token = token
        self.valor = token.valor


class UnaryOp(AST):

    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class TipoNode(AST):
    """Representa o tipo de uma variável (ex: INTEIRO, REAL)"""

    def __init__(self, token):
        self.token = token
        self.valor = token.valor


class VarDecl(AST):

    def __init__(self, var_node, tipo_node):
        self.var_node = var_node
        self.tipo_node = tipo_node


class Assign(AST):

    def __init__(self, esq, op, dir):
        self.esq = esq
        self.token = self.op = op
        self.dir = dir


class Var(AST):
    """O nó Var é usado quando a variável é referenciada/usada em uma expressão."""

    def __init__(self, token):
        self.token = token
        self.valor = token.valor


class BlockNode(AST):

    def __init__(self):
        self.declarations = []
        self.statements = []


class IfNode(AST):

    def __init__(self, condicao, bloco_se, bloco_senao):
        self.condicao = condicao
        self.bloco_se = bloco_se
        self.bloco_senao = bloco_senao  # Pode ser None


class WhileNode(AST):

    def __init__(self, condicao, bloco):
        self.condicao = condicao
        self.bloco = bloco


# --- Nova Classe Adicionada ---
class EscritaNode(AST):
    """Representa a instrução ESCREVA."""

    def __init__(self, expr):
        self.expr = expr


# -----------------------------


class NoOp(AST):
    """Representa uma instrução vazia."""
    pass


class ProgramaNode(AST):

    def __init__(self, nome, bloco):
        self.nome = nome
        self.bloco = bloco
