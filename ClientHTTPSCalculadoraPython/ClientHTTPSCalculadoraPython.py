import time
import requests
import ast

class CalculadoraRest:
    def __init__(self, base_url):
        # base_url deve apontar para o endpoint PHP completo, ex:
        # "http://localhost:8000/calculadora.php"
        self.base_url = base_url
        self.max_retries = 3       # número de tentativas
        self.retry_wait = 1.0      # segundos entre tentativas

    def _enviar(self, oper1, oper2, operacao):
        payload = {
            "oper1": oper1,
            "oper2": oper2,
            "operacao": operacao
        }

        tentativas = 0
        while tentativas < self.max_retries:
            try:
                response = requests.post(self.base_url, data=payload, timeout=5)

                if response.status_code == 200:
                    data = response.json()
                    if "resultado" in data:
                        return data.get("resultado")
                    else:
                        return f"Erro servidor: {data.get('erro')}"
                else:
                    return f"Erro HTTP: {response.status_code}"

            except requests.exceptions.RequestException as e:
                tentativas += 1
                if tentativas >= self.max_retries:
                    return f"Erro de conexão após {self.max_retries} tentativas: {e}"
                time.sleep(self.retry_wait)

    # wrappers simples
    def soma(self, a, b):
        return self._enviar(a, b, 1)

    def subtracao(self, a, b):
        return self._enviar(a, b, 2)

    def multiplicacao(self, a, b):
        return self._enviar(a, b, 3)

    def divisao(self, a, b):
        return self._enviar(a, b, 4)

    # -------------------------
    # Enviar expressão inteira ao servidor (1 requisição)
    # -------------------------
    def calcular_expressao_servidor(self, expr):
        tentativas = 0
        while tentativas < self.max_retries:
            try:
                response = requests.post(self.base_url, data={"expr": expr}, timeout=7)

                if response.status_code == 200:
                    data = response.json()
                    if "resultado" in data:
                        return data.get("resultado")
                    else:
                        return f"Erro servidor: {data.get('erro')}"
                else:
                    return f"Erro HTTP: {response.status_code}"

            except requests.exceptions.RequestException as e:
                tentativas += 1
                if tentativas >= self.max_retries:
                    return f"Erro de conexão após {self.max_retries} tentativas: {e}"
                time.sleep(self.retry_wait)

    # -------------------------
    # Avaliar expressão no cliente, decompondo e chamando operações remotas (_enviar)
    # Usa ast para parse seguro e faz chamadas recursivas.
    # -------------------------
    def calcular_expressao_cliente(self, expr):
        """
        Recebe uma string expr (ex: "(10 + 15) * 4").
        Faz parse com ast e avalia recursivamente. Para cada operação binária
        faz uma chamada remota via _enviar.
        Retorna número (int/float) ou string com mensagem de erro.
        """
        # limpar espaços desnecessários
        expr_clean = expr.strip()

        try:
            tree = ast.parse(expr_clean, mode="eval")
        except Exception as e:
            return f"Erro: expressão inválida ({e})"

        try:
            return self._eval_node(tree.body)
        except Exception as e:
            return f"Erro ao avaliar expressão: {e}"

    def _eval_node(self, node):
        """
        Avalia um nó AST e, quando encontra uma operação binária, 
        avalia operands recursivamente e chama _enviar para executar a operação.
        Suporta ast.BinOp com Add, Sub, Mult, Div; ast.UnaryOp (+/-); ast.Constant/Num.
        """
        # números constantes
        if isinstance(node, ast.Constant):  # Python 3.8+
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Constante não numérica")
        if isinstance(node, ast.Num):  # compatibilidade antiga
            return node.n

        # operações unárias: + / -
        if isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise ValueError("Operador unário não suportado")

        # operações binárias
        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)

            # garantir que left/right sejam números (se retornaram string de erro, propagar)
            if isinstance(left, str) and not isinstance(left, (int, float)):
                raise ValueError(left)
            if isinstance(right, str) and not isinstance(right, (int, float)):
                raise ValueError(right)

            # Mapear operador para _enviar
            op = node.op
            if isinstance(op, ast.Add):
                res = self._enviar(left, right, 1)
            elif isinstance(op, ast.Sub):
                res = self._enviar(left, right, 2)
            elif isinstance(op, ast.Mult):
                res = self._enviar(left, right, 3)
            elif isinstance(op, ast.Div):
                # poderíamos checar divisão por zero localmente, mas delegamos ao servidor
                res = self._enviar(left, right, 4)
            else:
                raise ValueError("Operador binário não suportado")

            # _enviar pode devolver número ou string de erro
            # se for string contendo 'Erro', lançar para propagar
            if isinstance(res, (int, float)):
                return res
            # tenta converter para float caso venha string numérica
            try:
                return float(res)
            except Exception:
                raise ValueError(res)

        # parênteses já virão como BinOp/Constant por AST; caso contrário, erro
        raise ValueError("Tipo de nó não suportado na expressão")
