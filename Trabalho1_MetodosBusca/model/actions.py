"""Ações e transições de estado da cafeteria robótica."""

from .state import State
from .constants import (
    DISTANCES, TABLE_AREA,
    COLD_DRINK_TIME, HOT_DRINK_TIME,
    WAITER_SPEED, WAITER_SPEED_TRAY, CLEAN_TIME_PER_M2,
)


def get_actions(state: State):
    """Gera todas as ações possíveis a partir de um estado."""
    actions = []
    t = state.time

    # ------------------#
    # AÇÕES DO BARISTA  #
    # ------------------#
    if state.barista_busy_until <= t and state.pending_orders:
        for i, (drink_type, table) in enumerate(state.pending_orders):
            actions.append(("barista_prepare", drink_type, table, i))

    # -----------------#
    # AÇÕES DO GARÇOM  #
    # -----------------#
    if state.waiter_busy_until <= t:

        # 1 -> Pegar bandeja no bar (se não tem bandeja e está no bar e não carrega nada)
        if not state.waiter_has_tray and state.waiter_pos == "bar" and len(state.waiter_carrying) == 0:
            if state.drinks_ready:  # só pega bandeja se há bebidas para carregar
                actions.append(("waiter_pick_tray",))

        # 2 -> Devolver bandeja no bar (se tem bandeja, está no bar e bandeja vazia)
        if state.waiter_has_tray and state.waiter_pos == "bar" and len(state.waiter_carrying) == 0:
            actions.append(("waiter_return_tray",))

        # 3 -> Pegar bebida do balcão (se está no bar)
        if state.waiter_pos == "bar" and state.drinks_ready:
            if state.waiter_has_tray:
                if len(state.waiter_carrying) < 3:
                    for i, drink in enumerate(state.drinks_ready):
                        actions.append(("waiter_pick_drink", i))
            else:
                if len(state.waiter_carrying) == 0:
                    for i, drink in enumerate(state.drinks_ready):
                        actions.append(("waiter_pick_drink", i))

        # 4 -> Entregar bebida na mesa atual
        if state.waiter_carrying:
            for i, (dtype, dest) in enumerate(state.waiter_carrying):
                if state.waiter_pos == dest:
                    actions.append(("waiter_deliver", i))

        # 5 -> Mover para outro local
        for target in ["bar", "mesa1", "mesa2", "mesa3", "mesa4"]:
            if target != state.waiter_pos:
                actions.append(("waiter_move", target))

        # 6 -> Limpar mesa (se está na mesa, mesa está suja, sem bandeja)
        if not state.waiter_has_tray and state.waiter_pos in state.dirty_tables:
            actions.append(("waiter_clean", state.waiter_pos))

    # 7 -> Esperar (avanço de tempo quando ambos estão ocupados)
    next_free = min(
        state.barista_busy_until if state.barista_busy_until > t else t,
        state.waiter_busy_until if state.waiter_busy_until > t else t
    )
    if next_free > t:
        actions.append(("wait", next_free))
    elif not actions:
        actions.append(("wait", t + 1))

    return actions


def apply_action(state: State, action):
    """Aplica uma ação e retorna (novo_estado, custo)."""
    t = state.time

    s = {
        "barista_busy_until": state.barista_busy_until,
        "drinks_ready": list(state.drinks_ready),
        "waiter_pos": state.waiter_pos,
        "waiter_busy_until": state.waiter_busy_until,
        "waiter_carrying": list(state.waiter_carrying),
        "waiter_has_tray": state.waiter_has_tray,
        "pending_orders": list(state.pending_orders),
        "delivered": list(state.delivered),
        "dirty_tables": list(state.dirty_tables),
        "cleaned_tables": list(state.cleaned_tables),
        "time": t,
    }

    cost = 0
    act = action[0]

    if act == "barista_prepare":
        _, drink_type, table, idx = action
        prep_time = COLD_DRINK_TIME if drink_type == "cold" else HOT_DRINK_TIME
        s["barista_busy_until"] = t + prep_time
        s["pending_orders"].pop(idx)
        s["drinks_ready"].append((drink_type, table))
        cost = prep_time

    elif act == "waiter_pick_tray":
        s["waiter_has_tray"] = True

    elif act == "waiter_return_tray":
        s["waiter_has_tray"] = False

    elif act == "waiter_pick_drink":
        _, idx = action
        drink = s["drinks_ready"].pop(idx)
        s["waiter_carrying"].append(drink)

    elif act == "waiter_deliver":
        _, idx = action
        drink = s["waiter_carrying"].pop(idx)
        s["delivered"].append(drink)

    elif act == "waiter_move":
        _, target = action
        dist = DISTANCES[(s["waiter_pos"], target)]
        speed = WAITER_SPEED_TRAY if s["waiter_has_tray"] else WAITER_SPEED
        move_time = dist / speed
        move_time = int(move_time) if move_time == int(move_time) else int(move_time) + 1
        s["waiter_busy_until"] = t + move_time
        s["waiter_pos"] = target
        cost = move_time

    elif act == "waiter_clean":
        _, table = action
        area = TABLE_AREA[table]
        clean_time = CLEAN_TIME_PER_M2 * area
        s["waiter_busy_until"] = t + clean_time
        s["dirty_tables"].remove(table)
        s["cleaned_tables"].append(table)
        cost = clean_time

    elif act == "wait":
        _, new_time = action
        cost = new_time - t
        s["time"] = new_time

    s["time"] = max(s["time"], s.get("waiter_busy_until", 0), t)

    for k in ["drinks_ready", "waiter_carrying", "pending_orders", "delivered", "dirty_tables", "cleaned_tables"]:
        s[k] = tuple(sorted(s[k]))

    return State(**s), cost


def is_goal(state: State, goal_deliveries, goal_cleans):
    """Verifica se o estado é um estado objetivo."""
    # Verificar entregas contando duplicatas corretamente
    remaining = list(state.delivered)
    for d in goal_deliveries:
        if d in remaining:
            remaining.remove(d)
        else:
            return False
    # Verificar mesas limpas
    for t in goal_cleans:
        if t not in state.cleaned_tables:
            return False
    if state.waiter_has_tray or state.waiter_carrying:
        return False
    return True


def format_action(action):
    """Formata uma ação para exibição legível."""
    act = action[0]
    if act == "barista_prepare":
        return f"Barista prepara bebida {action[1]} para {action[2]}"
    elif act == "waiter_pick_tray":
        return "Garçom pega bandeja"
    elif act == "waiter_return_tray":
        return "Garçom devolve bandeja"
    elif act == "waiter_pick_drink":
        return "Garçom pega bebida do balcão"
    elif act == "waiter_deliver":
        return "Garçom entrega bebida"
    elif act == "waiter_move":
        return f"Garçom move para {action[1]}"
    elif act == "waiter_clean":
        return f"Garçom limpa {action[1]}"
    elif act == "wait":
        return f"Espera até t={action[1]}"
    return str(action)
