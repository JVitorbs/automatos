import tkinter as tk
from tkinter import messagebox

# ===================== TABELAS =====================

unidades_pt = ["", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
especiais_pt = {
    10: "dez", 11: "onze", 12: "doze", 13: "treze", 14: "quatorze",
    15: "quinze", 16: "dezesseis", 17: "dezessete", 18: "dezoito", 19: "dezenove"
}
dezenas_pt = ["", "", "vinte", "trinta", "quarenta", "cinquenta",
              "sessenta", "setenta", "oitenta", "noventa"]
centenas_pt = ["", "cento", "duzentos", "trezentos", "quatrocentos",
               "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos"]

unidades_en = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
especiais_en = {
    10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
    15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen"
}
dezenas_en = ["", "", "twenty", "thirty", "forty", "fifty",
              "sixty", "seventy", "eighty", "ninety"]

# ===================== SAÍDA (λ) =====================

def lambda_ate_999(n, lang):
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

    else:
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

# ===================== FSM =====================

class MealyFSM:
    def __init__(self, n, lang):
        self.n = n
        self.lang = lang
        self.state = "q0"
        self.output = []
        self.log = []

        self.milhar = n // 1000
        self.resto = n % 1000

    def step(self):
        # δ e λ juntos (Mealy)

        if self.state == "q0":
            self.log.append("INITIAL STATE" if self.lang == "en" else "Estado INICIAL")
            self.state = "q_split"

        elif self.state == "q_split":
            self.log.append(
                f"Split: thousand={self.milhar}, rest={self.resto}"
                if self.lang == "en"
                else f"Separação: milhar={self.milhar}, resto={self.resto}"
            )

            if self.milhar > 0:
                self.state = "q_milhar"
            else:
                self.state = "q_resto"

        elif self.state == "q_milhar":
            texto = lambda_ate_999(self.milhar, self.lang)

            if self.lang == "pt":
                saida = "mil" if self.milhar == 1 else texto + " mil"
                self.log.append(f"Estado MILHAR -> {saida}")
            else:
                saida = texto + " thousand"
                self.log.append(f"THOUSAND STATE -> {saida}")

            self.output.append(saida)

            if self.resto > 0:
                self.state = "q_resto"
            else:
                self.state = "qf"

        elif self.state == "q_resto":
            texto = lambda_ate_999(self.resto, self.lang)

            if self.lang == "pt":
                self.log.append(f"Estado RESTO -> {texto}")
            else:
                self.log.append(f"REMAINDER STATE -> {texto}")

            self.output.append(texto)
            self.state = "qf"

        elif self.state == "qf":
            self.log.append("FINAL STATE" if self.lang == "en" else "Estado FINAL")

    def run(self):
        while self.state != "qf":
            self.step()

        self.step()  # registra estado final

        # montagem final (regra do português)
        if len(self.output) == 2 and self.lang == "pt":
            if self.resto < 100 or self.resto % 100 == 0:
                return self.output[0] + " e " + self.output[1], "\n".join(self.log)
            else:
                return self.output[0] + ", " + self.output[1], "\n".join(self.log)

        return " ".join(self.output), "\n".join(self.log)

# ===================== INTERFACE =====================

def converter():
    try:
        n = int(entry.get())
        lang = idioma.get()

        if n < 0 or n > 999999:
            raise ValueError

        fsm = MealyFSM(n, lang)
        resultado, log = fsm.run()

        resultado_label.config(text=resultado)
        passos_text.delete("1.0", tk.END)
        passos_text.insert(tk.END, log)

    except:
        messagebox.showerror(
            "Error" if idioma.get() == "en" else "Erro",
            "Invalid input!" if idioma.get() == "en" else "Entrada inválida!"
        )

# ===================== GUI =====================

root = tk.Tk()
root.title("FSM Mealy - Number to Words")
root.geometry("520x420")

idioma = tk.StringVar(value="pt")

frame = tk.Frame(root)
frame.pack()

tk.Radiobutton(frame, text="Português", variable=idioma, value="pt").pack(side="left")
tk.Radiobutton(frame, text="English", variable=idioma, value="en").pack(side="left")

tk.Label(root, text="Número / Number (0-999999):").pack()

entry = tk.Entry(root)
entry.pack()

tk.Button(root, text="Converter", command=converter).pack(pady=10)

resultado_label = tk.Label(root, fg="blue", wraplength=450)
resultado_label.pack()

tk.Label(root, text="FSM Log").pack()

passos_text = tk.Text(root, height=10, width=65)
passos_text.pack()

root.mainloop()