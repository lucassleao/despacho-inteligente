from dataclasses import dataclass
from enum import Enum

from despacho.geo import Ponto


class StatusPedido(Enum):
    """Enumeração para representar o status de um pedido."""
    PREPARANDO = "Preparando"
    PRONTO = "Pronto"
    EM_ROTA = "Em Rota"
    ENTREGUE = "Entregue"


@dataclass
class Restaurante:
    """Classe que representa um restaurante."""
    id: int
    nome: str
    local: Ponto
    tempo_preparo_medio_min: float  # Tempo médio de preparo em minutos


@dataclass
class Pedido:
    """classe que representa um pedido de entrega."""
    id: int
    restaurante: Restaurante
    destino: Ponto
    criado_em: float  # Timestamp de criação do pedido
    pronto_em: float  # Timestamp de quando o pedido ficou pronto
    status: StatusPedido = StatusPedido.PREPARANDO  # Status inicial do pedido
    
    @property
    def atraso_preparo_min(self) -> float:
        """Quanto o preparo passou da média do restaurante. Negativo = adiantado."""
        esperado = self.criado_em + self.restaurante.tempo_preparo_medio_min
        return self.pronto_em - esperado


@dataclass
class Entregador:
    id: int
    nome: str
    posicao: Ponto
    pedido_atual: Pedido | None = None

    @property
    def livre(self) -> bool:
        return self.pedido_atual is None



    

