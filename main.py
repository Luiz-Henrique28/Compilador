# main.py

from lexer import AnalisadorLexico
from token_type import TokenType  # <--- CORRIGIDO: importado do arquivo correto

codigo_fonte = """
programa Exemplo;
var
   idade: inteiro;
   acesso_permitido: logico;
inicio
   idade := 25;
   se (idade >= 18) entao
      escreva('Acesso permitido!');
   senao
      escreva('Acesso negado.');
   fimse
fim.
"""

print("--- Iniciando Análise Léxica ---")
lexer = AnalisadorLexico(codigo_fonte)

token = lexer.proximo_token()
while token.tipo != TokenType.EOF:
   print(token)
   token = lexer.proximo_token()

print(token)  # Imprime o token EOF
print("--- Análise Léxica Concluída ---")
