# ==========================================================
# DERIVADOR DE GRAMÁTICA LIVRE DE CONTEXTO  -  GUI escura
# ----------------------------------------------------------
# Disciplina: Autômatos e Linguagens Formais (DCA-3705)
# 4ª Lista de Programação - 2026.1
#
# Interface gráfica em Tkinter, tema escuro.
# Não precisa instalar nada — Tkinter já vem com o Python.
#
# Convenções:
#   - Variáveis = MAIÚSCULAS, terminais = minúsculas/dígitos
#   - ε é representado por '#' na entrada
# ==========================================================

import tkinter as tk
from tkinter import filedialog


# ==========================================================
# PARTE 1 — LÓGICA DA GRAMÁTICA (sem GUI)
# ==========================================================

GRAMATICA_EXEMPLO = """A -> 0A1 | B
B -> #"""


def carregar_regras(texto):
    """Texto -> ({variavel: [producoes]}, simbolo_inicial)."""
    gramatica = {}
    inicial = None
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        sep = "->" if "->" in linha else "→"
        if sep not in linha:
            raise ValueError(f"Regra mal-formada: {linha}")
        lhs, rhs = linha.split(sep, 1)
        lhs = lhs.strip()
        if inicial is None:
            inicial = lhs
        for alt in rhs.split("|"):
            alt = alt.strip()
            if alt == "#":              # '#' representa ε
                alt = ""
            gramatica.setdefault(lhs, []).append(alt)
    if inicial is None:
        raise ValueError("Nenhuma regra encontrada.")
    return gramatica, inicial


def regras_habilitadas(estado, gramatica):
    """Lista de (variavel, producao, posicao) aplicáveis no estado atual."""
    return [
        (s, p, i)
        for i, s in enumerate(estado) if s in gramatica
        for p in gramatica[s]
    ]


def aplicar_regra(estado, producao, pos):
    """Substitui o caractere em `pos` pela `producao`."""
    return estado[:pos] + producao + estado[pos+1:]


# ==========================================================
# PARTE 2 — PALETA DE CORES (tema escuro)
# ==========================================================

class Tema:
    BG          = "#0f1419"   # fundo da janela (quase preto)
    PAINEL      = "#1a1f2e"   # fundo dos painéis
    PAINEL_ALT  = "#242b3d"   # superfície elevada (textbox, listbox)
    BORDA       = "#2d3548"   # bordas sutis

    TEXTO       = "#e4e7eb"   # texto principal
    TEXTO_FRACO = "#8b95a7"   # texto secundário / labels

    CIANO       = "#22d3ee"   # destaque principal — forma sentencial
    CIANO_ESC   = "#0891b2"
    ROXO        = "#a78bfa"   # destaque secundário — botões primários
    ROXO_ESC    = "#7c3aed"
    ROXO_HOVER  = "#8b5cf6"
    VERDE       = "#34d399"   # sucesso
    VERMELHO    = "#f87171"   # erro

    FONTE_UI    = ("Segoe UI", 10)
    FONTE_LABEL = ("Segoe UI", 9)
    FONTE_BOLD  = ("Segoe UI", 10, "bold")
    FONTE_MONO  = ("Consolas", 11)
    FONTE_GIGANTE = ("Consolas", 28, "bold")
    FONTE_TITULO = ("Segoe UI", 11, "bold")


# ==========================================================
# PARTE 3 — WIDGETS CUSTOMIZADOS
# ==========================================================

