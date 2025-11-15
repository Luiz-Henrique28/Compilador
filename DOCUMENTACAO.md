# Compilador - Checkpoint 02
## Analisador Sintático

**Aluno:** [Seu Nome]
**Disciplina:** Compiladores
**Professor:** [Nome do Professor]

---

## 1. Introdução

Este documento apresenta a implementação do Checkpoint 02, que consiste em um **analisador sintático descendente recursivo** para a linguagem definida pela gramática fornecida.

O compilador é composto por:
- **lexer.py**: Analisador léxico (Checkpoint 01 com ajustes)
- **parser.py**: Analisador sintático (Checkpoint 02)
- **main.py**: Programa principal que integra as duas fases

---

## 2. Ajustes no Analisador Léxico

Para suportar a gramática do Checkpoint 02, foram adicionados os seguintes tokens ao lexer:

### Novos Tokens:
- **Palavras-chave**: `fn`, `main`, `let`, `mut`, `i32`, `f64`, `read`
- **Operadores**: `%` (módulo), `:` (dois pontos), `!` (exclamação), `&&` (E lógico), `||` (OU lógico)
- **Literais**: Strings (CADEIA) entre aspas duplas

---

## 3. Grafos Sintáticos

A seguir estão os grafos sintáticos para cada não-terminal da gramática:

### 3.1. Programa
```
programa → fn main ( ) bloco
```

### 3.2. Bloco
```
bloco → { listaComandos }
```

### 3.3. Lista de Comandos
```
listaComandos → comando listaComandos
              | comando
```

### 3.4. Comando
```
comando → declaracao
        | atribuicao
        | leitura
        | escrita
        | condicional
        | repeticao
        | bloco
```

### 3.5. Declaração
```
declaracao → let mutavel ID : tipo ;

mutavel → mut
        | ε (vazio)

tipo → i32
     | f64
```

### 3.6. Atribuição
```
atribuicao → ID = expressaoAritmetica ;
```

### 3.7. Leitura
```
leitura → read ( ID ) ;
```

### 3.8. Escrita
```
escrita → print ! ( ID ) ;
        | print ! ( CADEIA ) ;
```

### 3.9. Condicional
```
condicional → if expressaoRelacional bloco
            | if expressaoRelacional bloco else bloco
```

### 3.10. Repetição
```
repeticao → while expressaoRelacional bloco
```

### 3.11. Expressão Aritmética
```
expressaoAritmetica → expressaoAritmetica + termo
                    | expressaoAritmetica - termo
                    | termo

termo → termo * fator
      | termo / fator
      | fator

fator → NUMINT
      | NUMREAL
      | ID
      | ( expressaoAritmetica )
```

**Nota:** A recursão à esquerda foi eliminada na implementação:
- `expressaoAritmetica → termo ((+ | -) termo)*`
- `termo → fator ((* | / | %) fator)*`

### 3.12. Expressão Relacional
```
expressaoRelacional → expressaoAritmetica OP_REL expressaoAritmetica
                    | ( expressaoRelacional )
                    | expressaoRelacional operadorLogico termoRelacional

termoRelacional → expressaoAritmetica OP_REL expressaoAritmetica
                | ( expressaoRelacional )

operadorLogico → &&
               | ||
               | !
```

**Implementação:** Para evitar ambiguidade, foi usado:
- `expressaoRelacional → termoRelacional (operadorLogico termoRelacional)*`

---

## 4. Implementação

### 4.1. Estrutura do Parser

O parser foi implementado usando a técnica de **análise descendente recursiva**, onde:
- Cada não-terminal da gramática corresponde a um método `parse_XXX()`
- Os métodos chamam uns aos outros de acordo com as regras da gramática
- Erros sintáticos são detectados e reportados com linha e coluna

### 4.2. Árvore Sintática Abstrata (AST)

O parser constrói uma AST composta por nós que representam:
- `Program`: Programa completo
- `Block`: Bloco de comandos
- `Declaration`: Declaração de variável
- `Assignment`: Atribuição
- `Read`: Comando de leitura
- `Print`: Comando de escrita
- `Conditional`: Estrutura if/else
- `While`: Laço while
- `ArithmeticExpression`: Expressões aritméticas
- `RelationalExpression`: Expressões relacionais

### 4.3. Tratamento de Erros

O parser implementa recuperação de erros usando **modo pânico**:
- Quando um erro é detectado, sincroniza em ponto e vírgula ou palavras-chave
- Permite detectar múltiplos erros em uma única execução

---

## 5. Como Executar

### 5.1. Compilar o programa principal
```bash
python main.py --input programa_ckp2_ter_noite.txt
```

### 5.2. Modo verboso (mostra tokens e AST)
```bash
python main.py --input programa_ckp2_ter_noite.txt --verbose
```

### 5.3. Apenas análise léxica
```bash
python main.py --input programa.txt --lex-only
```

---

## 6. Testes

### 6.1. Programa Correto
- `programa_ckp2_ter_noite.txt`: Programa fornecido pelo professor (compila com sucesso)
- `teste_correto_simples.txt`: Programa simples para teste (compila com sucesso)

### 6.2. Programas com Erros Sintáticos
- `teste_erro1_falta_main.txt`: Erro - falta palavra 'main'
- `teste_erro2_falta_ponto_virgula.txt`: Erro - falta ponto e vírgula

### 6.3. Resultados Esperados

**Programa correto:**
```
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
```

**Programa com erro:**
```
============================================================
FASE 2: ANALISE SINTATICA
============================================================

ERROS SINTATICOS ENCONTRADOS:
  Erro sintático na linha X, coluna Y: <mensagem do erro>

Analise sintatica falhou.
```

---

## 7. Conclusão

O analisador sintático foi implementado com sucesso e:
- Compila corretamente o programa `programa_ckp2_ter_noite.txt`
- Detecta e reporta erros sintáticos de forma clara
- Gera uma AST que pode ser usada em fases futuras do compilador
- Implementa todas as regras da gramática fornecida

---

## 8. Referências

- Material da disciplina de Compiladores
- Gramática fornecida: `gramática_ckp2_ter_noite.txt`
- Programa de teste: `programa_ckp2_ter_noite.txt`