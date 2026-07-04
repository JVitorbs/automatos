# Tradutor de Expressões Aritméticas

**Disciplina:** Autômatos e Linguagens Formais (DCA-3705)  
**Professor:** Luiz Affonso Guedes  
**Período:** 2026.1  
**Data de Entrega:** 06/07/2026

---

## Visão Geral

Software que implementa um **tradutor para expressões aritméticas** (soma `+` e produto `*` de números não negativos, com parênteses). O tradutor percorre três estágios:

1. **Análise Léxica** — tokenização da entrada usando expressões regulares
2. **Análise Sintática** — parser LL(1) preditivo descendente recursivo
3. **Geração de Código** — código de três endereços e avaliação numérica

### Funcionamento

- O sistema aguarda uma expressão aritmética como string
- Informa se a expressão está correta léxica e sintaticamente
- Em caso de erro, exibe a mensagem e a posição do erro
- Em caso de sucesso, exibe os tokens, a AST, o código de três endereços e o resultado

### Critério de Pontuação

| Item | Pontuação |
|---|---|
| Expressões com 1 dígito e sem espaços | 7,0 |
| Reconhecer espaços em branco | +1,0 |
| Números inteiros com vários dígitos | +1,0 |
| Números em ponto flutuante | +1,0 |
| **Total** | **10,0** |

---

## Gramática Implementada

A gramática da linguagem de expressões aritméticas, conforme especificado no trabalho:

### Forma Padrão

```
E  -> E + T | T
T  -> T * F | F
F  -> (E) | id
```

### Forma Normal para Parser LL (sem recursão à esquerda)

```
E   -> T E'
E'  -> + T E' | ε
T   -> F T'
T'  -> * F T' | ε
F   -> (E) | id
```

Onde `id` é um número (inteiro ou ponto flutuante, não negativo).

---

## Estrutura do Projeto

```
trab_5/
├── lexer.py        # Analisador léxico
├── parser_ll.py    # Analisador sintático (LL(1))
├── codegen.py      # Gerador de código 3 endereços
├── main.py         # Interface gráfica (Tkinter)
└── README.md       # Documentação
```

---

## Módulo 1: Lexer (`lexer.py`)

### Função

Converter a string de entrada em uma sequência de tokens reconhecíveis pelo parser.

### Implementação

Usa uma única expressão regular compilada com grupos nomeados para casar cada tipo de token:

```python
TOKEN_SPEC = [
    ("NUMBER",  r"\d+(?:\.\d+)?"),   # inteiros ou floats
    ("PLUS",    r"\+"),               # operador de soma
    ("TIMES",   r"\*"),               # operador de produto
    ("LPAREN",  r"\("),               # parêntese esquerdo
    ("RPAREN",  r"\)"),               # parêntese direito
    ("SKIP",    r"[ \t]+"),           # espaços (descartados)
    ("MISMATCH", r"."),               # qualquer outro caractere (erro)
]
```

O padrão `\d+(?:\.\d+)?` reconhece:
- Inteiros: `0`, `123`, `42`
- Floats: `3.14`, `0.5`, `10.0`

### Fluxo Léxico

```
Entrada: "12 + 3.5 * (2+3)"
  ↓
Tokens: [NUMBER(12), PLUS(+), NUMBER(3.5), TIMES(*), LPAREN((), NUMBER(2), PLUS(+), NUMBER(3), RPAREN())]
```

### Tratamento de Erros

Se um caractere que não corresponde a nenhum padrão válido é encontrado, o lexer levanta `LexerError` com a posição exata:

```
Entrada: "2@3"
  → Erro léxico: caractere inesperado '@' na posição 1
```

---

## Módulo 2: Parser LL (`parser_ll.py`)

### Função

Analisar a sequência de tokens e construir uma **Árvore Sintática Abstrata (AST)**, verificando se a expressão está de acordo com a gramática.

### Implementação

Parser **descendente recursivo preditivo LL(1)** — cada não-terminal da gramática vira um método:

| Não-terminal | Método | Produção |
|---|---|---|
| `E` | `E()` | `T E'` |
| `E'` | `E_prime(left)` | `+ T E'` \| `ε` |
| `T` | `T()` | `F T'` |
| `T'` | `T_prime(left)` | `* F T'` \| `ε` |
| `F` | `F()` | `(E)` \| `NUMBER` |

### Estruturas da AST

```python
class Num(AST):       # Nó folha — armazena o valor do número
    value: str

class BinOp(AST):     # Nó interno — operação binária
    left: AST         # subexpressão à esquerda
    op: str           # '+' ou '*'
    right: AST        # subexpressão à direita
```

### Exemplo de AST

```
Expressão: "2 + 3 * 4"
  ↓
AST: BinOp(Num(2), +, BinOp(Num(3), *, Num(4)))

         '+'
        /   \
       2    '*'
           /   \
          3     4
```

A precedência de `*` sobre `+` é garantida pela gramática: `T` (que lida com `*`) é chamado dentro de `E_prime` (que lida com `+`), forçando a multiplicação primeiro.