class BotaoEstilizado(tk.Canvas):
    """Botão desenhado à mão para conseguir cantos visíveis e hover bonito."""

    def __init__(self, master, texto, comando=None,
                 cor_bg=Tema.PAINEL_ALT, cor_hover=Tema.BORDA,
                 cor_texto=Tema.TEXTO, largura=140, altura=34, primario=False):
        super().__init__(master, width=largura, height=altura,
                         bg=Tema.PAINEL, highlightthickness=0, bd=0)
        if primario:
            cor_bg = Tema.ROXO_ESC
            cor_hover = Tema.ROXO_HOVER
            cor_texto = "#ffffff"

        self.comando = comando
        self.cor_bg = cor_bg
        self.cor_hover = cor_hover
        self.cor_texto = cor_texto
        self.largura = largura
        self.altura = altura
        self.texto = texto

        self._desenhar(cor_bg)
        # bindings
        self.bind("<Enter>", lambda e: self._desenhar(self.cor_hover))
        self.bind("<Leave>", lambda e: self._desenhar(self.cor_bg))
        self.bind("<Button-1>", self._on_click)

    def _desenhar(self, cor):
        self.delete("all")
        # cantos arredondados desenhados como retângulo simples (Tk não tem rx
        # nativo em retângulos, mas com Canvas dá pra simular usando ovais nos
        # cantos; para simplicidade, usamos um retângulo simples mais "limpo")
        self.create_rectangle(0, 0, self.largura, self.altura,
                              fill=cor, outline="")
        self.create_text(self.largura / 2, self.altura / 2,
                         text=self.texto, fill=self.cor_texto,
                         font=Tema.FONTE_BOLD)

    def _on_click(self, _):
        if self.comando:
            self.comando()

    def definir_pai(self, novo_bg):
        """Permite alinhar o bg do canvas com o fundo do container pai."""
        self.config(bg=novo_bg)


# ==========================================================
# PARTE 4 — DIÁLOGO CUSTOMIZADO (substitui messagebox feio)
# ==========================================================

def mostrar_dialogo(pai, titulo, mensagem, tipo="info", destaque=None):
    """
    Abre uma janela modal estilizada no tema escuro.
      tipo     : "info", "sucesso", "aviso", "erro"  (controla a cor da borda
                 superior e do ícone)
      destaque : opcional — string a ser exibida em fonte gigante (ex.: a
                 cadeia gerada).
    """
    cores = {
        "info":    Tema.CIANO,
        "sucesso": Tema.VERDE,
        "aviso":   Tema.ROXO,
        "erro":    Tema.VERMELHO,
    }
    icones = {"info": "i", "sucesso": "✓", "aviso": "!", "erro": "×"}
    cor = cores.get(tipo, Tema.CIANO)
    icone = icones.get(tipo, "i")

    dlg = tk.Toplevel(pai)
    dlg.title(titulo)
    dlg.configure(bg=Tema.PAINEL)
    dlg.resizable(False, False)
    # largura fixa para evitar colapso de layout
    LARGURA = 460

    # Faixa superior colorida (acento visual)
    tk.Frame(dlg, bg=cor, height=4, width=LARGURA).pack(fill="x")

    corpo = tk.Frame(dlg, bg=Tema.PAINEL, padx=28, pady=22)
    corpo.pack(fill="both", expand=True)

    # Ícone circular + título
    cabecalho = tk.Frame(corpo, bg=Tema.PAINEL)
    cabecalho.pack(anchor="w", fill="x")
    circulo = tk.Canvas(cabecalho, width=36, height=36,
                        bg=Tema.PAINEL, highlightthickness=0, bd=0)
    circulo.create_oval(2, 2, 34, 34, fill=cor, outline="")
    circulo.create_text(18, 19, text=icone, fill="#ffffff",
                        font=("Segoe UI", 16, "bold"))
    circulo.pack(side="left", padx=(0, 12))
    tk.Label(cabecalho, text=titulo, bg=Tema.PAINEL, fg=Tema.TEXTO,
             font=("Segoe UI", 13, "bold")).pack(side="left")

    # Mensagem
    tk.Label(corpo, text=mensagem, bg=Tema.PAINEL, fg=Tema.TEXTO_FRACO,
             font=Tema.FONTE_UI, justify="left",
             wraplength=LARGURA - 60).pack(anchor="w",
                                           fill="x", pady=(14, 0))

    # Destaque grande (se houver)
    if destaque is not None:
        caixa = tk.Frame(corpo, bg=Tema.PAINEL_ALT, height=70)
        caixa.pack(fill="x", pady=(14, 0))
        caixa.pack_propagate(False)
        tk.Label(caixa, text=destaque, bg=Tema.PAINEL_ALT, fg=cor,
                 font=("Consolas", 22, "bold")).pack(expand=True)

    # Botão OK
    botoes = tk.Frame(corpo, bg=Tema.PAINEL)
    botoes.pack(anchor="e", fill="x", pady=(18, 0))
    BotaoEstilizado(botoes, "OK", comando=dlg.destroy,
                    largura=90, primario=True).pack(side="right")

    # Define largura mínima e centraliza em relação à janela pai
    dlg.update_idletasks()
    altura = dlg.winfo_reqheight()
    px = pai.winfo_rootx() + (pai.winfo_width() - LARGURA) // 2
    py = pai.winfo_rooty() + (pai.winfo_height() - altura) // 2
    dlg.geometry(f"{LARGURA}x{altura}+{px}+{py}")

    # Tornar modal e trazer à frente
    # (a ordem importa: transient → deiconify → grab_set → focus)
    dlg.transient(pai)
    dlg.lift()
    dlg.focus_force()
    dlg.grab_set()

    dlg.bind("<Return>", lambda e: dlg.destroy())
    dlg.bind("<Escape>", lambda e: dlg.destroy())
    pai.wait_window(dlg)


