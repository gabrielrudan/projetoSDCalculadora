from ClientHTTPSCalculadoraPython import CalculadoraRest

calc = CalculadoraRest("http://localhost:8000/calculadora.php")

print(calc.soma(10, 5))
print(calc.subtracao(10, 5))
print(calc.multiplicacao(10, 5))
print(calc.divisao(10, 5))