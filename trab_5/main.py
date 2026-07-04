# ==========================================================
# INTERFACE GRÁFICA - Tradutor de Expressões Aritméticas
# ----------------------------------------------------------
# GUI em Tkinter com tema escuro, consistente com os
# trabalhos anteriores da disciplina (DCA-3705).
#
# Fluxo: entrada → Lexer → Parser → CodeGen → exibição
# ==========================================================

import tkinter as tk

from lexer import Lexer, LexerError
from parser_ll import Parser, ParserError
from codegen import CodeGen, evaluate


# ==========================================================
# PALETA DE CORES (tema escuro)
# ==========================================================

BG          = "#0f1419"    # fundo da janela
PAINEL      = "#1a1f2e"    # fundo dos painéis
PAINEL_ALT  = "#242b3d"    # superfície elevada (inputs, text areas)
BORDA       = "#2d3548"    # bordas sutis
TEXTO       = "#e4e7eb"    # texto principal
TEXTO_FRACO = "#8b95a7"    # texto secundário
CIANO       = "#22d3ee"    # destaque principal (títulos)
ROXO        = "#a78bfa"    # destaque secundário
ROXO_ESC    = "#7c3aed"    # botão primário
ROXO_HOVER  = "#8b5cf6"    # hover do botão primário
VERDE       = "#34d399"    # resultado de sucesso
VERMELHO    = "#f87171"    # mensagem de erro

# Fontes
FONTE_LABEL  = ("Segoe UI", 9)
FONTE_BOLD   = ("Segoe UI", 10, "bold")
FONTE_MONO   = ("Consolas", 11)       # monoespaçada para logs
FONTE_MONO_G = ("Consolas", 14, "bold")  # entrada em destaque
FONTE_TITULO = ("Segoe UI", 11, "bold")
FONTE_RES    = ("Consolas", 22, "bold")  # resultado grande


# ==========================================================
# BOTÃO ESTILIZADO (Canvas personalizado)
# ==========================================================

class Botao(tk.Canvas):
    """Botão desenhado no Canvas para hover e tema escuro."""

    def __init__(self, master, texto, comando=None,
                 cor_bg=PAINEL_ALT, cor_hover=BORDA,
                 cor_texto=TEXTO, largura=140, altura=34, primario=False):
        super().__init__(master, width=largura, height=altura,
                         bg=PAINEL, highlightthickness=0, bd=0)
        if primario:
            cor_bg = ROXO_ESC
            cor_hover = ROXO_HOVER
            cor_texto = "#ffffff"

        self.comando = comando
        self.cor_bg = cor_bg
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto
        self.largura = largura
        self.altura = altura
        self.texto = texto

        self._desenhar(cor_bg)
        self.bind("<Enter>", lambda e: self._desenhar(self.cor_hover))
        self.bind("<Leave>", lambda e: self._desenhar(self.cor_bg))
        self.bind("<Button-1>", self._on_click)

    def _desenhar(self, cor):
        """Redesenha o botão com a cor especificada."""
        self.delete("all")
        self.create_rectangle(0, 0, self.largura, self.altura,
                              fill=cor, outline="")
        self.create_text(self.largura / 2, self.altura / 2,
                         text=self.texto, fill=self.cor_texto,
                         font=FONTE_BOLD)

    def _on_click(self, _):
        if self.comando:
            self.comando()


# ==========================================================
# JANELA PRINCIPAL
# ==========================================================

