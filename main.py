# main.py
"""
Compilador - Checkpoints 01 e 02
Analisador Léxico e Sintático

Uso:
    python main.py --input programa.txt              # Análise léxica e sintática
    python main.py --input programa.txt --lex-only   # Apenas análise léxica
    python main.py --input programa.txt --verbose    # Modo verboso com AST
"""

import argparse
import sys
from lexer import Lexer, LexerError, TokenType, Token
from parser import Parser, ParserError


def format_token(t: Token) -> str:
    """Formata um token para exibição"""
    lexeme_display = t.lexeme if t.lexeme != "" else "''"
    return f"{t.line}:{t.column} {t.type.name} {lexeme_display} {t.literal}"


def print_tokens(tokens: list[Token], keep_comments: bool = False):
    """Imprime todos os tokens"""
    for t in tokens:
        if not keep_comments and t.type in (TokenType.LINE_COMMENT, TokenType.BLOCK_COMMENT):
            continue
        print(format_token(t))


def print_ast(node, indent=0):
    """Imprime a AST de forma hierárquica"""
    prefix = "  " * indent
    node_type = type(node).__name__

    if hasattr(node, '__dict__'):
        attrs = []
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                attrs.append(f"{key}=[{len(value)} items]")
            elif not isinstance(value, (type(None), bool, int, float, str)):
                attrs.append(f"{key}=<{type(value).__name__}>")
            else:
                attrs.append(f"{key}={repr(value)}")

        attr_str = ", ".join(attrs) if attrs else ""
        print(f"{prefix}{node_type}({attr_str})")

        # Imprime recursivamente os filhos
        for key, value in node.__dict__.items():
            if isinstance(value, list):
                for item in value:
                    if hasattr(item, '__dict__'):
                        print_ast(item, indent + 1)
            elif hasattr(value, '__dict__') and not isinstance(value, (str, int, float, bool)):
                print_ast(value, indent + 1)
    else:
        print(f"{prefix}{node_type}: {node}")


def run_lexer_only(text: str, keep_comments: bool = False):
    """Executa apenas a análise léxica"""
    print("=" * 60)
    print("ANÁLISE LÉXICA")
    print("=" * 60)

    lexer = Lexer(text, keep_comments=keep_comments)
    tokens = lexer.tokenize()

    # Verifica se há erros léxicos
    lexical_errors = [t for t in tokens if t.type == TokenType.LEXICAL_ERROR]

    if lexical_errors:
        print("\nERROS LÉXICOS ENCONTRADOS:")
        for err in lexical_errors:
            print(f"  Linha {err.line}, coluna {err.column}: {err.literal}")
        print()

    print_tokens(tokens, keep_comments)
    print(f"\nTotal de tokens: {len(tokens)}")

    return len(lexical_errors) == 0


def run_full_analysis(text: str, verbose: bool = False):
    """Executa análise léxica e sintática completa"""

    # Fase 1: Análise Léxica
    print("=" * 60)
    print("FASE 1: ANÁLISE LÉXICA")
    print("=" * 60)

    lexer = Lexer(text, keep_comments=False)
    tokens = lexer.tokenize()

    # Verifica erros léxicos
    lexical_errors = [t for t in tokens if t.type == TokenType.LEXICAL_ERROR]

    if lexical_errors:
        print("\nERROS LÉXICOS ENCONTRADOS:")
        for err in lexical_errors:
            print(f"  Linha {err.line}, coluna {err.column}: {err.literal}")
        print("\nAnálise interrompida devido a erros léxicos.")
        return False

    print(f"[OK] Analise lexica concluida com sucesso ({len(tokens)} tokens)")

    if verbose:
        print("\nTOKENS:")
        print_tokens(tokens)

    # Fase 2: Análise Sintática
    print("\n" + "=" * 60)
    print("FASE 2: ANALISE SINTATICA")
    print("=" * 60)

    parser = Parser(tokens)
    ast = parser.parse()

    if parser.has_errors():
        print("\nERROS SINTATICOS ENCONTRADOS:")
        for err in parser.get_errors():
            print(f"  {err}")
        print("\nAnalise sintatica falhou.")
        return False

    if ast is None:
        print("\nErro: AST nao foi gerada corretamente.")
        return False

    print("[OK] Analise sintatica concluida com sucesso!")

    if verbose:
        print("\nARVORE SINTATICA ABSTRATA (AST):")
        print_ast(ast)

    print("\n" + "=" * 60)
    print("COMPILACAO BEM-SUCEDIDA!")
    print("=" * 60)

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Compilador - Checkpoints 01 e 02",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python main.py --input programa_ckp2_ter_noite.txt
  python main.py --input programa_ckp2_ter_noite.txt --verbose
  python main.py --input programa.txt --lex-only
  python main.py --input programa.txt --lex-only --keep-comments
        """
    )

    parser.add_argument(
        "--input",
        "-i",
        help="Caminho do arquivo .txt para analisar (padrão: programa_ckp2_ter_noite.txt)",
        default="programa_ckp2_ter_noite.txt",
    )

    parser.add_argument(
        "--lex-only",
        action="store_true",
        help="Executa apenas análise léxica (Checkpoint 01)",
    )

    parser.add_argument(
        "--keep-comments",
        action="store_true",
        help="Mantém tokens de comentários na saída (apenas com --lex-only)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Exibe informações detalhadas (tokens e AST)",
    )

    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Lê o código-fonte da entrada padrão (ignora --input)",
    )

    args = parser.parse_args()

    try:
        # Lê o código-fonte
        if args.stdin:
            text = sys.stdin.read()
        else:
            with open(args.input, "r", encoding="utf-8") as f:
                text = f.read()

        # Executa análise
        if args.lex_only:
            success = run_lexer_only(text, keep_comments=args.keep_comments)
        else:
            success = run_full_analysis(text, verbose=args.verbose)

        # Código de saída
        sys.exit(0 if success else 1)

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {args.input}", file=sys.stderr)
        sys.exit(2)
    except LexerError as e:
        print(f"Erro léxico: {e}", file=sys.stderr)
        sys.exit(3)
    except ParserError as e:
        print(f"Erro sintático: {e}", file=sys.stderr)
        sys.exit(4)
    except Exception as e:
        print(f"Erro inesperado: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(5)


if __name__ == "__main__":
    main()
