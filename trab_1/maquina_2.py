import tkinter as tk

# tabela de transição
TE = [
    [0,1],  # s0
    [2,1],  # s1
    [0,3],  # s2
    [2,1]   # s3
]

# saídas
VS = [0,0,0,1]

estado = 0

janela = tk.Tk()
janela.title("Máquina 2 - Detector 101")

canvas = tk.Canvas(janela, width=500, height=300)
canvas.pack()

# posições dos estados
pos = {
    0:(80,150),
    1:(200,60),
    2:(350,150),
    3:(200,240)
}

def desenhar():

    canvas.delete("all")

    # transições principais
    canvas.create_line(110,140,180,70,arrow=tk.LAST)
    canvas.create_line(230,70,330,140,arrow=tk.LAST)
    canvas.create_line(330,160,220,230,arrow=tk.LAST)
    canvas.create_line(180,230,90,160,arrow=tk.LAST)

    # estados
    for s,(x,y) in pos.items():

        cor = "lightgreen" if s == estado else "white"

        canvas.create_oval(
            x-30,y-30,
            x+30,y+30,
            fill=cor,
            width=2
        )

        canvas.create_text(x,y,text=f"s{s}\n/{VS[s]}")

def atualizar():
    desenhar()
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