# Compilador - Checkpoints 01 e 02
## Analisador Léxico e Sintático

**Disciplina:** Compiladores
**Checkpoints:** 01 (Léxico) + 02 (Sintático)

---

## 📋 Índice

1. [Introdução](#1-introdução)
2. [Estrutura do Projeto](#2-estrutura-do-projeto)
3. [Checkpoint 01 - Analisador Léxico](#3-checkpoint-01---analisador-léxico)
4. [Checkpoint 02 - Analisador Sintático](#4-checkpoint-02---analisador-sintático)
5. [Grafos Sintáticos](#5-grafos-sintáticos)
6. [Como Executar](#6-como-executar)
7. [Testes](#7-testes)
8. [Conclusão](#8-conclusão)

---

## 1. Introdução

Este projeto implementa um compilador com análise léxica e sintática para a linguagem definida pela gramática fornecida pelo professor.

**Fases implementadas:**
- **Fase 1 (Checkpoint 01):** Analisador Léxico - identifica tokens no código fonte
- **Fase 2 (Checkpoint 02):** Analisador Sintático - verifica a estrutura gramatical do programa

---

## 2. Estrutura do Projeto

### Arquivos Principais:
```
Compilador/
├── lexer.py                          # Analisador léxico
├── parser.py                         # Analisador sintático (descendente recursivo)
├── main.py                           # Programa principal
├── gramatica_ckp2_ter_noite.txt     # Especificação da gramática
├── programa_ckp2_ter_noite.txt      # Programa de teste fornecido
├── teste_correto_simples.txt        # Teste adicional (correto)
├── teste_erro1_falta_main.txt       # Teste com erro sintático
├── teste_erro2_falta_ponto_virgula.txt  # Teste com erro sintático
└── DOCUMENTACAO.md                  # Esta documentação
```

---

## 3. Checkpoint 01 - Analisador Léxico

### 3.1. Tokens Reconhecidos

#### Palavras-chave:
- `fn`, `main`, `let`, `mut`
- `i32`, `f64` (tipos)
- `if`, `else`, `while`, `return`
- `read`, `print`

#### Operadores:
- **Aritméticos:** `+`, `-`, `*`, `/`, `%`
- **Relacionais:** `==`, `!=`, `<`, `<=`, `>`, `>=`
- **Lógicos:** `&&`, `||`, `!`
- **Atribuição:** `=`

#### Delimitadores:
- Parênteses: `(`, `)`
- Chaves: `{`, `}`
- Outros: `,`, `;`, `:`

#### Literais:
- **Números:** inteiros e reais (ex: `42`, `3.14`)
- **Strings:** texto entre aspas duplas (ex: `"Hello"`)
- **Identificadores:** nomes de variáveis (ex: `contador`, `x`)

#### Comentários:
- Linha: `// comentário`
- Bloco: `/* comentário */`

### 3.2. Tratamento de Erros Léxicos

O lexer detecta:
- Caracteres inválidos
- Strings não finalizadas
- Comentários de bloco não fechados
- Números malformados

---

## 4. Checkpoint 02 - Analisador Sintático

### 4.1. Técnica Utilizada

**Análise Descendente Recursiva:**
- Cada regra da gramática corresponde a um método no parser
- Os métodos se chamam recursivamente seguindo a estrutura da gramática
- Implementa análise preditiva (LL)

### 4.2. Estrutura do Parser

O arquivo `parser.py` contém:

#### Classes de Nós da AST:
- `Program` - programa completo
- `Block` - bloco de comandos
- `Declaration` - declaração de variável
- `Assignment` - atribuição
- `Read` - comando de leitura
- `Print` - comando de escrita
- `Conditional` - if/else
- `While` - laço while
- `ArithmeticExpression` - expressões aritméticas
- `RelationalExpression` - expressões relacionais

#### Métodos de Parsing:
Cada não-terminal tem seu método:
- `parse_program()` - programa principal
- `parse_block()` - blocos `{ ... }`
- `parse_command()` - comandos individuais
- `parse_declaration()` - declarações `let`
- `parse_assignment()` - atribuições
- `parse_arithmetic_expression()` - expressões aritméticas
- `parse_relational_expression()` - expressões relacionais
- etc.

### 4.3. Tratamento de Erros Sintáticos

**Modo Pânico (Panic Mode Recovery):**
- Quando um erro é detectado, o parser sincroniza em pontos seguros
- Pontos de sincronização: `;`, `{`, `}`, palavras-chave de comandos
- Permite detectar múltiplos erros em uma única execução

**Exemplos de erros detectados:**
- Falta de `main` após `fn`
- Falta de ponto e vírgula
- Falta de tipo em declarações
- Parênteses não balanceados
- Estruturas incompletas (if sem bloco, etc)

### 4.4. AST - Árvore Sintática Abstrata

O parser constrói uma AST que representa a estrutura do programa.

**Exemplo:**
```
fn main() {
    let x:i32;
    x = 10;
}
```

**AST gerada:**
```
Program
└── Block
    ├── Declaration(identifier='x', type='i32')
    └── Assignment(identifier='x', expression=Number(10))
```

---

## 5. Grafos Sintáticos

### 5.1. Programa
```
programa → fn main ( ) bloco
```

### 5.2. Bloco
```
bloco → { listaComandos }

listaComandos → comando listaComandos
              | comando
```

### 5.3. Comandos

```
comando → declaracao
        | atribuicao
        | leitura
        | escrita
        | condicional
        | repeticao
        | bloco
```

#### Declaração:
```
declaracao → let mutavel ID : tipo ;

mutavel → mut
        | ε (vazio)

tipo → i32
     | f64
```

#### Atribuição:
```
atribuicao → ID = expressaoAritmetica ;
```

#### Leitura:
```
leitura → read ( ID ) ;
```

#### Escrita:
```
escrita → print ! ( ID ) ;
        | print ! ( CADEIA ) ;
```

#### Condicional:
```
condicional → if expressaoRelacional bloco
            | if expressaoRelacional bloco else bloco
```

#### Repetição:
```
repeticao → while expressaoRelacional bloco
```

### 5.4. Expressões

#### Expressão Aritmética:
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

**Implementação (eliminando recursão à esquerda):**
```
expressaoAritmetica → termo ((+ | -) termo)*
termo → fator ((* | / | %) fator)*
```

#### Expressão Relacional:
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

**Implementação:**
```
expressaoRelacional → termoRelacional (operadorLogico termoRelacional)*
termoRelacional → ! termoRelacional
                | ( expressaoRelacional )
                | ( expressaoAritmetica ) OP_REL expressaoAritmetica
                | expressaoAritmetica OP_REL expressaoAritmetica
```

---

## 6. Como Executar

### 6.1. Análise Completa (Léxica + Sintática)

```bash
python main.py --input programa_ckp2_ter_noite.txt
```

**Saída esperada (programa correto):**
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

### 6.2. Modo Verboso (detalhes)

```bash
python main.py --input programa_ckp2_ter_noite.txt --verbose
```

Exibe:
- Todos os tokens identificados
- AST completa do programa

### 6.3. Apenas Análise Léxica

```bash
python main.py --input programa.txt --lex-only
```

### 6.4. Testar Programas com Erros

```bash
python main.py --input teste_erro1_falta_main.txt
```

**Saída esperada (programa com erro):**
```
============================================================
FASE 2: ANALISE SINTATICA
============================================================

ERROS SINTATICOS ENCONTRADOS:
  Erro sintático na linha 2, coluna 4: Esperado 'main' após 'fn'

Analise sintatica falhou.
```

---

## 7. Testes

### 7.1. Programas Corretos

| Arquivo | Descrição | Resultado Esperado |
|---------|-----------|-------------------|
| `programa_ckp2_ter_noite.txt` | Programa fornecido pelo professor | ✅ Compila |
| `teste_correto_simples.txt` | Programa simples com if/while | ✅ Compila |

### 7.2. Programas com Erros

| Arquivo | Erro | Mensagem |
|---------|------|----------|
| `teste_erro1_falta_main.txt` | Usa "programa" ao invés de "main" | "Esperado 'main' após 'fn'" |
| `teste_erro2_falta_ponto_virgula.txt` | Esquece `;` na declaração | "Esperado ';' após declaração" |

### 7.3. Executar Todos os Testes

```bash
# Teste 1: Programa principal
python main.py --input programa_ckp2_ter_noite.txt

# Teste 2: Programa simples
python main.py --input teste_correto_simples.txt

# Teste 3: Erro - falta main
python main.py --input teste_erro1_falta_main.txt

# Teste 4: Erro - falta ponto e vírgula
python main.py --input teste_erro2_falta_ponto_virgula.txt
```

---

## 8. Conclusão

### Objetivos Alcançados:

✅ **Checkpoint 01 (Léxico):**
- Tokenização completa do código fonte
- Reconhecimento de todos os tokens necessários
- Detecção de erros léxicos

✅ **Checkpoint 02 (Sintático):**
- Análise sintática descendente recursiva
- Implementação de todas as regras da gramática
- Construção da AST
- Detecção e recuperação de erros sintáticos
- Compilação bem-sucedida do programa de teste fornecido

### Funcionalidades Principais:

1. **Análise em duas fases** (léxica e sintática)
2. **Detecção de erros** com mensagens claras
3. **Modo verboso** para debugging
4. **Múltiplos programas de teste** para validação
5. **Código modular** e bem documentado

---

## 📚 Referências

- Material da disciplina de Compiladores
- Gramática fornecida: `gramática_ckp2_ter_noite.txt`
- Programa de teste: `programa_ckp2_ter_noite.txt`
