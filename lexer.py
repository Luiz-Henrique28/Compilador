# lexer.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, List, Any


class LexerError(Exception):
    pass


class TokenType(Enum):
    # Valores / identificadores
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()  # CADEIA - strings literais

    # Palavras reservadas (prefixo KW_)
    KW_FN = auto()  # fn
    KW_MAIN = auto()  # main
    KW_LET = auto()  # let
    KW_MUT = auto()  # mut
    KW_I32 = auto()  # i32
    KW_F64 = auto()  # f64
    KW_READ = auto()  # read
    KW_INT = auto()
    KW_FLOAT = auto()
    KW_IF = auto()
    KW_ELSE = auto()
    KW_WHILE = auto()
    KW_RETURN = auto()
    KW_PRINT = auto()

    # Operadores aritméticos
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()  # % (módulo)

    # Parênteses e delimitadores
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()  # :
    EXCLAMATION = auto()  # !

    # Atribuição e relacionais
    ASSIGNMENT = auto()  # =
    REL_OPERATOR = auto()  # ==, !=, <, <=, >, >=

    # Operadores lógicos
    LOGICAL_AND = auto()  # &&
    LOGICAL_OR = auto()  # ||

    # Comentários
    LINE_COMMENT = auto()  # // ...
    BLOCK_COMMENT = auto()  # /* ... */

    # Especiais
    EOF = auto()
    LEXICAL_ERROR = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: Optional[Any]
    line: int
    column: int


