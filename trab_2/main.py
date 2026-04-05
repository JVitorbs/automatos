import tkinter as tk
from tkinter import messagebox

# ===================== TABELAS PT =====================
unidades_pt = ["", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
especiais_pt = {
    10: "dez", 11: "onze", 12: "doze", 13: "treze", 14: "quatorze",
    15: "quinze", 16: "dezesseis", 17: "dezessete", 18: "dezoito", 19: "dezenove"
}
dezenas_pt = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"]
centenas_pt = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"]

# ===================== TABELAS EN =====================
unidades_en = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
especiais_en = {
    10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
    15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen"
}
dezenas_en = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

# ===================== LÓGICA =====================
def converter_ate_999(n, lang="pt"):
    if n == 0:
        return ""

    if lang == "pt":
        if n == 100:
            return "cem"

        c = n // 100
        d = (n % 100) // 10
        u = n % 10

        partes = []

        if c > 0:
            partes.append(centenas_pt[c])

        if 10 <= n % 100 <= 19:
            partes.append(especiais_pt[n % 100])
        else:
            if d > 0:
                partes.append(dezenas_pt[d])
            if u > 0:
                partes.append(unidades_pt[u])

        return " e ".join(partes)

    else:  # inglês
        c = n // 100
        d = (n % 100) // 10
        u = n % 10

        partes = []

        if c > 0:
            partes.append(unidades_en[c] + " hundred")

        if 10 <= n % 100 <= 19:
            partes.append(especiais_en[n % 100])
        else:
            if d > 0:
                partes.append(dezenas_en[d])
            if u > 0:
                partes.append(unidades_en[u])

        return " ".join(partes)


def numero_para_extenso(n, lang="pt"):
    if n == 0:
        return "zero" if lang == "pt" else "zero"

    milhar = n // 1000
    resto = n % 1000

    partes = []

    if milhar > 0:
        if lang == "pt":
            if milhar == 1:
                partes.append("mil")
            else:
                partes.append(converter_ate_999(milhar, lang) + " mil")
        else:
            partes.append(converter_ate_999(milhar, lang) + " thousand")

    if resto > 0:
        partes.append(converter_ate_999(resto, lang))

    return ", ".join(partes)


# ===================== INTERFACE =====================
def converter():
    entrada = entry.get()
    lang = idioma_var.get()

    try:
        n = int(entrada)
        if n < 0 or n > 999999:
            raise ValueError

        resultado = numero_para_extenso(n, lang)
        resultado_label.config(text=resultado)

        # FSM
        milhar = n // 1000
        resto = n % 1000

        passos = f"INITIAL STATE -> input: {n}\n" if lang == "en" else f"Estado INICIAL -> entrada: {n}\n"
        passos += f"Split: thousand={milhar}, rest={resto}\n" if lang == "en" else f"Separação: milhar={milhar}, resto={resto}\n"

        if milhar > 0:
            texto_milhar = converter_ate_999(milhar, lang)
            passos += (f"THOUSAND STATE -> {texto_milhar} thousand\n" if lang == "en" 
                       else f"Estado MILHAR -> {texto_milhar} mil\n")

        if resto > 0:
            texto_resto = converter_ate_999(resto, lang)
            passos += (f"HUNDREDS/TENS/UNITS STATE -> {texto_resto}\n" if lang == "en" 
                       else f"Estado CENTENA/DEZENA/UNIDADE -> {texto_resto}\n")

        passos += "FINAL STATE" if lang == "en" else "Estado FINAL"

        passos_text.delete("1.0", tk.END)
        passos_text.insert(tk.END, passos)

    except:
        messagebox.showerror("Error" if lang == "en" else "Erro",
                             "Invalid input!" if lang == "en" else "Entrada inválida!")


# ===================== JANELA =====================
root = tk.Tk()
root.title("Number to Words (FSM - Mealy)")
root.geometry("520x420")

# Idioma
idioma_var = tk.StringVar(value="pt")

frame_idioma = tk.Frame(root)
frame_idioma.pack(pady=5)

tk.Radiobutton(frame_idioma, text="Português", variable=idioma_var, value="pt").pack(side="left")
tk.Radiobutton(frame_idioma, text="English", variable=idioma_var, value="en").pack(side="left")

# Entrada
label = tk.Label(root, text="Digite um número / Enter a number (0-999999):")
label.pack(pady=5)

entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Botão
botao = tk.Button(root, text="Converter", command=converter)
botao.pack(pady=10)

# Resultado
resultado_label = tk.Label(root, text="", wraplength=450, fg="blue")
resultado_label.pack(pady=10)

# FSM
passos_label = tk.Label(root, text="FSM Simulation")
passos_label.pack()

passos_text = tk.Text(root, height=10, width=65)
passos_text.pack(pady=5)

root.mainloop()
