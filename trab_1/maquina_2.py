import tkinter as tk

# Tabela de transicao: TE[estado_atual][entrada] -> proximo estado
#
# Esta maquina foi montada como detector da sequencia "101".
# Cada estado representa o quanto dessa sequencia ja foi reconhecido:
# s0: nenhum prefixo valido reconhecido ainda
# s1: reconheceu "1"
# s2: reconheceu "10"
# s3: reconheceu "101" (estado de deteccao)
TE = [
    [0,1],  # s0: com 0 continua em s0; com 1 avanca para s1
    [2,1],  # s1: com 0 avanca para s2; com 1 permanece em s1
    [0,3],  # s2: com 0 volta para s0; com 1 detecta "101" e vai para s3
    [2,1]   # s3: apos detectar, segue buscando novas ocorrencias sobrepostas
]

# Saidas por estado (maquina de Moore: a saida depende apenas do estado)
# Apenas s3 gera saida 1, indicando que a sequencia "101" foi detectada.
VS = [0,0,0,1]

# Estado inicial da maquina
estado = 0

# --- Interface grafica ---
janela = tk.Tk()
janela.title("Máquina 2 - Detector 101")

# Area onde os estados e transicoes sao desenhados
canvas = tk.Canvas(janela, width=500, height=300)
canvas.pack()

# Coordenadas (x, y) de cada estado no canvas
pos = {
    0:(80,150),
    1:(200,60),
    2:(350,150),
    3:(200,240)
}

def desenhar():
    """Redesenha toda a maquina no canvas, destacando o estado atual."""

    # Limpa o desenho anterior para atualizar a visualizacao
    canvas.delete("all")

    # Transicoes principais entre estados (setas)
    canvas.create_line(110,140,180,70,arrow=tk.LAST)
    canvas.create_line(230,70,330,140,arrow=tk.LAST)
    canvas.create_line(330,160,220,230,arrow=tk.LAST)
    canvas.create_line(180,230,90,160,arrow=tk.LAST)

    # Desenha os estados (circulos) e suas saidas
    for s,(x,y) in pos.items():

        # Estado ativo em verde para facilitar leitura da simulacao
        cor = "lightgreen" if s == estado else "white"

        canvas.create_oval(
            x-30,y-30,
            x+30,y+30,
            fill=cor,
            width=2
        )

        # Rotulo: nome do estado e saida associada
        canvas.create_text(x,y,text=f"s{s}\n/{VS[s]}")

def atualizar():
    """Atualiza desenho e labels de estado/saida."""
    desenhar()
    estado_label.config(text=f"Estado: s{estado}")
    saida_label.config(text=f"Saída: {VS[estado]}")

def entrada(valor):
    """Processa uma entrada (0 ou 1), muda de estado e redesenha."""
    global estado
    # Consulta a tabela de transicao com (estado atual, entrada)
    estado = TE[estado][valor]
    atualizar()

def reset():
    """Retorna ao estado inicial s0."""
    global estado
    estado = 0
    atualizar()

# Label de estado atual
estado_label = tk.Label(janela,font=("Arial",14))
estado_label.pack()

# Label de saida atual
saida_label = tk.Label(janela,font=("Arial",14))
saida_label.pack()

# Frame com botoes de controle
frame = tk.Frame(janela)
frame.pack(pady=10)

tk.Button(frame,text="Entrada 0",width=10,command=lambda:entrada(0)).grid(row=0,column=0)
tk.Button(frame,text="Entrada 1",width=10,command=lambda:entrada(1)).grid(row=0,column=1)
tk.Button(frame,text="Reset",width=10,command=reset).grid(row=0,column=2)

# Atualiza interface antes de iniciar o loop principal
atualizar()

janela.mainloop()