class Lexer:

    def __init__(self, source: str, keep_comments: bool = False) -> None:
        self.source = source
        self.length = len(source)
        self.index = 0
        self.line = 1
        self.column = 1
        self.keep_comments = keep_comments

        self._keywords = {
            "fn": TokenType.KW_FN,
            "main": TokenType.KW_MAIN,
            "let": TokenType.KW_LET,
            "mut": TokenType.KW_MUT,
            "i32": TokenType.KW_I32,
            "f64": TokenType.KW_F64,
            "read": TokenType.KW_READ,
            "int": TokenType.KW_INT,
            "float": TokenType.KW_FLOAT,
            "if": TokenType.KW_IF,
            "else": TokenType.KW_ELSE,
            "while": TokenType.KW_WHILE,
            "return": TokenType.KW_RETURN,
            "print": TokenType.KW_PRINT,
        }

    # -------------
    # Utilitários
    # -------------
    def is_at_end(self) -> bool:
        return self.index >= self.length

    def current_char(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.index]

    def peek(self, offset: int = 1) -> str:
        idx = self.index + offset
        if idx >= self.length:
            return "\0"
        return self.source[idx]

    def advance(self) -> str:
        if self.is_at_end():
            return "\0"
        ch = self.source[self.index]
        self.index += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def make_token(self, ttype: TokenType, lexeme: str, literal: Optional[Any],
                   line: int, column: int) -> Token:
        return Token(ttype, lexeme, literal, line, column)

    def error(self,
              message: str,
              line: int,
              column: int,
              lexeme: str = "") -> Token:
        # Emite um token de erro léxico com a mensagem no literal
        return Token(TokenType.LEXICAL_ERROR, lexeme, message, line, column)

    # -----------------------------------------
    # Pular espaços e (opcionalmente) emitir comentários
    # -----------------------------------------
    def skip_whitespace_and_comments(self) -> Optional[Token]:
        while not self.is_at_end():
            ch = self.current_char()

            # Espaços e quebras de linha
            if ch in (" ", "\t", "\r"):
                self.advance()
                continue
            if ch == "\n":
                self.advance()
                continue

            # Comentários
            if ch == "/":
                nxt = self.peek()
                # Comentário de linha: //...
                if nxt == "/":
                    start_line, start_col = self.line, self.column
                    start_idx = self.index
                    # Consome até antes do '\n' ou EOF
                    while not self.is_at_end() and self.current_char() != "\n":
                        self.advance()
                    if self.keep_comments:
                        lexeme = self.source[start_idx:self.index]
                        return self.make_token(TokenType.LINE_COMMENT, lexeme,
                                               None, start_line, start_col)
                    # Se não vamos manter comentários, apenas continue o loop para
                    # consumir o '\n' (se houver) como whitespace normal
                    continue

                # Comentário de bloco: /* ... */
                if nxt == "*":
                    start_line, start_col = self.line, self.column
                    start_idx = self.index
                    # Consome '/*'
                    self.advance()
                    self.advance()
                    # Agora consome até '*/' ou EOF
                    while not self.is_at_end():
                        if self.current_char() == "*" and self.peek() == "/":
                            self.advance()
                            self.advance()
                            if self.keep_comments:
                                lexeme = self.source[start_idx:self.index]
                                return self.make_token(TokenType.BLOCK_COMMENT,
                                                       lexeme, None,
                                                       start_line, start_col)
                            # Comentário consumido e ignorado; volta a pular espaços
                            break
                        else:
                            self.advance()
                    else:
                        # EOF atingido sem fechar '*/'
                        partial = self.source[start_idx:self.index]
                        return self.error("comentário de bloco não finalizado",
                                          start_line, start_col, partial)
                    continue

            # Nada mais para pular
            break

        return None

    # -----------------------
    # Identificadores/palavras-chave
    # -----------------------
    def scan_identifier_or_keyword(self, start_line: int,
                                   start_col: int) -> Token:
        start_idx = self.index
        self.advance()  # já consumiu o primeiro caractere (letra ou _)
        while not self.is_at_end():
            ch = self.current_char()
            if ch == "_" or ch.isalnum():
                self.advance()
            else:
                break

        lexeme = self.source[start_idx:self.index]
        ttype = self._keywords.get(lexeme, TokenType.IDENTIFIER)
        return self.make_token(ttype, lexeme, None, start_line, start_col)

    # -----------------------
    # Strings literais (CADEIA)
    # -----------------------
    def scan_string(self, start_line: int, start_col: int) -> Token:
        start_idx = self.index
        self.advance()  # consome '"' inicial

        while not self.is_at_end() and self.current_char() != '"':
            if self.current_char() == '\n':
                # String multilinha não permitida
                partial = self.source[start_idx:self.index]
                return self.error("string não finalizada (quebra de linha)",
                                  start_line, start_col, partial)
            if self.current_char() == '\\':
                # Sequências de escape simples: \n, \t, \", \\
                self.advance()  # consome '\'
                if not self.is_at_end():
                    self.advance()  # consome o caractere após '\'
            else:
                self.advance()

        if self.is_at_end():
            # EOF sem fechar a string
            partial = self.source[start_idx:self.index]
            return self.error("string não finalizada (EOF)", start_line, start_col, partial)

        # Consome '"' final
        self.advance()

        lexeme = self.source[start_idx:self.index]  # inclui as aspas
        # O literal é a string sem as aspas
        literal = lexeme[1:-1]
        return self.make_token(TokenType.STRING, lexeme, literal, start_line, start_col)

    # -----------------------
    # Números (int/float simples)
    # -----------------------
    def scan_number(self, start_line: int, start_col: int) -> Token:
        start_idx = self.index
        has_dot = False

        # Caso 1: começa com ponto
        if self.current_char() == ".":
            nxt = self.peek()
            if nxt is not None and nxt.isdigit():
                has_dot = True
                self.advance()  # consome '.'
                # consome os dígitos da parte fracionária
                while not self.is_at_end() and self.current_char().isdigit():
                    self.advance()
            else:
                # ponto isolado não é número
                return self.error("número inválido '.'", start_line, start_col,
                                  ".")
        else:
            # Caso 2: começa com dígitos
            while not self.is_at_end() and self.current_char().isdigit():
                self.advance()

            # Parte fracionária opcional
            if not self.is_at_end() and self.current_char() == ".":
                nxt = self.peek()
                if nxt is not None and nxt.isdigit():
                    has_dot = True
                    self.advance()  # consome '.'
                    while not self.is_at_end() and self.current_char().isdigit(
                    ):
                        self.advance()
                else:
                    # dígitos seguidos de ponto sem dígito após -> erro léxico do número inteiro + '.'
                    self.advance()  # consome o ponto para não travar
                    lex = self.source[start_idx:self.index]
                    return self.error(f"número inválido '{lex}'", start_line,
                                      start_col, lex)

        lexeme = self.source[start_idx:self.index]
        try:
            literal = float(lexeme) if has_dot else int(lexeme)
        except ValueError:
            return self.error(f"número inválido '{lexeme}'", start_line,
                              start_col, lexeme)

        return self.make_token(TokenType.NUMBER, lexeme, literal, start_line,
                               start_col)

    # -----------------------
    # Próximo token
    # -----------------------
    def next_token(self) -> Token:
        # 1) Pular espaços e comentários (retornando comentários se keep_comments=True)
        while True:
            if self.is_at_end():
                # EOF imediato
                return self.make_token(TokenType.EOF, "", None, self.line,
                                       self.column)

            maybe_comment = self.skip_whitespace_and_comments()
            if maybe_comment is not None:
                # Mantendo comentários: retorne um por vez
                return maybe_comment

            # Após pular espaços/comentários, pode ter chegado em EOF
            if self.is_at_end():
                return self.make_token(TokenType.EOF, "", None, self.line,
                                       self.column)

            # Agora há algo para ler
            break

        start_line, start_col = self.line, self.column
        ch = self.current_char()

        # 2) Strings literais
        if ch == '"':
            return self.scan_string(start_line, start_col)

        # 3) Identificadores / Palavras‑reservadas
        if ch.isalpha() or ch == "_":
            return self.scan_identifier_or_keyword(start_line, start_col)

        # 4) Números iniciando por dígito
        if ch.isdigit():
            return self.scan_number(start_line, start_col)

        # 3b) Números iniciando com ponto: .5, .123, etc.
        #     (mantém '12.' NÃO aceito como número com ponto final; ficará '12' e depois '.' separado/erro)
        if ch == "." and self.peek().isdigit():
            start_idx = self.index
            self.advance()  # consome '.'
            while self.current_char().isdigit():
                self.advance()
            lexeme = self.source[start_idx:self.index]  # ex: ".5"
            try:
                literal = float(lexeme)
            except ValueError:
                return self.error(f"número inválido '{lexeme}'", start_line,
                                  start_col, lexeme)
            return self.make_token(TokenType.NUMBER, lexeme, literal,
                                   start_line, start_col)

        # 4) Operadores e pontuação simples
        if ch == "+":
            self.advance()
            return self.make_token(TokenType.PLUS, "+", None, start_line,
                                   start_col)

        if ch == "-":
            self.advance()
            return self.make_token(TokenType.MINUS, "-", None, start_line,
                                   start_col)

        if ch == "*":
            self.advance()
            return self.make_token(TokenType.STAR, "*", None, start_line,
                                   start_col)

        if ch == "/":
            # Se fosse '//' ou '/*', já teria sido consumido em skip_whitespace_and_comments()
            self.advance()
            return self.make_token(TokenType.SLASH, "/", None, start_line,
                                   start_col)

        if ch == "%":
            self.advance()
            return self.make_token(TokenType.PERCENT, "%", None, start_line,
                                   start_col)

        if ch == "(":
            self.advance()
            return self.make_token(TokenType.LPAREN, "(", None, start_line,
                                   start_col)

        if ch == ")":
            self.advance()
            return self.make_token(TokenType.RPAREN, ")", None, start_line,
                                   start_col)

        if ch == "{":
            self.advance()
            return self.make_token(TokenType.LBRACE, "{", None, start_line,
                                   start_col)

        if ch == "}":
            self.advance()
            return self.make_token(TokenType.RBRACE, "}", None, start_line,
                                   start_col)

        if ch == ",":
            self.advance()
            return self.make_token(TokenType.COMMA, ",", None, start_line,
                                   start_col)

        if ch == ";":
            self.advance()
            return self.make_token(TokenType.SEMICOLON, ";", None, start_line,
                                   start_col)

        if ch == ":":
            self.advance()
            return self.make_token(TokenType.COLON, ":", None, start_line,
                                   start_col)

        # 5) '=' e operadores relacionais
        if ch == "=":
            if self.peek() == "=":
                self.advance()
                self.advance()
                return self.make_token(TokenType.REL_OPERATOR, "==", None,
                                       start_line, start_col)
            else:
                self.advance()
                return self.make_token(TokenType.ASSIGNMENT, "=", None,
                                       start_line, start_col)

        if ch == ">":
            if self.peek() == "=":
                self.advance()
                self.advance()
                return self.make_token(TokenType.REL_OPERATOR, ">=", None,
                                       start_line, start_col)
            else:
                self.advance()
                return self.make_token(TokenType.REL_OPERATOR, ">", None,
                                       start_line, start_col)

        if ch == "<":
            if self.peek() == "=":
                self.advance()
                self.advance()
                return self.make_token(TokenType.REL_OPERATOR, "<=", None,
                                       start_line, start_col)
            else:
                self.advance()
                return self.make_token(TokenType.REL_OPERATOR, "<", None,
                                       start_line, start_col)

        if ch == "!":
            if self.peek() == "=":
                self.advance()
                self.advance()
                return self.make_token(TokenType.REL_OPERATOR, "!=", None,
                                       start_line, start_col)
            else:
                # '!' usado em print! e como operador de negação
                self.advance()
                return self.make_token(TokenType.EXCLAMATION, "!", None,
                                       start_line, start_col)

        # 6) Operadores lógicos && e ||
        if ch == "&":
            if self.peek() == "&":
                self.advance()
                self.advance()
                return self.make_token(TokenType.LOGICAL_AND, "&&", None,
                                       start_line, start_col)
            else:
                # '&' sozinho não é suportado
                self.advance()
                return self.error("símbolo '&' inesperado", start_line,
                                  start_col, "&")

        if ch == "|":
            if self.peek() == "|":
                self.advance()
                self.advance()
                return self.make_token(TokenType.LOGICAL_OR, "||", None,
                                       start_line, start_col)
            else:
                # '|' sozinho não é suportado
                self.advance()
                return self.error("símbolo '|' inesperado", start_line,
                                  start_col, "|")

        # 7) Caractere desconhecido
        bad = ch
        self.advance()
        return self.error(f"caractere inesperado '{bad}'", start_line,
                          start_col, bad)

    # -----------------------
    # Tokenize completo
    # -----------------------
    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while True:
            tok = self.next_token()
            tokens.append(tok)
            if tok.type == TokenType.EOF:
                break
        return tokens
