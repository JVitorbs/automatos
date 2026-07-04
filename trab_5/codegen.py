# ==========================================================
# GERADOR DE CÓDIGO - Código de Três Endereços + Avaliador
# ----------------------------------------------------------
# Percorre a AST gerada pelo parser e:
#   1) Gera código intermediário de três endereços
#   2) Avalia numericamente a expressão
# ==========================================================

from parser_ll import Num, BinOp


class CodeGen:
    """Gera código de três endereços a partir da AST.

    Cada operação binária produz uma instrução no formato:
        tN = operando_esquerdo operador operando_direito

    Exemplo para "2 + 3 * 4":
        t1 = 3 * 4
        t2 = 2 + t1
    """

    def __init__(self):
        self.temp_count = 0       # contador para nomes de temporários
        self.instructions = []    # lista de instruções geradas

    def _new_temp(self):
        """Cria um novo nome de temporário (t1, t2, t3, ...)."""
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node):
        """Percorre a AST recursivamente gerando instruções.

        Retorna o nome do temporário (ou o valor literal) que
        contém o resultado do nó processado.
        """
        if isinstance(node, Num):
            # Nó folha: retorna o valor literal do número
            return node.value

        if isinstance(node, BinOp):
            # Gera código para os operandos, depois une com o operador
            left = self.generate(node.left)
            right = self.generate(node.right)
            temp = self._new_temp()
            self.instructions.append(f"{temp} = {left} {node.op} {right}")
            return temp

        raise ValueError(f"Tipo de nó desconhecido: {node}")

    def get_code(self):
        """Retorna o código gerado como string formatada."""
        return "\n".join(self.instructions) if self.instructions else "(nenhum código gerado)"


def evaluate(node):
    """Avalia a expressão aritmética representada pela AST.

    Percorre a árvore recursivamente:
      - Num: converte a string para int ou float
      - BinOp: avalia esquerda e direita, aplica o operador

    Retorna o valor numérico resultante.
    """
    if isinstance(node, Num):
        v = node.value
        # Se a string parece um inteiro, converte para int;
        # caso contrário, converte para float
        if v.isdigit() or (v.startswith("-") and v[1:].isdigit()):
            return int(v)
        return float(v)

    if isinstance(node, BinOp):
        left = evaluate(node.left)
        right = evaluate(node.right)
        if node.op == "+":
            return left + right
        if node.op == "*":
            return left * right
        raise ValueError(f"Operador desconhecido: {node.op}")

    raise ValueError(f"Tipo de nó desconhecido: {node}")
