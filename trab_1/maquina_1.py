import tkinter as tk

# Tabela de transição
TE = [
    [1, 0],  # s0
    [2, 1],  # s1
    [2, 0]   # s2
]

# Saídas
VS = [0, 1, 1]

estado = 0

# --- interface ---
janela = tk.Tk()
janela.title("Máquina de Estados Finitos")

canvas = tk.Canvas(janela, width=400, height=300)
canvas.pack()

# posições dos estados
pos = {
    0: (100,150),
    1: (300,80),
    2: (300,220)
}

circulos = {}

def desenhar_maquina():
    global circulos

    canvas.delete("all")

    # desenhar transições
    canvas.create_line(120,150,280,80,arrow=tk.LAST)
    canvas.create_line(300,100,300,200,arrow=tk.LAST)
    canvas.create_line(280,220,120,150,arrow=tk.LAST)

    # desenhar estados
    for s,(x,y) in pos.items():

        cor = "lightgreen" if s == estado else "white"

        circulos[s] = canvas.create_oval(
            x-30,y-30,
            x+30,y+30,
            fill=cor,
            width=2
        )

        canvas.create_text(x,y,text=f"s{s}\n/{VS[s]}")

def atualizar():
    desenhar_maquina()
    estado_label.config(text=f"Estado: s{estado}")
    saida_label.config(text=f"Saída: {VS[estado]}")

def entrada(valor):
    global estado
    estado = TE[estado][valor]
    atualizar()

def reset():
    global estado
    estado = 0
    atualizar()

estado_label = tk.Label(janela,font=("Arial",14))
estado_label.pack()

saida_label = tk.Label(janela,font=("Arial",14))
saida_label.pack()

frame = tk.Frame(janela)
frame.pack(pady=10)

tk.Button(frame,text="Entrada 0",width=10,command=lambda:entrada(0)).grid(row=0,column=0)
tk.Button(frame,text="Entrada 1",width=10,command=lambda:entrada(1)).grid(row=0,column=1)
tk.Button(frame,text="Reset",width=10,command=reset).grid(row=0,column=2)

atualizar()

janela.mainloop()