# parser.py
from lexer import TokenType

# --- Definições dos Nós da AST (Árvore de Sintaxe Abstrata) ---
# Adicionei estas classes porque o parser precisa delas para construir a árvore.

class ASTNode:
    pass

class ProgramNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"ProgramNode({self.statements})"

class VarDeclNode(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    def __repr__(self):
        return f"VarDeclNode(ID:{self.identifier}, Expr:{self.expression})"

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self):
        return f"({self.left} {self.op.value} {self.right})"

class NumberNode(ASTNode):
    def __init__(self, value):
        # Converte o valor para int aqui para garantir
        self.value = int(value)
    def __repr__(self):
        return f"Number({self.value})"

class VarAccessNode(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value
    def __repr__(self):
        return f"VarAccess({self.value})"

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"String('{self.value}')"

# --- Parser ---

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        return self.current_token

    def consume(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(f"Erro de sintaxe: Esperado {token_type}, mas encontrado {self.current_token.type}")

    def parse(self):
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
            # Adicionado para consumir ponto e vírgula opcionais entre as declarações
            if self.current_token.type == TokenType.SEMICOLON:
                self.consume(TokenType.SEMICOLON)
        return ProgramNode(statements)

    def statement(self):
        if self.current_token.type == TokenType.VAR_KEYWORD:
            return self.variable_declaration()
        else:
            return self.expression()

    def variable_declaration(self):
        self.consume(TokenType.VAR_KEYWORD) # Consome 'var'
        identifier_token = self.current_token
        self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.ASSIGN) # Consome '='
        expr = self.expression()
        return VarDeclNode(identifier_token.value, expr)

    def expression(self):
        return self.term()

    def term(self):
        node = self.factor()
        while self.current_token.type == TokenType.OPERATOR and self.current_token.value in ('+', '-'):
            op_token = self.current_token
            self.consume(TokenType.OPERATOR)
            right = self.factor()
            node = BinOp(left=node, op=op_token, right=right)
        return node

    def factor(self):
        node = self.power()
        while self.current_token.type == TokenType.OPERATOR and self.current_token.value in ('*', '/'):
            op_token = self.current_token
            self.consume(TokenType.OPERATOR)
            right = self.power()
            node = BinOp(left=node, op=op_token, right=right)
        return node

    def power(self):
        token = self.current_token

        # >>>>> ESTA É A CORREÇÃO PRINCIPAL <<<<<
        if token.type == TokenType.INTEGER_LITERAL:
            self.consume(TokenType.INTEGER_LITERAL)
            # Em vez de retornar token.value (uma string ou int), criamos um nó.
            return NumberNode(token.value)

        elif token.type == TokenType.STRING_LITERAL:
            self.consume(TokenType.STRING_LITERAL)
            return StringNode(token.value)

        elif token.type == TokenType.IDENTIFIER:
            return self.variable_access()

        elif token.type == TokenType.LPAREN:
            self.consume(TokenType.LPAREN)
            node = self.expression()
            self.consume(TokenType.RPAREN)
            return node

        raise Exception(f"Fator inválido: {token}")

    def variable_access(self):
        token = self.current_token
        self.consume(TokenType.IDENTIFIER)
        return VarAccessNode(token)