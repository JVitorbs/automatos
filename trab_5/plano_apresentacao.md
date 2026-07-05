# Plano de Apresentação — Tradutor de Expressões Aritméticas

**Duração estimada:** 12-15 minutos  
**Formato:** Apresentação presencial + demonstração ao vivo

---

## Sumário do Projeto

### Mapeamento Requisito → Implementação

| # | Requisito do Professor | Onde está implementado | Pontuação |
|---|---|---|---|
| 1 | Análise Léxica (RegEx) | `lexer.py:3-13` — especificação dos tokens com RegEx | 7,0 |
| 2 | Análise Sintática (parser LL) | `parser_ll.py:66-107` — métodos `E()`, `E_prime()`, `T()`, `T_prime()`, `F()` | 7,0 |
| 3 | Geração de Código (3 endereços) | `codegen.py:14-22` — método `generate()` da classe `CodeGen` | 7,0 |
| 4 | Avaliação do resultado | `codegen.py:28-40` — função `evaluate()` | 7,0 |
| 5 | Reconhecer espaços em branco | `lexer.py:9` — token `SKIP` com padrão `[ \t]+` | +1,0 |
| 6 | Números inteiros com vários dígitos | `lexer.py:4` — padrão `\d+(?:\.\d+)?` (cobre 1+ dígitos) | +1,0 |
| 7 | Números em ponto flutuante | `lexer.py:4` — parte `(?:\.\d+)?` do padrão `NUMBER` | +1,0 |
| 8 | Tratamento de erro léxico | `lexer.py:10,42-45` — token `MISMATCH` captura caracteres inválidos | 7,0 |
| 9 | Tratamento de erro sintático | `parser_ll.py:42-54,92-107` — `expect()` e `F()` verificam tokens esperados | 7,0 |
| 10 | Interface com usuário (GUI) | `main.py` — classe `TradutorGUI` com Tkinter | 7,0 |

### Estrutura dos Arquivos

| Arquivo | Módulo | Linhas | Função |
|---|---|---|---|
| `lexer.py` | Análise Léxica | 47 | Tokeniza a entrada com RegEx |
| `parser_ll.py` | Análise Sintática | 107 | Parser LL(1) descendente recursivo, constrói AST |
| `codegen.py` | Geração de Código | 40 | Código de 3 endereços + avaliador numérico |
| `main.py` | Interface Gráfica | 212 | GUI Tkinter com pipeline completo |

---

## Roteiro da Apresentação

### 1. Introdução (1 min)

- **Disciplina:** Autômatos e Linguagens Formais (DCA-3705) — Professor Luiz Affonso Guedes
- **O que o trabalho pede:** um tradutor de expressões aritméticas com soma (`+`), produto (`*`) e parênteses, implementando 3 estágios:
  1. Análise Léxica (RegEx)
  2. Análise Sintática (parser LL)
  3. Geração de Código (3 endereços)
- **Sistema:** aguarda entrada → verifica léxico/sintático → se ok, exibe resultado; se erro, exibe mensagem e retorna
- **Pontuação total:** 10,0 (7,0 base + 3 incrementos)

### 2. Visão Geral da Arquitetura (1 min)

```
                    ENTRADA (string)
                         │
                         ▼
              ┌───────────────────┐
              │   lexer.py        │  Análise Léxica (RegEx)
              │   Lexer           │
              └───────┬───────────┘
                      │ tokens
                      ▼
              ┌───────────────────┐
              │   parser_ll.py    │  Análise Sintática (LL(1))
              │   Parser          │
              └───────┬───────────┘
                      │ AST
                      ▼
              ┌───────────────────┐
              │   codegen.py      │  Geração de Código
              │   CodeGen         │  + Avaliador
              └───────┬───────────┘
                      │ resultado
                      ▼
              ┌───────────────────┐
              │   main.py         │  Interface Gráfica
              │   TradutorGUI     │  (Tkinter)
              └───────────────────┘
```

