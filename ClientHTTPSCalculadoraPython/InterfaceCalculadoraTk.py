import tkinter as tk
from ClientHTTPSCalculadoraPython import CalculadoraRest

def criar_interface():
    calc = CalculadoraRest("http://localhost:8000/calculadora.php")

    janela = tk.Tk()
    janela.title("Calculadora HTTPS")
    janela.resizable(False, False)

    # ===============================
    # DISPLAY
    # ===============================
    display = tk.Entry(janela, font=("Arial", 20), borderwidth=5, relief="ridge", justify="right")
    display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, ipadx=10, ipady=10)

    # ===============================
    # FUNÇÕES INTERNAS
    # ===============================
    def clicar_texto(txt):
        atual = display.get()
        display.delete(0, tk.END)
        display.insert(0, atual + str(txt))

    def limpar():
        display.delete(0, tk.END)

    def calcular_servidor():
        expr = display.get().strip()
        if expr == "":
            return
        resultado = calc.calcular_expressao_servidor(expr)
        display.delete(0, tk.END)
        display.insert(0, str(resultado))

    def calcular_cliente():
        expr = display.get().strip()
        if expr == "":
            return
        resultado = calc.calcular_expressao_cliente(expr)
        display.delete(0, tk.END)
        display.insert(0, str(resultado))

    # ===============================
    # BOTÕES DA CALCULADORA (inclui parênteses)
    # ===============================
    botoes = [
        ("(", lambda: clicar_texto("(")), (")", lambda: clicar_texto(")")), ("C", limpar), ("/", lambda: clicar_texto("/")),
        ("7", lambda: clicar_texto("7")), ("8", lambda: clicar_texto("8")), ("9", lambda: clicar_texto("9")), ("*", lambda: clicar_texto("*")),
        ("4", lambda: clicar_texto("4")), ("5", lambda: clicar_texto("5")), ("6", lambda: clicar_texto("6")), ("-", lambda: clicar_texto("-")),
        ("1", lambda: clicar_texto("1")), ("2", lambda: clicar_texto("2")), ("3", lambda: clicar_texto("3")), ("+", lambda: clicar_texto("+")),
        ("0", lambda: clicar_texto("0")), (".", lambda: clicar_texto(".")), ("=", calcular_servidor), ("", None)
    ]

    # Posicionar botões com grid
    linha = 1
    coluna = 0
    for texto, comando in botoes:
        if texto == "":
            coluna += 1
            if coluna > 3:
                coluna = 0
                linha += 1
            continue
        tk.Button(janela, text=texto, width=5, height=2, font=("Arial", 14), command=comando).grid(row=linha, column=coluna, padx=5, pady=5)
        coluna += 1
        if coluna > 3:
            coluna = 0
            linha += 1

    # ===============================
    # BOTÕES EXTRA: Calcular Cliente / Calcular Servidor
    # ===============================
    tk.Button(janela, text="Calcular (Cliente)", width=18, height=2, font=("Arial", 12), command=calcular_cliente).grid(row=6, column=0, columnspan=2, padx=5, pady=8)
    tk.Button(janela, text="Calcular (Servidor)", width=18, height=2, font=("Arial", 12), command=calcular_servidor).grid(row=6, column=2, columnspan=2, padx=5, pady=8)

    janela.mainloop()

if __name__ == "__main__":
    criar_interface()

