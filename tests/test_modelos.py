from despacho.geo import Ponto
from despacho.modelos import Entregador, Pedido, Restaurante, StatusPedido

LOCAL = Ponto(latitude=-23.56, longitude=-46.68)


def criar_restaurante(tempo_medio: float = 15) -> Restaurante:
    return Restaurante(id=1, nome="Teste", local=LOCAL, tempo_preparo_medio_min=tempo_medio)


def criar_pedido(criado_em: float = 0, pronto_em: float = 15, tempo_medio: float = 15) -> Pedido:
    return Pedido(
        id=1,
        restaurante=criar_restaurante(tempo_medio),
        destino=LOCAL,
        criado_em=criado_em,
        pronto_em=pronto_em,
    )


def test_pedido_nasce_preparando():
    assert criar_pedido().status == StatusPedido.PREPARANDO


def test_atraso_positivo_quando_fica_pronto_depois_da_media():
    # esperado = 10 + 15 = 25; ficou pronto no 32 -> 7 min de atraso
    pedido = criar_pedido(criado_em=10, pronto_em=32, tempo_medio=15)
    assert pedido.atraso_preparo_min == 7


def test_atraso_negativo_quando_fica_pronto_antes_da_media():
    # esperado = 10 + 15 = 25; ficou pronto no 22 -> adiantou 3 min
    pedido = criar_pedido(criado_em=10, pronto_em=22, tempo_medio=15)
    assert pedido.atraso_preparo_min == -3


def test_entregador_fica_ocupado_ao_receber_pedido():
    ana = Entregador(id=1, nome="Ana", posicao=LOCAL)
    assert ana.livre

    ana.pedido_atual = criar_pedido()
    assert not ana.livre
