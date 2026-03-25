"""
Busca de Custo Uniforme (UCS).
Vídeo explicativo: https://www.youtube.com/watch?v=XyoucHYKYSE
"""

import heapq
import time

from model.actions import get_actions, apply_action, is_goal
from .common import SearchResult


def ucs(initial_state, goal_deliveries, goal_cleans, max_nodes=2000000):
    start = time.time()
    # counter é necessário para desempate na heapq, caso contrário 
    # pode ocorrer erro de comparação entre estados
    counter = 0 
    frontier = [(0, counter, initial_state, [])]
    visited = {}
    explored = 0
    generated = 1
    max_frontier = 1

    while frontier and explored < max_nodes:
        g, _, state, path = heapq.heappop(frontier)

        # Checa se já visitamos este estado com um custo menor ou igual
        if state in visited and visited[state] <= g:
            continue

        visited[state] = g
        explored += 1

        # Verifica se é estado objetivo, se sim, retorna resultado
        if is_goal(state, goal_deliveries, goal_cleans):
            elapsed = time.time() - start
            final_path = [(initial_state, None)] + [(s, a) for s, a, c in path]
            return SearchResult(final_path, g, explored, generated, elapsed, max_frontier)

        # Expande os sucessores, calculando o custo acumulado e adicionando à fronteira
        for action in get_actions(state):
            new_state, cost = apply_action(state, action)
            new_g = g + cost
            if new_state not in visited or visited[new_state] > new_g:
                generated += 1
                counter += 1
                # path + [(new_state, action, cost)] ao invés de append é necessário 
                # para manter o path original intacto para outros sucessores
                heapq.heappush(frontier, (new_g, counter, new_state, path + [(new_state, action, cost)]))
                max_frontier = max(max_frontier, len(frontier))

    # Se esgotar a fronteira ou atingir o limite de nós explorados, retorna falha
    elapsed = time.time() - start
    return SearchResult(None, float('inf'), explored, generated, elapsed, max_frontier)