- **Saídas exibidas:** tokens detectados, AST gerada, código de 3 endereços, valor numérico
- **Em caso de erro:** interrompe o pipeline na etapa que falhou e exibe mensagem

### 3. Gramática (1 min)

**Forma Padrão (especificada no PDF):**
```
E  → E + T | T
T  → T * F | F
F  → (E) | id
```

**Por que não usamos essa forma?** Recursão à esquerda (`E → E + T`) — parser descendente entraria em loop infinito.

**Forma LL (implementada em `parser_ll.py:66-107`):**
```
E   → T E'
E'  → + T E' | ε
T   → F T'
T'  → * F T' | ε
F   → (E) | id
```

**Vantagem:** sem recursão à esquerda, permite parsing preditivo descendente com lookahead de 1 token.

**Precedência garantida pela gramática:**
- `*` tem precedência sobre `+` porque `T` (que lida com `*`) está aninhado dentro de `E'` (que lida com `+`)
- Parênteses têm maior precedência porque `F` resolve `(E)` antes de qualquer operador

### 4. Análise Léxica — `lexer.py` (2 min)

**O que faz:** Converte string → lista de tokens

**Implementação** (`lexer.py:3-13`):
```python
TOKEN_SPEC = [
    ("NUMBER",  r"\d+(?:\.\d+)?"),   # ← inteiros E floats
    ("PLUS",    r"\+"),
    ("TIMES",   r"\*"),
    ("LPAREN",  r"\("),
    ("RPAREN",  r"\)"),
    ("SKIP",    r"[ \t]+"),          # ← ignora espaços
    ("MISMATCH", r"."),              # ← captura erros
]
```

**Destaques dos critérios de pontuação:**

| Critério | Como funciona | No código |
|---|---|---|
| 1 dígito (base) | `\d+` casa 1 ou mais dígitos → `2+3` funciona | `lexer.py:4` |
| Espaços (+1,0) | `SKIP` com `[ \t]+` descarta espaços → `2 + 3` funciona | `lexer.py:9` |
| Vários dígitos (+1,0) | `\d+` casa qualquer quantidade → `12+345` funciona | `lexer.py:4` |
| Float (+1,0) | `(?:\.\d+)?` parte opcional → `1.5+2.25` funciona | `lexer.py:4` |

**Erro léxico** (`lexer.py:42-45`):
- Caractere inesperado (ex: `@`, `#`, letras) → `LexerError("Erro léxico: caractere inesperado '@' na posição 1")`
- Volta a aguardar nova entrada

### 5. Análise Sintática — `parser_ll.py` (2.5 min)

**O que faz:** tokens → AST (Árvore Sintática Abstrata)

**Estruturas da AST** (`parser_ll.py:1-22`):
- `Num(token)` — nó folha com o valor do número
- `BinOp(left, op_token, right)` — nó interno com operador e dois operandos

**Implementação do parser** (`parser_ll.py:66-107`):
Cada produção da gramática LL vira um método:

| Método | Produção | Linha |
|---|---|---|
| `E()` | `T E'` | `parser_ll.py:66` |
| `E_prime(left)` | `+ T E'` ou `ε` | `parser_ll.py:70` |
| `T()` | `F T'` | `parser_ll.py:78` |
| `T_prime(left)` | `* F T'` ou `ε` | `parser_ll.py:82` |
| `F()` | `(E)` ou `NUMBER` | `parser_ll.py:90` |

**Exemplos de AST gerada:**

```
Expressão: "2 + 3 * 4"           Expressão: "(2 + 3) * 4"

         '+'                               '*'
        /   \                             /   \
       2    '*'                          '+'   4
           /   \                        /   \
          3     4                      2     3
```

**Erro sintático** (`parser_ll.py:42-54`):
- Expressão incompleta (`2+`) → `"expressão incompleta, esperava número ou '('"`
- Parêntese não fechado (`(2+3`) → `"esperava RPAREN, mas fim da expressão foi atingido"`
- Token inesperado (`2+3)`) → `"token inesperado ')' na posição 3"`

