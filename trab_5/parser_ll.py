# ==========================================================
# ANALISADOR SINTÁTICO - Parser LL(1) Descendente Recursivo
# ----------------------------------------------------------
# Implementa a gramática na forma normal LL:
#
#   E  -> T E'
#   E' -> + T E' | ε
#   T  -> F T'
#   T' -> * F T' | ε
#   F  -> (E) | id
#
# Constrói uma Árvore Sintática Abstrata (AST) a partir
# da sequência de tokens fornecida pelo lexer.
# ==========================================================


class AST:
    """Classe base para todos os nós da AST."""
    pass


class Num(AST):
    """Nó folha: representa um número (inteiro ou float)."""

    def __init__(self, token):
        self.token = token      # token original (para referência)
        self.value = token.value  # valor do número como string

    def __repr__(self):
        return f"Num({self.value})"


class BinOp(AST):
    """Nó interno: representa uma operação binária (soma ou produto)."""

    def __init__(self, left, op_token, right):
        self.left = left          # subárvore esquerda
        self.token = op_token     # token do operador
        self.op = op_token.value  # '+' ou '*'
        self.right = right        # subárvore direita

    def __repr__(self):
        return f"BinOp({self.left}, {self.op}, {self.right})"


class ParserError(Exception):
    """Exceção para erros durante a análise sintática."""
    pass


class Parser:
    """Parser LL(1) descendente recursivo para expressões aritméticas."""

    def __init__(self, tokens):
        self.tokens = tokens    # lista de tokens do lexer
        self.pos = 0            # posição atual na lista

    # --------------------------------------------------
    # Métodos auxiliares de navegação
    # --------------------------------------------------

    def current(self):
        """Retorna o token atual ou None se chegou ao fim."""
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def advance(self):
        """Avança para o próximo token."""
        self.pos += 1

    def expect(self, type_):
        """Verifica se o token atual é do tipo esperado e avança.
        Levanta ParserError se não corresponder."""
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

    # --------------------------------------------------
    # Método principal: ponto de entrada do parser
    # --------------------------------------------------

    def parse(self):
        """Analisa a lista de tokens e retorna a raiz da AST.
        Verifica se todos os tokens foram consumidos."""
        ast = self.E()
        if self.current() is not None:
            tok = self.current()
            raise ParserError(
                f"Erro sintático na posição {tok.pos}: "
                f"token inesperado {tok.value!r}"
            )
        return ast

    # --------------------------------------------------
    # Implementação das produções da gramática LL
    # --------------------------------------------------

    def E(self):
        """E -> T E'  : processa uma expressão (soma)."""
        left = self.T()
        return self.E_prime(left)

    def E_prime(self, left):
        """E' -> + T E' | ε  : processa zero ou mais somas."""
        if self.current() and self.current().type == "PLUS":
            op = self.expect("PLUS")
            right = self.T()
            node = BinOp(left, op, right)
            return self.E_prime(node)  # recursão para cadeias de +
        return left                     # ε (produção vazia)

    def T(self):
        """T -> F T'  : processa um termo (multiplicação)."""
        left = self.F()
        return self.T_prime(left)

    def T_prime(self, left):
        """T' -> * F T' | ε  : processa zero ou mais multiplicações."""
        if self.current() and self.current().type == "TIMES":
            op = self.expect("TIMES")
            right = self.F()
            node = BinOp(left, op, right)
            return self.T_prime(node)  # recursão para cadeias de *
        return left                     # ε (produção vazia)

    def F(self):
        """F -> (E) | id  : processa um fator (número ou subexpressão)."""
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
