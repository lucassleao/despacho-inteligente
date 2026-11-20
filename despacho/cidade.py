"""gera uma cidade falsa (restaurante, entregadores e pedidos) ao redor de um bairro real para testes."""
import math
import random
from dataclasses import dataclass


from despacho.geo import Ponto
from despacho.modelos import Entregador, Pedido, Restaurante


CENTRO_PINHEIROS = Ponto(latitude=-23.564, longitude=-46.653)  # Centro de Pinheiros, São Paulo
KM_POR_GRAU = 111.32  # Aproximação: 1 grau de latitude ~ 111.32 km


NOMES_RESTAURANTES = [
    "Burger do Zé", "Sushi Kenzo", "Pizzaria Bella", "Marmita da Vó", "Açaí Tropical",
    "Taco Loco", "Pastel da Feira", "Poke House", "Churrasquinho 10", "Padaria Real"
]
NOMES_ENTREGADORES = ["Ana", "Bruno", "Carla", "Diego", "Elisa", "Felipe", "Gabi", "Hugo"]


@dataclass
class CidadeFalsa:
    """Representa uma cidade falsa com restaurantes, entregadores e pedidos."""
    restaurantes: list[Restaurante]
    entregadores: list[Entregador]
    pedidos: list[Pedido]


def ponto_aleatorio(centro: Ponto, raio_km:float, rng: random.Random) -> Ponto:
    """sorteia um ponto aleatorio dentri de um circulo ao redor de 'centro',"""
    distancia = raio_km * math.sqrt(rng.random())  # sqrt para uniformidade na area
    angulo = rng.uniform(0, 2 * math.pi)
    dlat = distancia * math.cos(angulo) / KM_POR_GRAU
    dlon = distancia * math.sin(angulo) / (KM_POR_GRAU * math.cos(math.radians(centro.latitude)))
    return Ponto(latitude=centro.latitude + dlat, longitude=centro.longitude + dlon)




def gerar_cidade(
    n_restaurantes: int = 10,
    n_entregadores: int = 5,
    n_pedidos: int = 30,
    duracao_min: int = 120,
    raio_km: float = 3.0,
    seed: int = 42,
) -> CidadeFalsa:
    """Cria uma cidade reproduzível: a mesma seed sempre gera a mesma cidade."""
    rng = random.Random(seed)

    restaurantes = [
        Restaurante(
            id=i,
            nome=NOMES_RESTAURANTES[i % len(NOMES_RESTAURANTES)],
            local=ponto_aleatorio(CENTRO_PINHEIROS, raio_km, rng),
            tempo_preparo_medio_min=rng.uniform(10, 25),
        )
        for i in range(n_restaurantes)
    ]

    entregadores = [
        Entregador(
            id=i,
            nome=NOMES_ENTREGADORES[i % len(NOMES_ENTREGADORES)],
            posicao=ponto_aleatorio(CENTRO_PINHEIROS, raio_km, rng),
        )
        for i in range(n_entregadores)
    ]


    pedidos = []
    for i in range(n_pedidos):
        restaurante = rng.choice(restaurantes)
        criado_em = rng.uniform(0, duracao_min)

        if rng.random() < 0.25:
            atraso = rng.uniform(8, 25)
        else:
            atraso = rng.gauss(0, 3)

        preparo = max(5.0, restaurante.tempo_preparo_medio_min + atraso)

        pedidos.append(
            Pedido(
                id=i,
                restaurante=restaurante,
                destino=ponto_aleatorio(restaurante.local, 2.5, rng),
                criado_em=criado_em,
                pronto_em=criado_em + preparo,
            )
        )

    pedidos.sort(key=lambda p: p.criado_em)

    return CidadeFalsa(restaurantes, entregadores, pedidos)
