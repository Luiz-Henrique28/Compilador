# parser.py
"""
Analisador Sintático Descendente Recursivo
Checkpoint 02 - Compiladores

Implementa um parser baseado na gramática fornecida:
- Análise descendente recursiva
- Tratamento de erros sintáticos
- Suporte para a linguagem definida na gramática
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Any
from lexer import Token, TokenType, Lexer


class ParserError(Exception):
    """Exceção para erros sintáticos"""
    def __init__(self, message: str, token: Token):
        self.message = message
        self.token = token
        super().__init__(f"Erro sintático na linha {token.line}, coluna {token.column}: {message}")


# -----------------------
# Nós da Árvore Sintática Abstrata (AST)
# -----------------------

@dataclass
class ASTNode:
    """Nó base da AST"""
    pass


@dataclass
class Program(ASTNode):
    """programa : 'fn' 'main' '(' ')' bloco"""
    block: Block


@dataclass
class Block(ASTNode):
    """bloco : '{' listaComandos '}'"""
    commands: List[Command]


@dataclass
class Command(ASTNode):
    """Classe base para comandos"""
    pass


@dataclass
class Declaration(Command):
    """declaracao : 'let' mutavel ID ':' tipo ';'"""
    is_mutable: bool
    identifier: str
    type_name: str
    line: int
    column: int


@dataclass
class Assignment(Command):
    """atribuicao : ID '=' expressaoAritmetica ';'"""
    identifier: str
    expression: ArithmeticExpression
    line: int
    column: int


@dataclass
class Read(Command):
    """leitura : 'read' '(' ID ')' ';'"""
    identifier: str
    line: int
    column: int


@dataclass
class Print(Command):
    """escrita : 'print' '!' '(' (ID | CADEIA) ')' ';'"""
    value: Any  # pode ser string (identifier) ou literal (CADEIA)
    is_identifier: bool
    line: int
    column: int


@dataclass
class Conditional(Command):
    """condicional : 'if' expressaoRelacional bloco ['else' bloco]"""
    condition: RelationalExpression
    then_block: Block
    else_block: Optional[Block]
    line: int
    column: int


@dataclass
class While(Command):
    """repeticao : 'while' expressaoRelacional bloco"""
    condition: RelationalExpression
    block: Block
    line: int
    column: int


@dataclass
class ArithmeticExpression(ASTNode):
    """Expressão aritmética"""
    pass


@dataclass
class BinaryOp(ArithmeticExpression):
    """Operação binária: left op right"""
    left: ArithmeticExpression
    operator: str
    right: ArithmeticExpression


@dataclass
class UnaryOp(ArithmeticExpression):
    """Operação unária: op operand"""
    operator: str
    operand: ArithmeticExpression


@dataclass
class Number(ArithmeticExpression):
    """Número (inteiro ou real)"""
    value: Any
    lexeme: str


@dataclass
class Identifier(ArithmeticExpression):
    """Identificador"""
    name: str


@dataclass
class RelationalExpression(ASTNode):
    """Expressão relacional"""
    pass


@dataclass
class RelationalOp(RelationalExpression):
    """expressaoAritmetica OP_REL expressaoAritmetica"""
    left: ArithmeticExpression
    operator: str
    right: ArithmeticExpression


@dataclass
class LogicalOp(RelationalExpression):
    """expressaoRelacional operadorLogico termoRelacional"""
    left: RelationalExpression
    operator: str
    right: RelationalExpression


@dataclass
class LogicalNot(RelationalExpression):
    """Negação lógica: '!' expressaoRelacional"""
    operand: RelationalExpression


# -----------------------
# Parser
# -----------------------

class Parser:
    """
    Analisador Sintático Descendente Recursivo

    Implementa a análise sintática baseada na gramática fornecida.
    Cada não-terminal da gramática corresponde a um método parse_XXX.
    """

    def __init__(self, tokens: List[Token]) -> None:
        # Remove comentários da lista de tokens
        self.tokens = [t for t in tokens if t.type not in (TokenType.LINE_COMMENT, TokenType.BLOCK_COMMENT)]
        self.current = 0
        self.errors: List[ParserError] = []

    # -----------------------
    # Utilitários
    # -----------------------

    def is_at_end(self) -> bool:
        """Verifica se chegou ao fim dos tokens"""
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        """Retorna o token atual sem avançar"""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return self.tokens[-1]  # EOF

    def previous(self) -> Token:
        """Retorna o token anterior"""
        return self.tokens[self.current - 1]

    def advance(self) -> Token:
        """Avança para o próximo token e retorna o anterior"""
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, *token_types: TokenType) -> bool:
        """Verifica se o token atual é de algum dos tipos especificados"""
        if self.is_at_end():
            return False
        return self.peek().type in token_types

    def match(self, *token_types: TokenType) -> bool:
        """Se o token atual for de algum dos tipos, avança e retorna True"""
        if self.check(*token_types):
            self.advance()
            return True
        return False

    def consume(self, token_type: TokenType, message: str) -> Token:
        """Consome um token esperado ou gera erro"""
        if self.check(token_type):
            return self.advance()

        raise ParserError(message, self.peek())

    def synchronize(self):
        """Sincroniza o parser após um erro (panic mode recovery)"""
        self.advance()

        while not self.is_at_end():
            # Sincroniza em ponto e vírgula
            if self.previous().type == TokenType.SEMICOLON:
                return

            # Sincroniza em palavras-chave que iniciam comandos
            if self.check(TokenType.KW_LET, TokenType.KW_IF, TokenType.KW_WHILE,
                          TokenType.KW_READ, TokenType.KW_PRINT, TokenType.KW_RETURN,
                          TokenType.LBRACE, TokenType.RBRACE):
                return

            self.advance()

    # -----------------------
    # Métodos de parsing (um por não-terminal da gramática)
    # -----------------------

    def parse(self) -> Optional[Program]:
        """Ponto de entrada do parser"""
        try:
            return self.parse_program()
        except ParserError as e:
            self.errors.append(e)
            return None

    def parse_program(self) -> Program:
        """
        programa : 'fn' 'main' '(' ')' bloco
        """
        self.consume(TokenType.KW_FN, "Esperado 'fn' no início do programa")
        self.consume(TokenType.KW_MAIN, "Esperado 'main' após 'fn'")
        self.consume(TokenType.LPAREN, "Esperado '(' após 'main'")
        self.consume(TokenType.RPAREN, "Esperado ')' após '('")

        block = self.parse_block()

        # Verifica se há tokens extras após o programa
        if not self.is_at_end():
            raise ParserError("Tokens inesperados após o fim do programa", self.peek())

        return Program(block)

    def parse_block(self) -> Block:
        """
        bloco : '{' listaComandos '}'
        """
        self.consume(TokenType.LBRACE, "Esperado '{'")
        commands = self.parse_command_list()
        self.consume(TokenType.RBRACE, "Esperado '}'")
        return Block(commands)

    def parse_command_list(self) -> List[Command]:
        """
        listaComandos :
            comando listaComandos |
            comando
        """
        commands = []

        # Continua enquanto houver comandos
        while not self.check(TokenType.RBRACE) and not self.is_at_end():
            try:
                cmd = self.parse_command()
                commands.append(cmd)
            except ParserError as e:
                self.errors.append(e)
                self.synchronize()

        return commands

    def parse_command(self) -> Command:
        """
        comando :
            declaracao |
            atribuicao |
            leitura |
            escrita |
            condicional |
            repeticao |
            bloco
        """
        # declaracao: 'let'
        if self.check(TokenType.KW_LET):
            return self.parse_declaration()

        # leitura: 'read'
        if self.check(TokenType.KW_READ):
            return self.parse_read()

        # escrita: 'print'
        if self.check(TokenType.KW_PRINT):
            return self.parse_print()

        # condicional: 'if'
        if self.check(TokenType.KW_IF):
            return self.parse_conditional()

        # repeticao: 'while'
        if self.check(TokenType.KW_WHILE):
            return self.parse_while()

        # bloco: '{'
        if self.check(TokenType.LBRACE):
            return self.parse_block()

        # atribuicao: ID
        if self.check(TokenType.IDENTIFIER):
            return self.parse_assignment()

        raise ParserError("Comando inválido", self.peek())

    def parse_declaration(self) -> Declaration:
        """
        declaracao : 'let' mutavel ID ':' tipo ';'
        mutavel : 'mut' | /* vazio */
        tipo : 'i32' | 'f64'
        """
        let_token = self.consume(TokenType.KW_LET, "Esperado 'let'")

        # mutavel (opcional)
        is_mutable = self.match(TokenType.KW_MUT)

        # ID
        id_token = self.consume(TokenType.IDENTIFIER, "Esperado identificador após 'let'")

        # ':'
        self.consume(TokenType.COLON, "Esperado ':' após identificador")

        # tipo
        if self.match(TokenType.KW_I32):
            type_name = "i32"
        elif self.match(TokenType.KW_F64):
            type_name = "f64"
        else:
            raise ParserError("Esperado tipo 'i32' ou 'f64'", self.peek())

        # ';'
        self.consume(TokenType.SEMICOLON, "Esperado ';' após declaração")

        return Declaration(is_mutable, id_token.lexeme, type_name,
                         let_token.line, let_token.column)

    def parse_assignment(self) -> Assignment:
        """
        atribuicao : ID '=' expressaoAritmetica ';'
        """
        id_token = self.consume(TokenType.IDENTIFIER, "Esperado identificador")
        self.consume(TokenType.ASSIGNMENT, "Esperado '=' após identificador")
        expr = self.parse_arithmetic_expression()
        self.consume(TokenType.SEMICOLON, "Esperado ';' após atribuição")

        return Assignment(id_token.lexeme, expr, id_token.line, id_token.column)

    def parse_read(self) -> Read:
        """
        leitura : 'read' '(' ID ')' ';'
        """
        read_token = self.consume(TokenType.KW_READ, "Esperado 'read'")
        self.consume(TokenType.LPAREN, "Esperado '(' após 'read'")
        id_token = self.consume(TokenType.IDENTIFIER, "Esperado identificador dentro de 'read'")
        self.consume(TokenType.RPAREN, "Esperado ')' após identificador")
        self.consume(TokenType.SEMICOLON, "Esperado ';' após 'read'")

        return Read(id_token.lexeme, read_token.line, read_token.column)

    def parse_print(self) -> Print:
        """
        escrita : 'print' '!' '(' (ID | CADEIA) ')' ';'
        """
        print_token = self.consume(TokenType.KW_PRINT, "Esperado 'print'")
        self.consume(TokenType.EXCLAMATION, "Esperado '!' após 'print'")
        self.consume(TokenType.LPAREN, "Esperado '(' após 'print!'")

        # ID ou CADEIA
        if self.check(TokenType.IDENTIFIER):
            token = self.advance()
            value = token.lexeme
            is_identifier = True
        elif self.check(TokenType.STRING):
            token = self.advance()
            value = token.literal  # o conteúdo da string sem aspas
            is_identifier = False
        else:
            raise ParserError("Esperado identificador ou string dentro de 'print!'", self.peek())

        self.consume(TokenType.RPAREN, "Esperado ')' após argumento de 'print!'")
        self.consume(TokenType.SEMICOLON, "Esperado ';' após 'print!'")

        return Print(value, is_identifier, print_token.line, print_token.column)

    def parse_conditional(self) -> Conditional:
        """
        condicional :
            'if' expressaoRelacional bloco |
            'if' expressaoRelacional bloco 'else' bloco
        """
        if_token = self.consume(TokenType.KW_IF, "Esperado 'if'")
        condition = self.parse_relational_expression()
        then_block = self.parse_block()

        # else opcional
        else_block = None
        if self.match(TokenType.KW_ELSE):
            else_block = self.parse_block()

        return Conditional(condition, then_block, else_block, if_token.line, if_token.column)

    def parse_while(self) -> While:
        """
        repeticao : 'while' expressaoRelacional bloco
        """
        while_token = self.consume(TokenType.KW_WHILE, "Esperado 'while'")
        condition = self.parse_relational_expression()
        block = self.parse_block()

        return While(condition, block, while_token.line, while_token.column)

    def parse_arithmetic_expression(self) -> ArithmeticExpression:
        """
        expressaoAritmetica :
            expressaoAritmetica '+' termo |
            expressaoAritmetica '-' termo |
            termo

        Implementado com eliminação de recursão à esquerda:
        expressaoAritmetica : termo (('+' | '-') termo)*
        """
        expr = self.parse_term()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous().lexeme
            right = self.parse_term()
            expr = BinaryOp(expr, operator, right)

        return expr

    def parse_term(self) -> ArithmeticExpression:
        """
        termo :
            termo '*' fator |
            termo '/' fator |
            fator

        Implementado com eliminação de recursão à esquerda:
        termo : fator (('*' | '/' | '%') fator)*
        """
        expr = self.parse_factor()

        while self.match(TokenType.STAR, TokenType.SLASH, TokenType.PERCENT):
            operator = self.previous().lexeme
            right = self.parse_factor()
            expr = BinaryOp(expr, operator, right)

        return expr

    def parse_factor(self) -> ArithmeticExpression:
        """
        fator :
            NUMINT |
            NUMREAL |
            ID |
            '(' expressaoAritmetica ')'
        """
        # Número
        if self.match(TokenType.NUMBER):
            token = self.previous()
            return Number(token.literal, token.lexeme)

        # Identificador
        if self.match(TokenType.IDENTIFIER):
            token = self.previous()
            return Identifier(token.lexeme)

        # Expressão entre parênteses
        if self.match(TokenType.LPAREN):
            expr = self.parse_arithmetic_expression()
            self.consume(TokenType.RPAREN, "Esperado ')' após expressão")
            return expr

        raise ParserError("Esperado número, identificador ou '('", self.peek())

    def parse_relational_expression(self) -> RelationalExpression:
        """
        expressaoRelacional :
            expressaoAritmetica OP_REL expressaoAritmetica |
            '(' expressaoRelacional ')' |
            expressaoRelacional operadorLogico termoRelacional

        Para evitar ambiguidade e recursão à esquerda, implementamos:
        expressaoRelacional : termoRelacional (operadorLogico termoRelacional)*

        termoRelacional :
            expressaoAritmetica OP_REL expressaoAritmetica |
            '(' expressaoRelacional ')' |
            '!' termoRelacional
        """
        expr = self.parse_relational_term()

        # operadorLogico: && | ||
        while self.match(TokenType.LOGICAL_AND, TokenType.LOGICAL_OR):
            operator = self.previous().lexeme
            right = self.parse_relational_term()
            expr = LogicalOp(expr, operator, right)

        return expr

    def parse_relational_term(self) -> RelationalExpression:
        """
        termoRelacional :
            expressaoAritmetica OP_REL expressaoAritmetica |
            '(' expressaoRelacional ')' |
            '!' termoRelacional
        """
        # Negação lógica: '!'
        if self.match(TokenType.EXCLAMATION):
            operand = self.parse_relational_term()
            return LogicalNot(operand)

        # Expressão entre parênteses - pode ser relacional ou aritmética
        if self.check(TokenType.LPAREN):
            # Salva posição atual para potencial backtracking
            saved_pos = self.current
            self.advance()  # consome '('

            # Tenta parsear como expressão aritmética primeiro
            left = self.parse_arithmetic_expression()

            # Se após a expressão aritmética temos ')', é uma expressão aritmética entre parênteses
            # Mas ainda precisamos de um operador relacional depois
            if self.check(TokenType.RPAREN):
                self.advance()  # consome ')'

                # Verifica se há operador relacional após os parênteses
                if self.check(TokenType.REL_OPERATOR):
                    operator = self.advance().lexeme
                    right = self.parse_arithmetic_expression()
                    return RelationalOp(left, operator, right)
                else:
                    # Sem operador relacional, erro
                    raise ParserError("Esperado operador relacional", self.peek())

            # Se não tem ')', pode ser uma expressão relacional complexa dentro dos parênteses
            # Restaura posição e tenta parsear como expressão relacional
            self.current = saved_pos
            self.advance()  # consome '(' novamente
            expr = self.parse_relational_expression()
            self.consume(TokenType.RPAREN, "Esperado ')' após expressão relacional")
            return expr

        # expressaoAritmetica OP_REL expressaoAritmetica
        left = self.parse_arithmetic_expression()

        if self.match(TokenType.REL_OPERATOR):
            operator = self.previous().lexeme
            right = self.parse_arithmetic_expression()
            return RelationalOp(left, operator, right)

        raise ParserError("Esperado operador relacional", self.peek())

    # -----------------------
    # Métodos auxiliares
    # -----------------------

    def has_errors(self) -> bool:
        """Verifica se houve erros durante o parsing"""
        return len(self.errors) > 0

    def get_errors(self) -> List[ParserError]:
        """Retorna a lista de erros"""
        return self.errors
