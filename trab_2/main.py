import tkinter as tk
from tkinter import messagebox

# ===================== TABELAS =====================
unidades = ["", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
especiais = {
    10: "dez", 11: "onze", 12: "doze", 13: "treze", 14: "quatorze",
    15: "quinze", 16: "dezesseis", 17: "dezessete", 18: "dezoito", 19: "dezenove"
}
dezenas = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
centenas = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"]

# ===================== LÓGICA =====================
def converter_ate_999(n):
    if n == 0:
        return ""
    if n == 100:
        return "cem"

    c = n // 100
    d = (n % 100) // 10
    u = n % 10

    partes = []

    if c > 0:
        partes.append(centenas[c])

    if 10 <= n % 100 <= 19:
        partes.append(especiais[n % 100])
    else:
        if d > 0:
            partes.append(dezenas[d])
        if u > 0:
            partes.append(unidades[u])

    return " e ".join(partes)


def numero_para_extenso(n):
    if n == 0:
        return "zero"

    milhar = n // 1000
    resto = n % 1000

    partes = []

    if milhar > 0:
        if milhar == 1:
            partes.append("mil")
        else:
            partes.append(converter_ate_999(milhar) + " mil")

    if resto > 0:
        if milhar > 0:
            partes.append(converter_ate_999(resto))
        else:
            partes.append(converter_ate_999(resto))

    return ", ".join(partes)


# ===================== INTERFACE =====================
def converter():
    entrada = entry.get()

    try:
        n = int(entrada)
        if n < 0 or n > 999999:
            raise ValueError

        resultado = numero_para_extenso(n)
        resultado_label.config(text=resultado)

        # Mostrar etapas (simulação da máquina de estados)
        milhar = n // 1000
        resto = n % 1000

        passos = f"Estado INICIAL -> entrada: {n}\n"
        passos += f"Separação: milhar={milhar}, resto={resto}\n"

        if milhar > 0:
            passos += f"Estado MILHAR -> {converter_ate_999(milhar)} mil\n"

        if resto > 0:
            passos += f"Estado CENTENA/DEZENA/UNIDADE -> {converter_ate_999(resto)}\n"

        passos += "Estado FINAL"

        passos_text.delete("1.0", tk.END)
        passos_text.insert(tk.END, passos)

    except:
        messagebox.showerror("Erro", "Entrada inválida! Digite um número entre 0 e 999999.")


# ===================== JANELA =====================
root = tk.Tk()
root.title("Conversor para Extenso (FSM - Mealy)")
root.geometry("500x400")

# Entrada
label = tk.Label(root, text="Digite um número (0 a 999999):")
label.pack(pady=5)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Botão
botao = tk.Button(root, text="Converter", command=converter)
botao.pack(pady=10)

# Resultado
resultado_label = tk.Label(root, text="", wraplength=400, fg="blue")
resultado_label.pack(pady=10)

# Área de passos (FSM)
passos_label = tk.Label(root, text="Simulação da Máquina de Estados:")
passos_label.pack()

passos_text = tk.Text(root, height=10, width=60)
passos_text.pack(pady=5)

root.mainloop()
