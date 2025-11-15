from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Union


class TokenType(Enum):
    # Identificadores e literais
    IDENTIFIER = auto()
    NUMBER = auto()

    # Palavras reservadas
    KW_INT = auto()
    KW_FLOAT = auto()
    KW_PRINT = auto()
    KW_IF = auto()
    KW_ELSE = auto()

    # Operadores aritméticos
    PLUS = auto()  # +
    MINUS = auto()  # -
    STAR = auto()  # *
    SLASH = auto()  # /

    # Atribuição
    ASSIGN = auto()  # =

    # Operadores relacionais (lexema distingue qual)
    REL_OP = auto()  # >, >=, <, <=, !=, ==

    # Delimitadores
    LPAREN = auto()  # (
    RPAREN = auto()  # )

    # Fim de arquivo
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    literal: Optional[Union[int, float, str]]
    line: int
    column: int

    def __str__(self) -> str:
        # Ex.: 3:15 IDENTIFIER "foo"
        lit = f" literal={self.literal}" if self.literal is not None else ""
        return f"{self.line}:{self.column} {self.type.name} {self.lexeme}{lit}"


class LexicalError(Exception):

    def __init__(self, message: str, line: int, column: int):
        super().__init__(message)
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"Erro léxico (linha {self.line}, coluna {self.column}): {super().__str__()}"
