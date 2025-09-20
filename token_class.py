# token_class.py

class Token:
    """
    Representa um token, que é a menor unidade de código com significado.
    Cada token tem um tipo e um valor (o texto original do código).
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        """
        Retorna uma representação em string do token, útil para depuração.
        Exemplo: Token(IDENTIFIER, 'x')
        """
        # self.type.name pega o nome da enumeração (ex: "IDENTIFIER")
        return f"Token({self.type.name}, '{self.value}')"
