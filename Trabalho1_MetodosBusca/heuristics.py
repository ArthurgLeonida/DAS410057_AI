"""Heurísticas para busca informada na cafeteria robótica."""

from model.constants import (
    DISTANCES, TABLE_AREA,
    COLD_DRINK_TIME, HOT_DRINK_TIME,
    WAITER_SPEED, CLEAN_TIME_PER_M2,
)


def heuristic_null(state, goal_deliveries, goal_cleans):
    """Heurística nula (h=0). Transforma A* em UCS."""
    return 0


def heuristic_simple(state, goal_deliveries, goal_cleans):
    """
    Heurística admissível simples:
    - Conta bebidas não entregues * tempo mínimo de preparo + entrega
    - Conta mesas sujas * tempo mínimo de limpeza
    """
    h = 0

    for dtype, table in state.pending_orders:
        prep = COLD_DRINK_TIME if dtype == "cold" else HOT_DRINK_TIME
        min_delivery = DISTANCES[("bar", table)] / WAITER_SPEED
        h += prep + min_delivery

    for dtype, table in state.drinks_ready:
        min_delivery = DISTANCES[("bar", table)] / WAITER_SPEED
        h += min_delivery

    for dtype, table in state.waiter_carrying:
        if state.waiter_pos != table:
            h += DISTANCES[(state.waiter_pos, table)] / WAITER_SPEED

    for table in state.dirty_tables:
        area = TABLE_AREA[table]
        h += CLEAN_TIME_PER_M2 * area

    return h


def heuristic_advanced(state, goal_deliveries, goal_cleans):
    """
    Heurística mais informada:
    Considera o tempo mínimo para completar todas as tarefas restantes,
    incluindo deslocamentos mínimos.
    """
    remaining_deliveries = set(goal_deliveries) - set(state.delivered)
    remaining_cleans = set(goal_cleans) - set(state.cleaned_tables)

    # Tempo mínimo do barista
    barista_remaining = 0
    for dtype, table in state.pending_orders:
        barista_remaining += COLD_DRINK_TIME if dtype == "cold" else HOT_DRINK_TIME

    # Tempo mínimo do garçom
    waiter_tasks_time = 0

    tables_to_visit = set()
    for dtype, table in state.drinks_ready:
        tables_to_visit.add(table)
    for dtype, table in state.waiter_carrying:
        if (dtype, table) in remaining_deliveries:
            tables_to_visit.add(table)
    for dtype, table in state.pending_orders:
        tables_to_visit.add(table)

    if tables_to_visit:
        min_table_dist = min(DISTANCES[("bar", t)] for t in tables_to_visit)
        waiter_tasks_time += min_table_dist / WAITER_SPEED

    # Limpeza: tempo de limpeza de todas as mesas + distância mínima até a mais próxima
    for table in remaining_cleans:
        area = TABLE_AREA[table]
        waiter_tasks_time += CLEAN_TIME_PER_M2 * area
    if remaining_cleans:
        min_clean_dist = min(DISTANCES[(state.waiter_pos, t)] for t in remaining_cleans)
        waiter_tasks_time += min_clean_dist / WAITER_SPEED

    return max(barista_remaining, waiter_tasks_time)
