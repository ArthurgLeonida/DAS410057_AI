"""Estado do problema da cafeteria robótica."""

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class State:
    """Estado imutável e hashable do problema."""
    # Barista
    barista_busy_until: int = 0
    drinks_ready: tuple = ()  # tupla de (tipo, mesa_destino) no balcão

    # Garçom
    waiter_pos: str = "bar"
    waiter_busy_until: int = 0
    waiter_carrying: tuple = ()   # bebidas na garra (max 1) ou bandeja (max 3)
    waiter_has_tray: bool = False

    # Pedidos pendentes (ainda não preparados)
    pending_orders: tuple = ()  # (tipo, mesa_destino)

    # Bebidas já entregues
    delivered: tuple = ()  # (tipo, mesa_destino)

    # Mesas que precisam ser limpas
    dirty_tables: tuple = ()

    # Mesas já limpas
    cleaned_tables: tuple = ()

    # Tempo global (para custo uniforme)
    time: int = 0
