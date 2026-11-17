# Responsável: Mateus Zanatta
# Regra 2: calcular o desconto do pedido
import pytest

from src.regras_localeats import calcular_desconto


# TU01 - comportamento esperado: pedido acima de R$ 100,00 recebe 10%
def test_pedido_de_150_reais_recebe_desconto_de_15():
    resultado = calcular_desconto(150)
    assert resultado == 15


# TU02 - situação alternativa: pedido abaixo de R$ 100,00 não recebe desconto
def test_pedido_abaixo_de_100_reais_nao_recebe_desconto():
    resultado = calcular_desconto(80)
    assert resultado == 0


# TU03 - casos de borda: valores em volta do limite de R$ 100,00 e o zero.
# pytest.approx é usado porque 100.01 * 0.10 resulta em 10.001000000000001
# (imprecisão normal de números decimais no computador).
@pytest.mark.parametrize(
    "valor_pedido, desconto_esperado",
    [
        (0, 0),
        (99.99, 0),
        (100, 10),
        (100.01, 10.001),
    ],
)
def test_desconto_nos_limites_da_regra(valor_pedido, desconto_esperado):
    resultado = calcular_desconto(valor_pedido)
    assert resultado == pytest.approx(desconto_esperado)


# TU04 - comportamento inválido: valor negativo gera ValueError
def test_valor_negativo_gera_value_error():
    with pytest.raises(ValueError, match="não pode ser negativo"):
        calcular_desconto(-10)
