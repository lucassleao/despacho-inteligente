from despacho.cidade import CENTRO_PINHEIROS, gerar_cidade
from despacho.geo import distancia_km


def test_mesma_seed_gera_mesma_cidade():
    a = gerar_cidade(seed=7)
    b = gerar_cidade(seed=7)
    assert [p.pronto_em for p in a.pedidos] == [p.pronto_em for p in b.pedidos]


def test_seeds_diferentes_geram_cidades_diferentes():
    a = gerar_cidade(seed=1)
    b = gerar_cidade(seed=2)
    assert [p.pronto_em for p in a.pedidos] != [p.pronto_em for p in b.pedidos]


def test_quantidades_pedidas_sao_respeitadas():
    cidade = gerar_cidade(n_restaurantes=4, n_entregadores=3, n_pedidos=12)
    assert len(cidade.restaurantes) == 4
    assert len(cidade.entregadores) == 3
    assert len(cidade.pedidos) == 12


def test_restaurantes_ficam_dentro_do_raio():
    # 200 restaurantes: se a conversão km -> graus estiver errada, algum escapa do círculo
    cidade = gerar_cidade(n_restaurantes=200, raio_km=3.0)
    for r in cidade.restaurantes:
        assert distancia_km(CENTRO_PINHEIROS, r.local) <= 3.0 + 1e-6


def test_restaurantes_se_espalham_nas_duas_direcoes():
    # pega o bug de "achatar" a cidade: se a conversão de latitude estiver errada,
    # todos os pontos ficam numa linha horizontal e ninguém se afasta para norte/sul
    cidade = gerar_cidade(n_restaurantes=200, raio_km=3.0)
    km_norte_sul = [abs(r.local.latitude - CENTRO_PINHEIROS.latitude) * 111.32 for r in cidade.restaurantes]
    km_do_centro = [distancia_km(CENTRO_PINHEIROS, r.local) for r in cidade.restaurantes]
    assert max(km_norte_sul) > 2.0
    assert max(km_do_centro) > 2.0


def test_preparo_nunca_e_menor_que_5_minutos():
    # trava de sanidade: max(5.0, ...)
    cidade = gerar_cidade(n_pedidos=500)
    for p in cidade.pedidos:
        assert p.pronto_em - p.criado_em >= 5.0


def test_pedidos_estao_em_ordem_de_chegada():
    cidade = gerar_cidade(n_pedidos=100)
    horarios = [p.criado_em for p in cidade.pedidos]
    assert horarios == sorted(horarios)


def test_todos_os_entregadores_comecam_livres():
    assert all(e.livre for e in gerar_cidade().entregadores)
