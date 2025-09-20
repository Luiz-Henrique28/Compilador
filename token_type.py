# token_type.py
from enum import Enum, auto

# Define todos os tipos de tokens possíveis que nosso analisador léxico pode gerar.
class TokenType(Enum):
    # Palavras-chave
    VAR_KEYWORD = auto()
    IF_KEYWORD = auto()
    ELSE_KEYWORD = auto()

    # Identificadores e Literais
    IDENTIFIER = auto()
    INTEGER_LITERAL = auto()
    STRING_LITERAL = auto()

    # Operadores e Pontuação
    ASSIGN = auto()          # Para o sinal de '='
    OPERATOR = auto()        # <-- ADICIONADO: Para '+', '-', '*', '/' etc.
    LPAREN = auto()          # '('
    RPAREN = auto()          # ')'
    LBRACE = auto()          # '{'
    RBRACE = auto()          # '}'
    SEMICOLON = auto()       # ';'
    COMMA = auto()           # ','

    # Especiais
    WHITESPACE = auto()
    COMMENT = auto()
    UNKNOWN = auto()
    EOF = auto()             # End-Of-File (Fim do Arquivo)