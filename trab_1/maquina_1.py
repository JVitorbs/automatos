import tkinter as tk

# Tabela de transição: TE[estado_atual][entrada] → próximo estado
# Alfabeto de entrada: {0, 1}
# Estados: s0, s1, s2
TE = [
    [1, 0],  # s0: com 0 vai para s1, com 1 fica em s0
    [2, 1],  # s1: com 0 vai para s2, com 1 fica em s1
    [2, 0]   # s2: com 0 fica em s2, com 1 vai para s0
]

# Saídas de cada estado (Máquina de Moore: saída depende apenas do estado)
# s0 → 0, s1 → 1, s2 → 1
VS = [0, 1, 1]

# Estado inicial da máquina
estado = 0

# --- interface ---
janela = tk.Tk()
janela.title("Máquina de Estados Finitos")

# Área de desenho onde os estados e transições serão renderizados
canvas = tk.Canvas(janela, width=400, height=300)
canvas.pack()

# Coordenadas (x, y) de cada estado no canvas
pos = {
    0: (100,150),
    1: (300,80),
    2: (300,220)
}

# Dicionário para guardar referências aos círculos desenhados no canvas
circulos = {}

def desenhar_maquina():
    """Redesenha todos os estados e transições no canvas."""
    global circulos

    # Limpa o canvas antes de redesenhar
    canvas.delete("all")

    # Desenhar as setas de transição entre os estados
    canvas.create_line(120,150,280,80,arrow=tk.LAST)   # s0 → s1
    canvas.create_line(300,100,300,200,arrow=tk.LAST)  # s1 → s2
    canvas.create_line(280,220,120,150,arrow=tk.LAST)  # s2 → s0

    # Desenhar cada estado como um círculo com rótulo
    for s,(x,y) in pos.items():

        # Estado ativo fica verde; os demais ficam brancos
        cor = "lightgreen" if s == estado else "white"

        circulos[s] = canvas.create_oval(
            x-30,y-30,
            x+30,y+30,
            fill=cor,
            width=2
        )

        # Exibe o nome do estado e sua saída dentro do círculo
        canvas.create_text(x,y,text=f"s{s}\n/{VS[s]}")

def atualizar():
    """Atualiza o canvas e os labels de estado e saída."""
    desenhar_maquina()
    estado_label.config(text=f"Estado: s{estado}")
    saida_label.config(text=f"Saída: {VS[estado]}")

def entrada(valor):
    """Aplica uma entrada (0 ou 1) e avança para o próximo estado."""
    global estado
    estado = TE[estado][valor]  # consulta a tabela de transição
    atualizar()

def reset():
    """Reinicia a máquina para o estado inicial s0."""
    global estado
    estado = 0
    atualizar()

# Label que exibe o estado atual
estado_label = tk.Label(janela,font=("Arial",14))
estado_label.pack()

# Label que exibe a saída do estado atual
saida_label = tk.Label(janela,font=("Arial",14))
saida_label.pack()

# Frame com os botões de controle
frame = tk.Frame(janela)
frame.pack(pady=10)

tk.Button(frame,text="Entrada 0",width=10,command=lambda:entrada(0)).grid(row=0,column=0)
tk.Button(frame,text="Entrada 1",width=10,command=lambda:entrada(1)).grid(row=0,column=1)
tk.Button(frame,text="Reset",width=10,command=reset).grid(row=0,column=2)

# Desenho inicial da máquina
atualizar()

# Inicia o loop principal da interface gráfica
janela.mainloop()