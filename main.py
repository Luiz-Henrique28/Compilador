# main.py
from lexer import Lexer
from parser import Parser

def main():
    try:
        with open('teste_simples.lang', 'r', encoding='utf-8') as f:
            code = f.read()

        print("--- Iniciando Análise Léxica ---")
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print("Tokens Gerados:")
        for token in tokens:
            print(token)

        print("\n--- Iniciando Análise Sintática (Parsing) ---")
        parser = Parser(tokens)
        ast = parser.parse()
        print("Árvore de Sintaxe Abstrata (AST) Gerada:")
        print(ast)

    except (SyntaxError, Exception) as e:
        print(f"\nOcorreu um erro durante a análise: {e}")

if __name__ == '__main__':
    main()