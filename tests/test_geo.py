import pytest

from despacho.geo import Ponto, distancia_km, tempo_viagem_min


PRACA_DA_SE = Ponto(latitude=-23.5505, longitude=-46.6333)  # São Paulo
CRISTO_REDENTOR = Ponto(latitude=-22.9519, longitude=-43.2105)  # Rio de Janeiro


def test_distancia_de_um_ponto_para_ele_mesmo_deve_ser_zero():
    assert distancia_km(PRACA_DA_SE, PRACA_DA_SE) == 0.0


def test_distancia_e_simetrica():
    ida = distancia_km(PRACA_DA_SE, CRISTO_REDENTOR)
    volta = distancia_km(CRISTO_REDENTOR, PRACA_DA_SE)
    assert ida == pytest.approx(volta)  # Comparação com tolerância relativa


def test_distancia_entre_sao_paulo_e_rio_deve_ser_aproximadamente_360_km():
    assert 350 <= distancia_km(PRACA_DA_SE, CRISTO_REDENTOR) <= 370


def test_tempo_de_viagem_usa_velocidade_e_tortuosidade():
    esperado = distancia_km(PRACA_DA_SE, CRISTO_REDENTOR) * 1.3 / 20 * 60
    assert tempo_viagem_min(PRACA_DA_SE, CRISTO_REDENTOR) == pytest.approx(esperado)
