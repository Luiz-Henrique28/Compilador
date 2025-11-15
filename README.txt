================================================================================
COMPILADOR - CHECKPOINTS 01 e 02
Analisador Lexico e Sintatico
================================================================================

ARQUIVOS DO PROJETO:
--------------------
- lexer.py                         : Analisador lexico (Checkpoint 01 ajustado)
- parser.py                        : Analisador sintatico (Checkpoint 02)
- main.py                          : Programa principal
- gramatica_ckp2_ter_noite.txt     : Especificacao da gramatica
- programa_ckp2_ter_noite.txt      : Programa de teste (fornecido)
- teste_correto_simples.txt        : Programa correto simples
- teste_erro1_falta_main.txt       : Teste com erro sintatico
- teste_erro2_falta_ponto_virgula.txt : Teste com erro sintatico
- DOCUMENTACAO.md                  : Documentacao completa com grafos sintaticos


COMO EXECUTAR:
--------------

1. TESTAR O PROGRAMA PRINCIPAL (deve compilar sem erros):

   python main.py --input programa_ckp2_ter_noite.txt


2. VER DETALHES (tokens + arvore sintatica):

   python main.py --input programa_ckp2_ter_noite.txt --verbose


3. TESTAR APENAS ANALISE LEXICA (Checkpoint 01):

   python main.py --input programa.txt --lex-only


4. TESTAR PROGRAMA COM ERRO SINTATICO:

   python main.py --input teste_erro1_falta_main.txt


SAIDA ESPERADA (PROGRAMA CORRETO):
-----------------------------------
============================================================
FASE 1: ANALISE LEXICA
============================================================
[OK] Analise lexica concluida com sucesso (108 tokens)

============================================================
FASE 2: ANALISE SINTATICA
============================================================
[OK] Analise sintatica concluida com sucesso!

============================================================
COMPILACAO BEM-SUCEDIDA!
============================================================


SAIDA ESPERADA (PROGRAMA COM ERRO):
------------------------------------
============================================================
FASE 2: ANALISE SINTATICA
============================================================

ERROS SINTATICOS ENCONTRADOS:
  Erro sintatico na linha X, coluna Y: <mensagem>

Analise sintatica falhou.


ESTRUTURA DO COMPILADOR:
-------------------------
1. FASE LEXICA (lexer.py):
   - Tokenizacao do codigo fonte
   - Identificacao de palavras-chave, operadores, numeros, strings
   - Deteccao de erros lexicos

2. FASE SINTATICA (parser.py):
   - Analise descendente recursiva
   - Construcao da AST (Arvore Sintatica Abstrata)
   - Deteccao de erros sintaticos
   - Recuperacao de erros (modo panico)


TOKENS SUPORTADOS:
------------------
Palavras-chave: fn, main, let, mut, i32, f64, read, print, if, else, while
Operadores: +, -, *, /, %, =, ==, !=, <, <=, >, >=, &&, ||, !
Delimitadores: ( ) { } , ; :
Literais: numeros inteiros, numeros reais, strings


OBSERVACOES:
------------
- O programa principal deve comecar com "fn main() { ... }"
- Todas as declaracoes devem ter tipo (i32 ou f64)
- Print deve ser usado como "print!(valor)" ou "print!("string")"
- Comentarios de linha (//) e bloco (/* */) sao suportados

================================================================================
