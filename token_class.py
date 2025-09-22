# ARQUIVO: token_class.py

from token_type import TokenType


class Token:
    """
    Representa um token individual, que é a menor unidade de código.
    """

    def __init__(self,
                 tipo: TokenType,
                 lexema: str,
                 literal: object = None,
                 linha: int = 1):
        """
        Construtor da classe Token.

        Args:
            tipo (TokenType): O tipo do token (ex: INTEIRO, SOMA).
            lexema (str): O trecho do código-fonte que gerou o token (ex: "123", "+").
            literal (object): O valor real do token (ex: o número 123).
            linha (int): A linha onde o token foi encontrado.
        """
        # CORREÇÃO: Os atributos agora são 'tipo', 'lexema', e 'linha' para padronização.
        self.tipo = tipo
        self.lexema = lexema
        self.literal = literal
        self.linha = linha

    def __str__(self):
        """Retorna uma representação em string do token."""
        # CORREÇÃO: Atualizado para usar os novos nomes de atributos.
        return f"Token(Tipo: {self.tipo.name}, Lexema: '{self.lexema}', Literal: {self.literal}, Linha: {self.linha})"
