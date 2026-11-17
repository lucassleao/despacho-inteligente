"""geografia:pontos no mapa, distancia e tempo de viagem."""
import math
from dataclasses import dataclass


RAIO_TERRA_KM = 6371.0  # Raio médio da Terra em quilômetros
VELOCIDADE_MEDIA_KMH = 20.0  # Velocidade média em km/h


@dataclass(frozen=True)
class Ponto:
    """Representa um ponto geográfico com latitude e longitude."""
    latitude: float
    longitude: float


def distancia_km(a: Ponto, b: Ponto) -> float:
    """calcular a distanciaentre dois pontos ou seja loja e destinio(formula de haversine)"""
    lat1, lon1, lat2, lon2 = map(math.radians, [a.latitude, a.longitude, b.latitude, b.longitude])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    haversine = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * RAIO_TERRA_KM * math.asin(math.sqrt(haversine))


def tempo_viagem_min(a: Ponto, b: Ponto, velocidade_kmh: float = VELOCIDADE_MEDIA_KMH) -> float:
    """calcular o tempo de viagem entre dois pontos em minutos."""
    FATOR_TORTUOSIDADE = 1.3  # Fator de correção para estradas sinuosas
    km = distancia_km(a, b) * FATOR_TORTUOSIDADE
    return km / velocidade_kmh * 60  # Convertendo horas para minutos
    
    