### 6. Geração de Código — `codegen.py` (1.5 min)

**O que faz:** AST → código de três endereços + resultado numérico

**Código de três endereços** (`codegen.py:14-22`):
Cada operação binária gera `tN = left op right`:

```
"2 + 3 * 4"                "(2 + 3) * 4"
t1 = 3 * 4                 t1 = 2 + 3
t2 = 2 + t1                t2 = t1 * 4
```

**Avaliação numérica** (`codegen.py:28-40`):
- `evaluate()` percorre a AST recursivamente
- `Num` → converte string para `int` (se inteiro) ou `float` (se contiver ponto)
- `BinOp` → soma ou multiplica os valores das subárvores
- Resultados inteiros são exibidos sem casa decimal (7 em vez de 7.0)

### 7. Interface Gráfica — `main.py` (1 min)

**O que faz:** entrada do usuário + exibição dos resultados

**Layout** (`main.py`):

```
┌──────────────────────────────────────────────┐
│  Tradutor de Expressões Aritméticas          │
│  DCA-3705 • 5ª Lista • 2026.1               │
├──────────────────────────────────────────────┤
│  EXPRESSÃO ARITMÉTICA                        │
│  ┌──────────────────────────────┬──────────┐ │
│  │  12 + 3.5 * (2+3)           │▶ Traduzir │ │
│  └──────────────────────────────┴──────────┘ │
├──────────────────────────────────────────────┤
│  RESULTADO                                   │
│  = 29.5                                      │
│                                              │
│  ┌──────────────────────────────────────────┐│
│  │ Tokens: NUMBER(12) PLUS(+) NUMBER(3.5)...││  ← `main.py:172-174`
│  ├──────────────────────────────────────────┤│
│  │ AST: BinOp(Num(12), +, BinOp(...))        ││  ← `main.py:205`
│  ├──────────────────────────────────────────┤│
│  │ Código de 3 endereços:                   ││  ← `main.py:206`
│  │ t1 = 3.5 * 5                             ││
│  │ t2 = 12 + t1                             ││
│  └──────────────────────────────────────────┘│
└──────────────────────────────────────────────┘
```

**Pipeline completo** (`main.py:162-206`):
1. Pega expressão do campo de texto
2. Chama `Lexer(expr).tokenize()` → exibe tokens
3. Chama `Parser(tokens).parse()` → exibe AST
4. Chama `CodeGen().generate(ast)` → exibe código 3 endereços
5. Chama `evaluate(ast)` → exibe resultado numérico

**Tratamento de erros na GUI:**
- Erro léxico → resultado mostra "ERRO LÉXICO" em vermelho (`main.py:175-180`)
- Erro sintático → resultado mostra "ERRO SINTÁTICO" em vermelho (`main.py:184-188`)

**Tema escuro:** cores definidas em `main.py:9-21`

### 8. Demonstração ao Vivo (3 min)

#### Testes de Sucesso (mostrar pipeline completo)

| # | Entrada | Resultado | O que demonstra |
|---|---|---|---|
| 1 | `2+3` | = 5 | Base: 1 dígito, sem espaços |
| 2 | `2+3*4` | = 14 | Precedência: `*` antes de `+` |
| 3 | `(2+3)*4` | = 20 | Parênteses: mudam a precedência |
| 4 | `12 + 345 * 6` | = 2082 | Espaços + múltiplos dígitos |
| 5 | `1.5 + 2.25 * 3` | = 8.25 | Ponto flutuante |
| 6 | `3.5 * 2` | = 7 | Float com resultado inteiro |

**Para cada teste, apontar:** a saída de tokens, a AST gerada, o código de 3 endereços, e o resultado.

#### Testes de Erro

| # | Entrada | Erro | O que demonstra |
|---|---|---|---|
| 7 | `2@3` | "Erro léxico: caractere inesperado '@'" | Léxico: caractere inválido |
| 8 | `(2+3` | "Erro sintático: esperava RPAREN" | Sintático: parêntese não fechado |
| 9 | `2+` | "Erro sintático: expressão incompleta" | Sintático: operando faltando |

### 9. Relação com a Teoria de Autômatos (1 min)

| Estágio | Tipo de Linguagem | Autômato Correspondente | Implementação |
|---|---|---|---|
| Léxico | Regular (Tipo 3) | AFD — Automato Finito Determinístico | RegEx em `lexer.py:4-10` |
| Sintático | Livre de Contexto (Tipo 2) | APD — Autômato com Pilha Determinístico | Parser LL recursivo em `parser_ll.py:66-107` |

**Hierarquia de Chomsky:**
- O tradutor percorre dois níveis: regular (lexer) e livre de contexto (parser)
- O lexer reconhece tokens como linguagens regulares
- O parser decide se a sequência de tokens pertence à linguagem livre de contexto definida pela gramática

**Parser LL como APD:**
- A pilha de chamadas recursivas dos métodos `E()`, `T()`, `F()` simula a pilha do APD
- O lookahead de 1 token decide qual produção usar (preditivo)
- `ε` (produção vazia) é implementado como simples retorno sem consumir token

### 10. Conclusão (30s)

- **Todos os critérios implementados e testados**
  - Base (7,0): expressões com 1 dígito sem espaços ✓
  - Espaços (+1,0): `SKIP` no lexer ✓
  - Múltiplos dígitos (+1,0): `\d+` no padrão NUMBER ✓
  - Ponto flutuante (+1,0): `(?:\.\d+)?` no padrão NUMBER ✓
- **Código modular:** cada estágio em seu próprio arquivo
- **12 testes de sucesso + 7 casos de erro** verificados
- **Perguntas**

---

## Dicas para a Defesa

1. **Abra os 4 arquivos** em abas do editor para navegar rápido
2. **Mostre a especificação de tokens** (`lexer.py:3-13`) — é curta e ilustra bem o léxico
3. **Mostre os métodos do parser** (`parser_ll.py:66-107`) — relacione cada método com a gramática no slide
4. **Compare `2+3*4` com `(2+3)*4`** — a diferença na AST e no código de 3 endereços prova a precedência
5. **Demonstre os erros primeiro** (itens 7-9) — mostra que o tratamento funciona e engaja
6. **Slide da gramática** — deixe visível enquanto explica o parser
7. **Não leia os slides** — use como guia, o foco é o código rodando
8. **Menção à teoria:** toda vez que mostrar um token, relacione a AFD; toda vez que mostrar o parser, relacione a APD

---

## Sugestão de Slides (8 slides)

| Slide | Conteúdo |
|---|---|
| 1 | **Capa:** título, disciplina, professor, período, sumário dos critérios |
| 2 | **Gramática:** forma padrão (PDF) vs forma LL (implementada) lado a lado |
| 3 | **Pipeline:** diagrama Entrada → Lexer → Parser → CodeGen → Saída |
| 4 | **Lexer:** tabela de tokens com RegEx, destaque para `NUMBER`, `SKIP`, `MISMATCH` |
| 5 | **Parser:** métodos da gramática, exemplos de AST (`2+3*4` vs `(2+3)*4`) |
| 6 | **Código:** código de 3 endereços, função `evaluate()` |
| 7 | **Critérios + GUI:** tabela de pontuação, print da tela |
| 8 | **Teoria + Conclusão:** hierarquia de Chomsky, AFD → APD, perguntas |

---

## Checklist para o Dia da Defesa

- [ ] Notebook com Python 3 e Tkinter instalados
- [ ] Código aberto no editor (4 abas: `lexer.py`, `parser_ll.py`, `codegen.py`, `main.py`)
- [ ] Slides prontos (8 slides)
- [ ] Expressões de teste copiadas para um bloco de notas (não digitar na hora)
- [ ] Testar `python3 main.py` antes de começar
- [ ] Marcar horário no drive da disciplina
