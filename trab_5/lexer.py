import re

TOKEN_SPEC = [
    ("NUMBER",  r"\d+(?:\.\d+)?"),
    ("PLUS",    r"\+"),
    ("TIMES",   r"\*"),
    ("LPAREN",  r"\("),
    ("RPAREN",  r"\)"),
    ("SKIP",    r"[ \t]+"),
    ("MISMATCH", r"."),
]

TOKEN_RE = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))


class Token:
    def __init__(self, type_, value, pos):
        self.type = type_
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, pos={self.pos})"


class LexerError(Exception):
    pass


class Lexer:
    def __init__(self, text):
        self.text = text

    def tokenize(self):
        tokens = []
        for mo in TOKEN_RE.finditer(self.text):
            kind = mo.lastgroup
            value = mo.group()
            pos = mo.start()
            if kind == "SKIP":
                continue
            if kind == "MISMATCH":
                raise LexerError(
                    f"Erro léxico: caractere inesperado {value!r} na posição {pos}"
                )
            tokens.append(Token(kind, value, pos))
        return tokens