class TradutorGUI:
    """Interface principal do tradutor."""

    def __init__(self, raiz):
        self.raiz = raiz
        raiz.title("Tradutor de Expressões Aritméticas")
        raiz.geometry("820x700")
        raiz.configure(bg=BG)
        raiz.minsize(700, 600)
        self._montar()

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    def _montar(self):
        """Monta o layout completo da janela."""
        # Cabeçalho
        cab = tk.Frame(self.raiz, bg=BG)
        cab.pack(fill="x", padx=24, pady=(20, 4))
        tk.Label(cab, text="Tradutor de Expressões Aritméticas",
                 bg=BG, fg=TEXTO,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(cab, text="DCA-3705  •  5ª Lista de Programação  •  2026.1",
                 bg=BG, fg=TEXTO_FRACO,
                 font=FONTE_LABEL).pack(anchor="w", pady=(2, 0))

        # Container principal
        cont = tk.Frame(self.raiz, bg=BG)
        cont.pack(fill="both", expand=True, padx=24, pady=(8, 20))

        self._montar_entrada(cont)
        self._montar_saida(cont)

    def _montar_entrada(self, pai):
        """Área de entrada: campo de texto + botão traduzir."""
        painel = tk.Frame(pai, bg=PAINEL, padx=20, pady=16)
        painel.pack(fill="x")

        tk.Label(painel, text="EXPRESSÃO ARITMÉTICA",
                 bg=PAINEL, fg=CIANO,
                 font=FONTE_TITULO).pack(anchor="w")
        tk.Label(painel,
                 text="Operadores: + (soma) e * (produto). Use parênteses para agrupar.",
                 bg=PAINEL, fg=TEXTO_FRACO,
                 font=FONTE_LABEL).pack(anchor="w", pady=(2, 10))

        # Linha: entrada + botão
        frame_input = tk.Frame(painel, bg=PAINEL_ALT)
        frame_input.pack(fill="x")

        self.entry = tk.Entry(frame_input, font=FONTE_MONO_G,
                              bg=PAINEL_ALT, fg=TEXTO,
                              insertbackground=CIANO,
                              selectbackground=ROXO_ESC,
                              relief="flat", bd=0)
        self.entry.pack(side="left", fill="x", expand=True, padx=4, pady=4)
        self.entry.bind("<Return>", lambda e: self._traduzir())

        Botao(frame_input, "Traduzir ▶", comando=self._traduzir,
              largura=130, primario=True).pack(side="right", padx=8, pady=4)

    def _montar_saida(self, pai):
        """Área de saída: resultado + tokens + AST + código 3 endereços."""
        painel = tk.Frame(pai, bg=PAINEL, padx=20, pady=16)
        painel.pack(fill="both", expand=True, pady=(12, 0))

        tk.Label(painel, text="RESULTADO",
                 bg=PAINEL, fg=CIANO,
                 font=FONTE_TITULO).pack(anchor="w")

        # Resultado numérico em destaque
        self.lbl_resultado = tk.Label(painel, text="—",
                                      bg=PAINEL, fg=VERDE,
                                      font=FONTE_RES)
        self.lbl_resultado.pack(anchor="w", pady=(8, 12), fill="x")

        # Tokens detectados
        self.txt_tokens = tk.Text(painel, height=5, font=FONTE_MONO,
                                  bg=PAINEL_ALT, fg=TEXTO,
                                  relief="flat", bd=0, padx=12, pady=8,
                                  wrap="none", state="disabled")
        self.txt_tokens.pack(fill="x", pady=(8, 4))

        # AST gerada
        self.txt_ast = tk.Text(painel, height=5, font=FONTE_MONO,
                               bg=PAINEL_ALT, fg=TEXTO,
                               relief="flat", bd=0, padx=12, pady=8,
                               wrap="none", state="disabled")
        self.txt_ast.pack(fill="x", pady=(4, 4))

        # Código de três endereços
        self.txt_code = tk.Text(painel, height=5, font=FONTE_MONO,
                                bg=PAINEL_ALT, fg=TEXTO_FRACO,
                                relief="flat", bd=0, padx=12, pady=8,
                                wrap="none", state="disabled")
        self.txt_code.pack(fill="x", pady=(4, 0))

    # --------------------------------------------------
    # Utilitário para preencher Text widgets
    # --------------------------------------------------

    def _set_texto(self, widget, texto, cor=None):
        """Insere texto em um widget Text (read-only)."""
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", texto)
        if cor:
            widget.config(fg=cor)
        else:
            widget.config(fg=TEXTO)
        widget.config(state="disabled")

    # --------------------------------------------------
    # Pipeline principal
    # --------------------------------------------------

    def _traduzir(self):
        """Executa o pipeline completo: Lexer → Parser → CodeGen."""
        expr = self.entry.get().strip()
        if not expr:
            self.lbl_resultado.config(text="Digite uma expressão", fg=TEXTO_FRACO)
            self._set_texto(self.txt_tokens, "")
            self._set_texto(self.txt_ast, "")
            self._set_texto(self.txt_code, "")
            return

        # 1) ANÁLISE LÉXICA
        try:
            tokens = Lexer(expr).tokenize()
            self._set_texto(self.txt_tokens,
                            "Tokens: " + ", ".join(f"{t.type}({t.value})" for t in tokens))
        except LexerError as e:
            self.lbl_resultado.config(text="ERRO LÉXICO", fg=VERMELHO)
            self._set_texto(self.txt_tokens, str(e))
            self._set_texto(self.txt_ast, "")
            self._set_texto(self.txt_code, "")
            return

        # 2) ANÁLISE SINTÁTICA
        try:
            ast = Parser(tokens).parse()
        except ParserError as e:
            self.lbl_resultado.config(text="ERRO SINTÁTICO", fg=VERMELHO)
            self._set_texto(self.txt_ast, str(e))
            self._set_texto(self.txt_code, "")
            return

        # 3) GERAÇÃO DE CÓDIGO (três endereços)
        try:
            cg = CodeGen()
            cg.generate(ast)
            code_text = cg.get_code()
        except Exception as e:
            code_text = f"Erro na geração de código: {e}"

        # 4) AVALIAÇÃO NUMÉRICA
        try:
            valor = evaluate(ast)
            # Se o resultado é um float "inteiro" (ex: 7.0), exibe como int
            if isinstance(valor, float) and valor == int(valor):
                valor = int(valor)
            self.lbl_resultado.config(text=f"= {valor}", fg=VERDE)
        except Exception as e:
            self.lbl_resultado.config(text=f"Erro na avaliação", fg=VERMELHO)

        # Atualiza as áreas de texto com AST e código gerado
        self._set_texto(self.txt_ast, f"AST: {ast}")
        self._set_texto(self.txt_code, f"Código de 3 endereços:\n{code_text}")


# ==========================================================
# PONTO DE ENTRADA
# ==========================================================

if __name__ == "__main__":
    raiz = tk.Tk()
    TradutorGUI(raiz)
    raiz.mainloop()