### Tratamento de Erros Sintáticos

- Expressão incompleta: `"2 +"` → `Erro sintático: expressão incompleta, esperava número ou '('`
- Parêntese não fechado: `"(2+3"` → `Erro sintático: esperava RPAREN, mas fim da expressão foi atingido`
- Token inesperado ao final: `"2+3)"` → `Erro sintático na posição N: token inesperado ')'`

---

## Módulo 3: Gerador de Código (`codegen.py`)

### Função

Percorrer a AST e gerar:

1. **Código de três endereços** — sequência de instruções com temporários
2. **Valor numérico** — resultado da expressão

### Geração de Código de Três Endereços

Cada operação binária gera uma instrução no formato `tN = esquerda op direita`, onde `tN` é um novo registrador temporário:

```
Expressão: "2 + 3 * 4"
  ↓
Código 3 endereços:
  t1 = 3 * 4
  t2 = 2 + t1

Expressão: "(2+3)*4"
  ↓
Código 3 endereços:
  t1 = 2 + 3
  t2 = t1 * 4
```

### Avaliação Numérica

A função `evaluate()` percorre a AST recursivamente:

- Nó `Num`: converte o valor para `int` (se inteiro) ou `float` (se contiver ponto)
- Nó `BinOp`: avalia a esquerda e a direita, depois aplica `+` ou `*`

Resultados inteiros são exibidos sem casa decimal (ex: `= 14`), floats mantêm a precisão (ex: `= 8.25`).

---

## Módulo 4: Interface Gráfica (`main.py`)

### Função

Interface visual (Tkinter) em tema escuro, consistente com os trabalhos anteriores da disciplina.

### Layout

```
┌─────────────────────────────────────────────┐
│  Tradutor de Expressões Aritméticas         │
│  DCA-3705 • 5ª Lista • 2026.1               │
├─────────────────────────────────────────────┤
│  EXPRESSÃO ARITMÉTICA                       │
│  ┌─────────────────────────────────┬──────┐ │
│  │  12 + 3.5 * (2+3)              │▶ Tr.│ │
│  └─────────────────────────────────┴──────┘ │
├─────────────────────────────────────────────┤
│  RESULTADO                                  │
│  = 29.5                                     │
│                                             │
│  ┌─────────────────────────────────────────┐│
│  │ Tokens: NUMBER(12) PLUS(+) NUMBER(3.5)...││
│  ├─────────────────────────────────────────┤│
│  │ AST: BinOp(Num(12), +, BinOp(...))       ││
│  ├─────────────────────────────────────────┤│
│  │ Código de 3 endereços:                   ││
│  │ t1 = 3.5 * 5                            ││
│  │ t2 = 12 + t1                            ││
│  └─────────────────────────────────────────┘│
└─────────────────────────────────────────────┘
```

### Cores (Tema Escuro)

- Fundo: quase preto (`#0f1419`)
- Painéis: azul escuro (`#1a1f2e`)
- Destaques: ciano (`#22d3ee`) e roxo (`#a78bfa`)
- Sucesso: verde (`#34d399`)
- Erro: vermelho (`#f87171`)
- Texto: branco suave (`#e4e7eb`)

### Fluxo na Interface

1. Usuário digita a expressão e pressiona Enter ou clica "Traduzir ▶"
2. O sistema executa o pipeline completo: Lexer → Parser → CodeGen
3. Resultados são exibidos nas áreas de texto abaixo
4. Em caso de erro, a etapa que falhou mostra a mensagem em vermelho

---

## Como Executar

```bash
python3 trab_5/main.py
```

## Exemplos de Uso

| Entrada | Resultado |
|---|---|
| `2+3` | `= 5` |
| `2*3` | `= 6` |
| `2+3*4` | `= 14` |
| `(2+3)*4` | `= 20` |
| `12+345*6` | `= 2082` |
| `1.5+2.25*3` | `= 8.25` |
| `3.5 * 2` | `= 7.0` → exibe `= 7` |
| `2@3` | Erro léxico: caractere inesperado |
| `(2+3` | Erro sintático: parêntese não fechado |
| `2+` | Erro sintático: expressão incompleta |

---

## Relação com a Teoria de Autômatos

### Análise Léxica

O lexer implementa o reconhecimento de tokens por expressões regulares, que correspondem a **linguagens regulares** (tipo 3 na hierarquia de Chomsky). Cada token é uma linguagem regular reconhecida por um AFD.

### Análise Sintática

A gramática de expressões aritméticas é uma **linguagem livre de contexto** (tipo 2). O parser LL(1) implementa um **Autômato com Pilha Determinístico (APD)** que decide se a cadeia de tokens pertence à linguagem. A pilha é simulada pelas chamadas recursivas dos métodos.

### Geração de Código

O código de três endereços é uma forma intermediária que separa cada operação em uma instrução elementar, facilitando a geração de código de máquina ou a avaliação direta.
