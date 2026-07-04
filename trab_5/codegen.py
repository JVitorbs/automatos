from parser_ll import Num, BinOp


class CodeGen:
    def __init__(self):
        self.temp_count = 0
        self.instructions = []

    def _new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, node):
        if isinstance(node, Num):
            return node.value
        if isinstance(node, BinOp):
            left = self.generate(node.left)
            right = self.generate(node.right)
            temp = self._new_temp()
            self.instructions.append(f"{temp} = {left} {node.op} {right}")
            return temp
        raise ValueError(f"Unknown node: {node}")

    def get_code(self):
        return "\n".join(self.instructions) if self.instructions else "(nenhum código gerado)"


def evaluate(node):
    if isinstance(node, Num):
        v = node.value
        return int(v) if v.isdigit() or (v.startswith("-") and v[1:].isdigit()) else float(v)
    if isinstance(node, BinOp):
        left = evaluate(node.left)
        right = evaluate(node.right)
        if node.op == "+":
            return left + right
        if node.op == "*":
            return left * right
        raise ValueError(f"Unknown operator: {node.op}")
    raise ValueError(f"Unknown node: {node}")
