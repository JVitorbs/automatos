# ==========================================================
# ANALISADOR LÉXICO - Tradutor de Expressões Aritméticas
# ----------------------------------------------------------
# Converte a string de entrada em uma lista de tokens
# usando expressões regulares com grupos nomeados.
# ==========================================================

import re

# Especificação dos tokens reconhecidos pelo léxico.
# Cada tupla contém (nome_do_token, padrão_regex).
# A ordem importa: NUMBER deve vir antes de MISMATCH
# para que dígitos sejam reconhecidos como números.
TOKEN_SPEC = [
    ("NUMBER",  r"\d+(?:\.\d+)?"),   # inteiros (123) ou ponto flutuante (3.14)
    ("PLUS",    r"\+"),               # operador de soma
    ("TIMES",   r"\*"),               # operador de multiplicação
    ("LPAREN",  r"\("),               # parêntese esquerdo
    ("RPAREN",  r"\)"),               # parêntese direito
    ("SKIP",    r"[ \t]+"),           # espaços em branco (serão ignorados)
    ("MISMATCH", r"."),               # qualquer outro caractere (gera erro léxico)
]

# Compila todos os padrões em uma única RegEx com grupos nomeados.
# Exemplo do padrão gerado: (?P<NUMBER>\d+(?:\.\d+)?)|(?P<PLUS>\+)|...
TOKEN_RE = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))


class Token:
    """Representa um token individual extraído da entrada."""

    def __init__(self, type_, value, pos):
        self.type = type_      # tipo do token (NUMBER, PLUS, etc.)
        self.value = value     # string correspondente ao token
        self.pos = pos         # posição (índice) na string original

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, pos={self.pos})"


class LexerError(Exception):
    """Exceção para erros durante a análise léxica."""
    pass


class Lexer:
    """Analisador léxico: transforma string em lista de tokens."""

    def __init__(self, text):
        self.text = text

    def tokenize(self):
        """Percorre a entrada casando os padrões e retorna lista de tokens."""
        tokens = []
        for mo in TOKEN_RE.finditer(self.text):
            kind = mo.lastgroup   # nome do grupo que casou
            value = mo.group()    # texto do token
            pos = mo.start()      # posição na string original

            if kind == "SKIP":
                continue          # espaços são ignorados

            if kind == "MISMATCH":
                raise LexerError(
                    f"Erro léxico: caractere inesperado {value!r} na posição {pos}"
                )

            tokens.append(Token(kind, value, pos))

        return tokens
