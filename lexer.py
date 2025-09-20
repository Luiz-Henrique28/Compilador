# lexer.py

from token_class import Token, TokenType
import re


class Lexer:

    def __init__(self, source_code):
        self.source_code = source_code
        self.pos = 0

    def tokenize(self):
        tokens = []
        while self.pos < len(self.source_code):
            # Ignorar espaços em branco, tabulações e novas linhas
            if self.source_code[self.pos].isspace():
                self.pos += 1
                continue

            # Ignorar comentários de linha única
            if self.source_code[self.pos:self.pos + 2] == '//':
                while self.pos < len(self.source_code) and self.source_code[
                        self.pos] != '\n':
                    self.pos += 1
                continue

            # Números (inteiros e decimais)
            match = re.match(r'\d+(\.\d+)?', self.source_code[self.pos:])
            if match:
                value = match.group(0)
                if '.' in value:
                    tokens.append(Token(TokenType.NUMBER, float(value)))
                else:
                    tokens.append(Token(TokenType.NUMBER, int(value)))
                self.pos += len(value)
                continue

            # Operadores e outros caracteres
            char = self.source_code[self.pos]
            if char == '+':
                tokens.append(Token(TokenType.OPERATOR, '+'))
            elif char == '-':
                tokens.append(Token(TokenType.OPERATOR, '-'))
            elif char == '*':
                tokens.append(Token(TokenType.OPERATOR, '*'))
            elif char == '/':
                tokens.append(Token(TokenType.OPERATOR, '/'))
            elif char == '(':
                tokens.append(Token(TokenType.LPAREN, '('))
            elif char == ')':
                tokens.append(Token(TokenType.RPAREN, ')'))
            # Adicione aqui outros tokens que precisar
            else:
                # Se nenhum padrão conhecido for encontrado, lança um erro.
                raise ValueError(f"Caractere inesperado: {char}")

            self.pos += 1

        return tokens
