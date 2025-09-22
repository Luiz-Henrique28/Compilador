# token_type.py
from enum import Enum, auto

# Define todos os tipos de tokens possíveis que nosso analisador léxico pode gerar.
class TokenType(Enum):
    # Palavras-chave
    PROGRAMA = auto()
    VAR = auto()
    INTEIRO_TIPO = auto()
    REAL_TIPO = auto()
    TEXTO_TIPO = auto()
    SE = auto()
    SENAO = auto()
    FIMSE = auto()  # Adicionado
    ENQUANTO = auto()
    FIMENQUANTO = auto()  # Adicionado
    FUNCAO = auto()  # Adicionado
    FIMFUNCAO = auto()  # Adicionado
    RETORNE = auto()  # Adicionado
    ESCREVA = auto()
    LEIA = auto()
    INICIO = auto()
    FIM = auto()

    # Símbolos e Operadores
    DOIS_PONTOS = auto()
    PONTO_VIRGULA = auto()
    VIRGULA = auto()
    ATRIBUICAO = auto()
    SOMA = auto()  # +
    SUB = auto()   # -
    MULT = auto()  # *
    DIV = auto()   # /
    IGUAL = auto()
    MENOR = auto()
    MAIOR = auto()
    MENOR_IGUAL = auto()
    MAIOR_IGUAL = auto()
    DIFERENTE = auto()
    LPAREN = auto()
    RPAREN = auto()

    # Literais e Identificadores
    ID = auto()
    INTEIRO_CONST = auto()  # Adicionado
    INTEIRO = auto()
    REAL = auto()
    TEXTO = auto()

    # Fim de Arquivo
    EOF = auto()