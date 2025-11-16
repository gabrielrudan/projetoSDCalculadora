<?php
// Calculadora remota via POST

header('Content-Type: application/json');

// =============================
// 1) CÁLCULO DE EXPRESSÃO COMPLETA
// =============================
if (isset($_POST['expr'])) {
    $expr = $_POST['expr'];

    // Permite apenas números, operadores e parênteses
    if (!preg_match('/^[0-9+\-.*() \/]+$/', $expr)) {
        echo json_encode(["erro" => "Expressão contém caracteres não permitidos"]);
        exit;
    }

    try {
        // Cálculo da expressão com segurança básica
        $resultado = eval("return ($expr);");
        echo json_encode(["resultado" => $resultado]);
    } catch (Throwable $e) {
        echo json_encode(["erro" => "Expressão inválida"]);
    }

    exit; // IMPORTANTE: encerra aqui, não deixa cair no resto do código
}

// =============================
// 2) CÁLCULO OPERACIONAL (soma, sub, mult, div)
// =============================

// Função para validar e converter valores
function getPostValue($key) {
    return isset($_POST[$key]) ? floatval($_POST[$key]) : null;
}

$oper1 = getPostValue('oper1');
$oper2 = getPostValue('oper2');
$operacao = isset($_POST['operacao']) ? intval($_POST['operacao']) : null;

$resultado = null;
$erro = null;

if ($oper1 === null || $oper2 === null || $operacao === null) {
    $erro = "Parâmetros inválidos. Envie 'oper1', 'oper2' e 'operacao' via POST.";
} else {
    switch ($operacao) {
        case 1: // Soma
            $resultado = $oper1 + $oper2;
            break;
        case 2: // Subtração
            $resultado = $oper1 - $oper2;
            break;
        case 3: // Multiplicação
            $resultado = $oper1 * $oper2;
            break;
        case 4: // Divisão
            if ($oper2 == 0) {
                $erro = "Erro: divisão por zero.";
            } else {
                $resultado = $oper1 / $oper2;
            }
            break;
        default:
            $erro = "Operação inválida. Use 1 (soma), 2 (subtração), 3 (multiplicação) ou 4 (divisão).";
    }
}

if ($erro) {
    echo json_encode(["erro" => $erro]);
} else {
    echo json_encode([
        "oper1" => $oper1,
        "oper2" => $oper2,
        "operacao" => $operacao,
        "resultado" => $resultado
    ]);
}

