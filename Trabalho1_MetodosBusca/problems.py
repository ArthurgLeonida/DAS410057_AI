"""Instâncias do problema da cafeteria robótica."""

from model.state import State


def create_problem_1():
    """Problema 1: 2 clientes mesa 2 (2 frias). Limpar mesas 3 e 4."""
    orders = [("cold", "mesa2"), ("cold", "mesa2")]
    dirty = ["mesa3", "mesa4"]
    state = State(
        pending_orders=tuple(orders),
        dirty_tables=tuple(dirty),
    )
    return state, orders[:], ["mesa3", "mesa4"], "Problema 1"


def create_problem_2():
    """Problema 2: 4 clientes mesa 3 (2 frias, 2 quentes). Limpar mesa 1."""
    orders = [("cold", "mesa3"), ("cold", "mesa3"),
              ("hot", "mesa3"), ("hot", "mesa3")]
    dirty = ["mesa1"]
    state = State(
        pending_orders=tuple(orders),
        dirty_tables=tuple(dirty),
    )
    return state, orders[:], ["mesa1"], "Problema 2"


def create_problem_3():
    """Problema 3: 2 clientes mesa 4 (2 quentes), 2 clientes mesa 1 (2 quentes). Limpar mesa 3."""
    orders = [("hot", "mesa4"), ("hot", "mesa4"),
              ("hot", "mesa1"), ("hot", "mesa1")]
    dirty = ["mesa3"]
    state = State(
        pending_orders=tuple(orders),
        dirty_tables=tuple(dirty),
    )
    return state, orders[:], ["mesa3"], "Problema 3"


def create_problem_4():
    """Problema 4: 2 mesa 4 + 2 mesa 1 (frias), 4 mesa 3 (quentes). Limpar mesa 2."""
    orders = [("cold", "mesa4"), ("cold", "mesa4"),
              ("cold", "mesa1"), ("cold", "mesa1"),
              ("hot", "mesa3"), ("hot", "mesa3"),
              ("hot", "mesa3"), ("hot", "mesa3")]
    dirty = ["mesa2"]
    state = State(
        pending_orders=tuple(orders),
        dirty_tables=tuple(dirty),
    )
    return state, orders[:], ["mesa2"], "Problema 4"
