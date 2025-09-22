# Arquivo: lexer.py

from token_class import Token  # <-- CORREÇÃO APLICADA AQUI
from token_type import TokenType


class AnalisadorLexico:

    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.posicao = 0
        self.char_atual = self.codigo_fonte[self.posicao]
        self.palavras_reservadas = {
            "programa": TokenType.PROGRAMA,
            "inicio": TokenType.INICIO,
            "fim": TokenType.FIM,
            "inteiro": TokenType.INTEIRO_TIPO,
            "real": TokenType.REAL_TIPO,
            "se": TokenType.SE,
            "senao": TokenType.SENAO,
            "fimse": TokenType.FIMSE,
            "enquanto": TokenType.ENQUANTO,
            "fimenquanto": TokenType.FIMENQUANTO,
            "funcao": TokenType.FUNCAO,
            "fimfuncao": TokenType.FIMFUNCAO,
            "var": TokenType.VAR,
            "retorne": TokenType.RETORNE,
        }

    def erro(self):
        raise Exception("Caractere inválido na análise léxica")

    def avancar(self):
        self.posicao += 1
        if self.posicao > len(self.codigo_fonte) - 1:
            self.char_atual = None  # Indica o fim do arquivo (EOF)
        else:
            self.char_atual = self.codigo_fonte[self.posicao]

    def pular_espaco_branco(self):
        while self.char_atual is not None and self.char_atual.isspace():
            self.avancar()

    def numero(self):
        resultado = ''
        while self.char_atual is not None and self.char_atual.isdigit():
            resultado += self.char_atual
            self.avancar()
        return Token(TokenType.INTEIRO_CONST, int(resultado))

    def identificador_ou_palavra_reservada(self):
        resultado = ''
        while self.char_atual is not None and (self.char_atual.isalnum() or self.char_atual == '_'):
            resultado += self.char_atual
            self.avancar()

        # Verifica se é uma palavra reservada, senão é um ID
        tipo_token = self.palavras_reservadas.get(resultado.lower(),
                                                  TokenType.ID)
        return Token(tipo_token, resultado)

    def string_literal(self):
        self.avancar()  # Pula a primeira aspa simples
        resultado = ''
        while self.char_atual is not None and self.char_atual != "'":
            resultado += self.char_atual
            self.avancar()
        self.avancar()  # Pula a última aspa simples
        return Token(TokenType.TEXTO, resultado)

    def proximo_token(self):
        while self.char_atual is not None:
            if self.char_atual.isspace():
                self.pular_espaco_branco()
                continue

            if self.char_atual.isdigit():
                return self.numero()

            if self.char_atual.isalpha() or self.char_atual == '_':
                return self.identificador_ou_palavra_reservada()

            if self.char_atual == "'":
                return self.string_literal()

            if self.char_atual == '+':
                self.avancar()
                return Token(TokenType.SOMA, '+')

            if self.char_atual == '-':
                self.avancar()
                return Token(TokenType.SUB, '-')

            if self.char_atual == '*':
                self.avancar()
                return Token(TokenType.MULT, '*')

            if self.char_atual == '/':
                self.avancar()
                return Token(TokenType.DIV, '/')

            if self.char_atual == '(':
                self.avancar()
                return Token(TokenType.LPAREN, '(')

            if self.char_atual == ')':
                self.avancar()
                return Token(TokenType.RPAREN, ')')

            if self.char_atual == ';':
                self.avancar()
                return Token(TokenType.PONTO_VIRGULA, ';')

            if self.char_atual == ',':
                self.avancar()
                return Token(TokenType.VIRGULA, ',')

            if self.char_atual == ':':
                # Verifica se é := (atribuição) ou apenas : (dois pontos)
                if self.codigo_fonte[self.posicao + 1:self.posicao + 2] == '=':
                    self.avancar()  # pula ':'
                    self.avancar()  # pula '='
                    return Token(TokenType.ATRIBUICAO, ':=')
                else:
                    self.avancar()
                    return Token(TokenType.DOIS_PONTOS, ':')

            if self.char_atual == '.':
                self.avancar()
                return Token(TokenType.FIM, '.')

            if self.char_atual == '=':
                self.avancar()
                return Token(TokenType.IGUAL, '=')

            if self.char_atual == '<':
                # Verifica se é <= ou <>
                next_char = self.codigo_fonte[self.posicao + 1:self.posicao + 2] if self.posicao + 1 < len(self.codigo_fonte) else None
                if next_char == '=':
                    self.avancar()
                    self.avancar()
                    return Token(TokenType.MENOR_IGUAL, '<=')
                elif next_char == '>':
                    self.avancar()
                    self.avancar()
                    return Token(TokenType.DIFERENTE, '<>')
                else:
                    self.avancar()
                    return Token(TokenType.MENOR, '<')

            if self.char_atual == '>':
                # Verifica se é >=
                if self.codigo_fonte[self.posicao + 1:self.posicao + 2] == '=':
                    self.avancar()
                    self.avancar()
                    return Token(TokenType.MAIOR_IGUAL, '>=')
                else:
                    self.avancar()
                    return Token(TokenType.MAIOR, '>')

            # Se nenhum dos acima, o caractere é inválido
            self.erro()

        return Token(TokenType.EOF, None)