# ==========================================================
# PARTE 5 — INTERFACE PRINCIPAL
# ==========================================================

class DerivadorGUI:
    def __init__(self, raiz):
        self.raiz = raiz
        raiz.title("Derivador de Gramática Livre de Contexto")
        raiz.geometry("1000x680")
        raiz.configure(bg=Tema.BG)
        raiz.minsize(900, 600)

        # Estado da derivação
        self.gramatica = None
        self.estado_atual = None
        self.historico = []

        self._montar()

    # ------------------------------------------------------
    # Layout
    # ------------------------------------------------------
    def _montar(self):
        # Cabeçalho
        cab = tk.Frame(self.raiz, bg=Tema.BG, height=70)
        cab.pack(fill="x", padx=24, pady=(20, 8))
        tk.Label(cab, text="Derivador de Gramática Livre de Contexto",
                 bg=Tema.BG, fg=Tema.TEXTO,
                 font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(cab, text="DCA-3705  •  4ª Lista de Programação  •  2026.1",
                 bg=Tema.BG, fg=Tema.TEXTO_FRACO,
                 font=Tema.FONTE_LABEL).pack(anchor="w", pady=(2, 0))

        # Container principal (duas colunas)
        cont = tk.Frame(self.raiz, bg=Tema.BG)
        cont.pack(fill="both", expand=True, padx=24, pady=(8, 20))
        cont.columnconfigure(0, weight=4)
        cont.columnconfigure(1, weight=6)
        cont.rowconfigure(0, weight=1)

        self._montar_esquerda(cont)
        self._montar_direita(cont)

    # ---- coluna esquerda: gramática ----------------------
    def _montar_esquerda(self, pai):
        painel = tk.Frame(pai, bg=Tema.PAINEL, padx=20, pady=20)
        painel.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        tk.Label(painel, text="GRAMÁTICA", bg=Tema.PAINEL, fg=Tema.CIANO,
                 font=Tema.FONTE_TITULO).pack(anchor="w")
        tk.Label(painel,
                 text="Uma regra por linha. Use '|' para alternativas e '#' para ε.",
                 bg=Tema.PAINEL, fg=Tema.TEXTO_FRACO,
                 font=Tema.FONTE_LABEL, justify="left",
                 wraplength=340).pack(anchor="w", pady=(2, 12))

        # Caixa de texto da gramática
        self.txt_gramatica = tk.Text(
            painel, height=12, font=Tema.FONTE_MONO,
            bg=Tema.PAINEL_ALT, fg=Tema.TEXTO,
            insertbackground=Tema.CIANO,        # cursor ciano
            selectbackground=Tema.ROXO_ESC,
            relief="flat", bd=0,
            padx=12, pady=10, wrap="none")
        self.txt_gramatica.pack(fill="both", expand=True)

        # Botões
        botoes = tk.Frame(painel, bg=Tema.PAINEL)
        botoes.pack(fill="x", pady=(14, 0))

        BotaoEstilizado(botoes, "Exemplo",
                        comando=self._carregar_exemplo,
                        largura=100).pack(side="left", padx=(0, 6))
        BotaoEstilizado(botoes, "Abrir arquivo",
                        comando=self._abrir_arquivo,
                        largura=120).pack(side="left", padx=6)
        BotaoEstilizado(botoes, "Iniciar  ▶",
                        comando=self._iniciar,
                        largura=130, primario=True).pack(side="right")

    # ---- coluna direita: derivação -----------------------
    def _montar_direita(self, pai):
        painel = tk.Frame(pai, bg=Tema.PAINEL, padx=20, pady=20)
        painel.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        tk.Label(painel, text="DERIVAÇÃO", bg=Tema.PAINEL, fg=Tema.CIANO,
                 font=Tema.FONTE_TITULO).pack(anchor="w")

        # Forma sentencial em destaque
        tk.Label(painel, text="Forma sentencial atual",
                 bg=Tema.PAINEL, fg=Tema.TEXTO_FRACO,
                 font=Tema.FONTE_LABEL).pack(anchor="w", pady=(10, 0))

        caixa_estado = tk.Frame(painel, bg=Tema.PAINEL_ALT, height=72)
        caixa_estado.pack(fill="x", pady=(6, 16))
        caixa_estado.pack_propagate(False)
        self.lbl_estado = tk.Label(caixa_estado, text="—",
                                   bg=Tema.PAINEL_ALT, fg=Tema.CIANO,
                                   font=Tema.FONTE_GIGANTE)
        self.lbl_estado.pack(expand=True)

        # Lista de regras habilitadas
        tk.Label(painel, text="Regras habilitadas",
                 bg=Tema.PAINEL, fg=Tema.TEXTO_FRACO,
                 font=Tema.FONTE_LABEL).pack(anchor="w")
        tk.Label(painel, text="Clique duplo aplica a regra.",
                 bg=Tema.PAINEL, fg=Tema.TEXTO_FRACO,
                 font=("Segoe UI", 8, "italic")).pack(anchor="w", pady=(0, 6))

        frame_lista = tk.Frame(painel, bg=Tema.PAINEL_ALT,
                               highlightthickness=0, bd=0)
        frame_lista.pack(fill="both", expand=True)

        self.lst_regras = tk.Listbox(
            frame_lista, font=Tema.FONTE_MONO,
            bg=Tema.PAINEL_ALT, fg=Tema.TEXTO,
            selectbackground=Tema.ROXO_ESC, selectforeground="#ffffff",
            highlightthickness=0, bd=0, relief="flat",
            activestyle="none")
        scroll = tk.Scrollbar(frame_lista, orient="vertical",
                              command=self.lst_regras.yview,
                              bg=Tema.PAINEL_ALT, troughcolor=Tema.PAINEL,
                              activebackground=Tema.ROXO_ESC,
                              borderwidth=0, highlightthickness=0)
        self.lst_regras.config(yscrollcommand=scroll.set)
        self.lst_regras.pack(side="left", fill="both", expand=True,
                             padx=8, pady=8)
        scroll.pack(side="right", fill="y")
        self.lst_regras.bind("<Double-Button-1>",
                             lambda e: self._aplicar_selecionada())

        # Botões inferiores
        botoes = tk.Frame(painel, bg=Tema.PAINEL)
        botoes.pack(fill="x", pady=(12, 0))
        BotaoEstilizado(botoes, "Aplicar regra",
                        comando=self._aplicar_selecionada,
                        largura=140, primario=True).pack(side="left")
        BotaoEstilizado(botoes, "Reiniciar",
                        comando=self._iniciar,
                        largura=110).pack(side="left", padx=8)

        # Histórico
        tk.Label(painel, text="Histórico",
                 bg=Tema.PAINEL, fg=Tema.TEXTO_FRACO,
                 font=Tema.FONTE_LABEL).pack(anchor="w", pady=(16, 4))

        self.txt_historico = tk.Text(
            painel, height=6, font=Tema.FONTE_MONO,
            bg=Tema.PAINEL_ALT, fg=Tema.TEXTO_FRACO,
            relief="flat", bd=0, padx=12, pady=10,
            wrap="word", state="disabled")
        self.txt_historico.pack(fill="x")
        # tag para destacar o estado mais recente
        self.txt_historico.tag_configure("atual", foreground=Tema.CIANO,
                                         font=Tema.FONTE_BOLD)

    # ------------------------------------------------------
    # Ações
    # ------------------------------------------------------
    def _carregar_exemplo(self):
        self.txt_gramatica.delete("1.0", "end")
        self.txt_gramatica.insert("1.0", GRAMATICA_EXEMPLO)

    def _abrir_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Abrir gramática",
            filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
        if not caminho:
            return
        try:
            with open(caminho, encoding="utf-8") as f:
                conteudo = f.read()
        except OSError as e:
            mostrar_dialogo(self.raiz, "Erro ao abrir arquivo",
                            str(e), tipo="erro")
            return
        self.txt_gramatica.delete("1.0", "end")
        self.txt_gramatica.insert("1.0", conteudo)

    def _iniciar(self):
        texto = self.txt_gramatica.get("1.0", "end")
        try:
            self.gramatica, inicial = carregar_regras(texto)
        except ValueError as e:
            mostrar_dialogo(self.raiz, "Erro na gramática",
                            str(e), tipo="erro")
            return
        self.estado_atual = inicial
        self.historico = [inicial]
        self._atualizar()

    def _aplicar_selecionada(self):
        if self.gramatica is None:
            mostrar_dialogo(self.raiz, "Atenção",
                            "Clique em 'Iniciar' primeiro para começar a derivação.",
                            tipo="aviso")
            return
        sel = self.lst_regras.curselection()
        if not sel:
            return
        idx = sel[0]
        habilitadas = regras_habilitadas(self.estado_atual, self.gramatica)
        if idx >= len(habilitadas):
            return
        _var, prod, pos = habilitadas[idx]
        self.estado_atual = aplicar_regra(self.estado_atual, prod, pos)
        self.historico.append(self.estado_atual)
        self._atualizar()

    # ------------------------------------------------------
    # Redesenha tudo a partir do estado atual
    # ------------------------------------------------------
    def _atualizar(self):
        # Forma sentencial em destaque
        self.lbl_estado.config(
            text=self.estado_atual if self.estado_atual else "ε")

        # Lista de regras
        self.lst_regras.delete(0, "end")
        habilitadas = regras_habilitadas(self.estado_atual, self.gramatica)
        for i, (var, prod, pos) in enumerate(habilitadas):
            exib = prod if prod != "" else "ε"
            self.lst_regras.insert(
                "end", f"   {i})   {var} → {exib}        (posição {pos})")
        # zebra striping para facilitar a leitura
        for i in range(self.lst_regras.size()):
            if i % 2 == 1:
                self.lst_regras.itemconfig(i, background=Tema.PAINEL)

        # Histórico (último em destaque)
        self.txt_historico.config(state="normal")
        self.txt_historico.delete("1.0", "end")
        for i, s in enumerate(self.historico):
            linha = f"⇒  {s if s else 'ε'}\n"
            tag = "atual" if i == len(self.historico) - 1 else ""
            self.txt_historico.insert("end", linha, tag)
        self.txt_historico.config(state="disabled")
        self.txt_historico.see("end")

        # Mensagem de fim
        if not habilitadas:
            if any(c in self.gramatica for c in self.estado_atual):
                mostrar_dialogo(
                    self.raiz, "Derivação bloqueada",
                    "Sem regras habilitadas, mas ainda há não-terminais na "
                    "forma sentencial. A gramática não consegue prosseguir "
                    "a partir deste ponto.",
                    tipo="aviso",
                    destaque=self.estado_atual)
            else:
                mostrar_dialogo(
                    self.raiz, "Derivação concluída",
                    "Todos os não-terminais foram expandidos. A cadeia "
                    "terminal abaixo foi gerada pela gramática:",
                    tipo="sucesso",
                    destaque=self.estado_atual if self.estado_atual else "ε")


# ==========================================================
# PARTE 5 — PONTO DE ENTRADA
# ==========================================================
if __name__ == "__main__":
    raiz = tk.Tk()
    DerivadorGUI(raiz)
    raiz.mainloop()