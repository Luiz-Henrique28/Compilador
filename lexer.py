# lexer.py

from token_class import Token
from token_type import TokenType

class Lexer:
    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.current_char = self.source[self.position] if self.position < len(self.source) else None

    def advance(self):
        """Avança o ponteiro de posição e atualiza o caractere atual."""
        self.position += 1
        if self.position < len(self.source):
            self.current_char = self.source[self.position]
        else:
            self.current_char = None # Fim do arquivo

    def skip_whitespace(self):
        """Pula espaços em branco, tabulações e quebras de linha."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        """Pula comentários de linha única que começam com // ou #."""
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
        elif self.current_char == '#':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()

    def peek(self):
        """Olha o próximo caractere sem avançar a posição."""
        peek_pos = self.position + 1
        if peek_pos < len(self.source):
            return self.source[peek_pos]
        return None

    def get_identifier_or_keyword(self):
        """Processa um identificador ou uma palavra-chave."""
        result = ""
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        # Mapeia palavras-chave para seus tipos de token
        keywords = {
            "var": TokenType.VAR_KEYWORD,
            "if": TokenType.IF_KEYWORD,
            "else": TokenType.ELSE_KEYWORD,
            "se": TokenType.IF_KEYWORD,
            "senao": TokenType.ELSE_KEYWORD,
            "funcao": TokenType.IDENTIFIER,  # Função será tratada como identificador por enquanto
            "retorna": TokenType.IDENTIFIER, # Retorno será tratado como identificador por enquanto
            "enquanto": TokenType.IDENTIFIER, # While será tratado como identificador por enquanto
            # Adicione outras palavras-chave aqui (while, for, etc.)
        }

        # Se a string 'result' for uma palavra-chave, retorna o tipo correspondente.
        # Caso contrário, é um identificador.
        token_type = keywords.get(result, TokenType.IDENTIFIER)
        return Token(token_type, result)

    def get_number(self):
        """Processa um número inteiro."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.INTEGER_LITERAL, int(result))

    def get_string(self):
        """Processa uma string literal entre aspas duplas."""
        self.advance() # Pula a primeira aspa
        result = ""
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance() # Pula a última aspa
        return Token(TokenType.STRING_LITERAL, result)

    def get_next_token(self):
        """Retorna o próximo token do código-fonte."""
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if (self.current_char == '/' and self.peek() == '/') or self.current_char == '#':
                self.skip_comment()
                continue

            if self.current_char.isalpha() or self.current_char == '_':
                return self.get_identifier_or_keyword()

            if self.current_char.isdigit():
                return self.get_number()

            if self.current_char == '"':
                return self.get_string()

            # Dicionário para operadores de um caractere
            single_char_tokens = {
                '=': TokenType.ASSIGN,          # <-- CORREÇÃO AQUI
                '+': TokenType.OPERATOR,
                '-': TokenType.OPERATOR,
                '*': TokenType.OPERATOR,
                '/': TokenType.OPERATOR,
                '<': TokenType.OPERATOR,
                '>': TokenType.OPERATOR,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                ';': TokenType.SEMICOLON,
                ',': TokenType.COMMA,
            }

            if self.current_char in single_char_tokens:
                token_type = single_char_tokens[self.current_char]
                token_value = self.current_char
                self.advance()
                return Token(token_type, token_value)

            # Se nenhum token for reconhecido, lança um erro
            raise Exception(f"Caractere não reconhecido: {self.current_char}")

        # Retorna o token de Fim de Arquivo (EOF) quando não há mais caracteres
        return Token(TokenType.EOF, None)

    def tokenize(self):
        """Tokeniza todo o código-fonte e retorna uma lista de tokens."""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens