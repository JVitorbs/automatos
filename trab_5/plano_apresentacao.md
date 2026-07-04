# Plano de Apresentação — Tradutor de Expressões Aritméticas

**Duração estimada:** 10-12 minutos  
**Formato:** Apresentação presencial + demonstração ao vivo

---

## Estrutura da Apresentação

### 1. Introdução (1 min)

- Disciplina: Autômatos e Linguagens Formais (DCA-3705)
- Objetivo do trabalho: implementar um tradutor com 3 estágios (léxico, sintático, código)
- Expressões aritméticas com `+`, `*` e parênteses
- Pontuação: 7,0 base + 1,0 espaços + 1,0 dígitos múltiplos + 1,0 float

### 2. Visão Geral do Sistema (1 min)

- **Entrada:** string com expressão aritmética
- **Pipeline:** Lexer → Parser → CodeGen → Resultado
- **Saída:** tokens, AST, código 3 endereços, valor numérico
- Se erro → mensagem com posição, volta a aguardar entrada

### 3. Gramática (1 min)

Mostrar no slide:

**Forma Padrão:**
```
E → E + T | T
T → T * F | F
F → (E) | id
```

**Forma LL (usada no parser):**
```
E  → T E'
E' → + T E' | ε
T  → F T'
T' → * F T' | ε
F  → (E) | id
```

Explicar: a forma LL elimina a recursão à esquerda para permitir parsing descendente.

### 4. Análise Léxica — Lexer (1.5 min)

- Tokenização com RegEx (grupos nomeados)
- Mostrar a tabela de tokens:
  - `NUMBER` → `\d+(?:\.\d+)?` (cobre inteiros e floats)
  - `PLUS`, `TIMES`, `LPAREN`, `RPAREN`
  - `SKIP` → espaços em branco (descartados)
- Tratamento de erro: `MISMATCH` captura qualquer caractere inválido

**Demonstração rápida no código:**

```python
TOKEN_SPEC = [
    ("NUMBER",  r"\d+(?:\.\d+)?"),
    ("PLUS",    r"\+"),
    ...
]
```

### 5. Análise Sintática — Parser LL (2 min)

- Parser descendente recursivo preditivo LL(1)
- Cada não-terminal da gramática é um método
- Construção da AST (Abstract Syntax Tree):
  - `Num(value)` — nó folha
  - `BinOp(left, op, right)` — nó interno

**Mostrar exemplos de AST no slide:**

```
Expressão: "2 + 3 * 4"

         '+'
        /   \
       2    '*'
           /   \
          3     4
```

```
Expressão: "(2 + 3) * 4"

         '*'
        /   \
       '+'   4
      /   \
     2     3
```

Explicar que a precedência de `*` sobre `+` vem naturalmente da gramática: `T` (multiplicação) está aninhado dentro de `E'` (adição).

### 6. Geração de Código (1.5 min)

- Código de três endereços: cada operação vira uma instrução
- Temporários `t1, t2, ...` para resultados intermediários

**Exemplos:**
```
"2 + 3 * 4"          "(2 + 3) * 4"
t1 = 3 * 4           t1 = 2 + 3
t2 = 2 + t1          t2 = t1 * 4
```

- Avaliação numérica: percorre a AST recursivamente
  - `Num` → converte string para int ou float
  - `BinOp` → avalia esquerda, direita, aplica operador

### 7. Interface Gráfica (1 min)

- Tkinter, tema escuro (mesmo padrão dos trabalhos anteriores)
- Campos:
  - Entrada da expressão + botão "Traduzir ▶"
  - Resultado grande em destaque (verde)
  - Área de tokens detectados
  - Área da AST gerada
  - Área do código de 3 endereços
- Tratamento visual de erros (vermelho)

### 8. Demonstração ao Vivo (2 min)

Expressões para testar (nesta ordem):

| # | Entrada | Expectativa |
|---|---|---|
| 1 | `2+3` | = 5 (base) |
| 2 | `2*3` | = 6 (base) |
| 3 | `2+3*4` | = 14 (precedência) |
| 4 | `(2+3)*4` | = 20 (parênteses) |
| 5 | `12 + 345 * 6` | = 2082 (espaços + multi dígitos) |
| 6 | `1.5 + 2.25 * 3` | = 8.25 (float) |
| 7 | `2@3` | Erro léxico |
| 8 | `(2+3` | Erro sintático |

Mostrar que cada entrada gera os 3 outputs (tokens, AST, código).

### 9. Relação com a Teoria (1 min)

- **Léxico:** linguagens regulares (tipo 3) — AFD para cada token
- **Sintático:** linguagem livre de contexto (tipo 2) — APD implementado como parser LL
- **Hierarquia de Chomsky:** o tradutor percorre dois níveis: regular (lexer) e livre de contexto (parser)

### 10. Conclusão (30s)

- Todos os critérios implementados (7,0 + 1,0 + 1,0 + 1,0)
- Código modular e testado
- Perguntas

---

## Dicas para a Defesa

1. **Tenha o código aberto** nos 3 arquivos (`lexer.py`, `parser_ll.py`, `codegen.py`) para mostrar rapidamente
2. **Demonstre os erros primeiro** (itens 7 e 8) para mostrar que o tratamento funciona
3. **Destaque a precedência** com os exemplos 3 e 4 — é o ponto mais conceitual
4. **Mostre o código de 3 endereços** mudando entre `2+3*4` e `(2+3)*4` — a diferença nas instruções ilustra o efeito dos parênteses
5. **Slide de gramática** — deixe visível durante a explicação do parser
6. **Não leia os slides** — use como guia, o foco deve estar no código rodando

## Sugestão de Slides (6-8 slides)

| Slide | Conteúdo |
|---|---|
| 1 | Capa: título, disciplina, professor, período |
| 2 | Gramática (forma padrão e forma LL lado a lado) |
| 3 | Pipeline: Entrada → Lexer → Parser → CodeGen → Resultado |
| 4 | Tabela de tokens + RegEx |
| 5 | Exemplos de AST (`2+3*4` vs `(2+3)*4`) |
| 6 | Código de 3 endereços (mesmos exemplos) |
| 7 | Critério de pontuação + prints da GUI |
| 8 | Obrigado + perguntas |
