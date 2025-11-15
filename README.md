Mini Analisador Léxico (Python)

Este projeto implementa um analisador léxico manual em Python com:

    Rastreamento de linha/coluna
    Palavras‑chave: KW_INT, KW_FLOAT, KW_IF, KW_ELSE, KW_WHILE, KW_RETURN
    Identificadores, números (inteiros/decimais)
    Operadores:
        Atribuição: =
        Aritméticos: +, -, *, /
        Relacionais (REL_OPERATOR): <, <=, >, >=, ==, !=
    Delimitadores: ( ) { } [ ] ; ,
    Comentários: “# ...” e “// ...” (linha), “/* ... */” (bloco)
    Saídas: tabela ASCII (padrão) e JSON (--json), com formatos compacto ou “pretty”
    Opções úteis: resumo (--summary), exibir EOF (--show-eof), manter comentários (--keep-comments), limitar tokens (--max-tokens), exibir erros léxicos (--show-errors)

Requisitos

    Python 3.10+ (sem dependências externas)

Estrutura sugerida

    main.py
    lexer.py
    tests/
        inputs/: entradas de teste
        expected/: saídas esperadas (tabela ASCII e JSON)
    docs/apresentacao.md

Instalação

    Clone o repositório
    Use Python 3.10 ou superior

Execução

    Gerar tokens em tabela (padrão):

    bash

python3 main.py --input tests/inputs/input1.txt

Ler da entrada padrão:

bash

cat tests/inputs/input1.txt | python3 main.py --stdin

Saída em JSON (compacta):

bash

python3 main.py --input tests/inputs/input1.txt --json

Saída em JSON formatada (“pretty”):

bash

python3 main.py --input tests/inputs/input1.txt --json --pretty

Saída em JSON super compacta:

bash

python3 main.py --input tests/inputs/input1.txt --json --compact

Incluir tokens de comentários:

bash

python3 main.py --input tests/inputs/input1.txt --keep-comments

Exibir também o token EOF:

bash

python3 main.py --input tests/inputs/input1.txt --show-eof

Limitar a quantidade de tokens:

bash

python3 main.py --input tests/inputs/input1.txt --max-tokens 100

Exibir tokens de erro léxico (LEXICAL_ERROR) na saída:

bash

python3 main.py --input tests/inputs/input1.txt --show-errors

Rodar testes (auto‑descoberta em tests/inputs):

bash

    python3 main.py --tests

Se você não informar uma entrada, o programa exibirá: “Nenhuma entrada fornecida. Use uma das opções:

    --input CAMINHO/ARQUIVO
    --stdin (ler da entrada padrão)
    --tests (rodar arquivo(s) de teste)”

Formato da tabela (ASCII)

Cada linha: linha:col TOKEN lexema literal

Exemplo: 18:1 KW_IF if None

    lexema: o texto exato do token
    literal: valor interpretado (ex.: int, float), ou None quando não aplicável

Formato do JSON

Estrutura (lista de objetos):

    type: nome do token (string)
    lexeme: lexema (string)
    literal: valor literal (int/float/string/null)
    line: número da linha (1‑based)
    column: número da coluna inicial (1‑based)

Exemplo:

json

[
  {"type": "KW_IF", "lexeme": "if", "literal": null, "line": 18, "column": 1},
  {"type": "LPAREN", "lexeme": "(", "literal": null, "line": 18, "column": 4}
]

Palavras‑chave reconhecidas

    int, float, if, else, while, return