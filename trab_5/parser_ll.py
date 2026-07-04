class AST:
    pass


class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return f"Num({self.value})"


class BinOp(AST):
    def __init__(self, left, op_token, right):
        self.left = left
        self.token = op_token
        self.op = op_token.value
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        self.pos += 1

    def expect(self, type_):
        tok = self.current()
        if tok is None:
            raise ParserError(
                f"Erro sintático: esperava {type_}, mas fim da expressão foi atingido"
            )
        if tok.type != type_:
            raise ParserError(
                f"Erro sintático na posição {tok.pos}: "
                f"esperava {type_}, mas obteve {tok.value!r}"
            )
        self.advance()
        return tok

    def parse(self):
        ast = self.E()
        if self.current() is not None:
            tok = self.current()
            raise ParserError(
                f"Erro sintático na posição {tok.pos}: "
                f"token inesperado {tok.value!r}"
            )
        return ast

    def E(self):
        left = self.T()
        return self.E_prime(left)

    def E_prime(self, left):
        if self.current() and self.current().type == "PLUS":
            op = self.expect("PLUS")
            right = self.T()
            node = BinOp(left, op, right)
            return self.E_prime(node)
        return left

    def T(self):
        left = self.F()
        return self.T_prime(left)

    def T_prime(self, left):
        if self.current() and self.current().type == "TIMES":
            op = self.expect("TIMES")
            right = self.F()
            node = BinOp(left, op, right)
            return self.T_prime(node)
        return left

    def F(self):
        tok = self.current()
        if tok is None:
            raise ParserError(
                "Erro sintático: expressão incompleta, esperava número ou '('"
            )
        if tok.type == "LPAREN":
            self.expect("LPAREN")
            node = self.E()
            self.expect("RPAREN")
            return node
        if tok.type == "NUMBER":
            self.expect("NUMBER")
            return Num(tok)
        raise ParserError(
            f"Erro sintático na posição {tok.pos}: "
            f"token inesperado {tok.value!r}, esperava número ou '('"
        )
