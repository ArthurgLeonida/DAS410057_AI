"""Constantes do problema da cafeteria robótica."""

# Distâncias entre locais (bar e mesas 1-4)
DISTANCES = {
    ("bar", "mesa1"): 2, ("bar", "mesa2"): 2,
    ("bar", "mesa3"): 3, ("bar", "mesa4"): 3,
    ("mesa1", "mesa2"): 1, ("mesa1", "mesa3"): 1,
    ("mesa1", "mesa4"): 1, ("mesa2", "mesa3"): 1,
    ("mesa2", "mesa4"): 1, ("mesa3", "mesa4"): 1,
}

# Tornar simétrico
for (a, b), d in list(DISTANCES.items()):
    DISTANCES[(b, a)] = d
for loc in ["bar", "mesa1", "mesa2", "mesa3", "mesa4"]:
    DISTANCES[(loc, loc)] = 0

# Área das mesas (m²)
TABLE_AREA = {"mesa1": 1, "mesa2": 1, "mesa3": 2, "mesa4": 1}

# Tempos
COLD_DRINK_TIME = 3
HOT_DRINK_TIME = 5
WAITER_SPEED = 2          # m por unidade de tempo (sem bandeja)
WAITER_SPEED_TRAY = 1     # m por unidade de tempo (com bandeja)
CLEAN_TIME_PER_M2 = 2     # unidades de tempo por m²
