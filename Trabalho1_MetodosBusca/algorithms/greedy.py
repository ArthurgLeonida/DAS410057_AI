"""
Busca Gulosa (Greedy Best-First Search).
Vídeo explicativo: https://www.youtube.com/watch?v=dv1m3L6QXWs
"""

import heapq
import time

from model.actions import get_actions, apply_action, is_goal
from .common import SearchResult


def greedy(initial_state, goal_deliveries, goal_cleans, heuristic, max_nodes=2000000):
    start = time.time()
    counter = 0
    h0 = heuristic(initial_state, goal_deliveries, goal_cleans)
    frontier = [(h0, counter, initial_state, [], 0)]
    visited = set()
    explored = 0
    generated = 1
    max_frontier = 1

    while frontier and explored < max_nodes:
        _, _, state, path, g = heapq.heappop(frontier)

        if state in visited:
            continue
        visited.add(state)
        explored += 1

        if is_goal(state, goal_deliveries, goal_cleans):
            elapsed = time.time() - start
            final_path = [(initial_state, None)] + [(s, a) for s, a, c in path]
            return SearchResult(final_path, g, explored, generated, elapsed, max_frontier)

        for action in get_actions(state):
            new_state, cost = apply_action(state, action)
            if new_state not in visited:
                generated += 1
                counter += 1
                h = heuristic(new_state, goal_deliveries, goal_cleans)
                new_g = g + cost
                # path + [(new_state, action, cost)] ao invés de append é necessário 
                # para manter o path original intacto para outros sucessores
                heapq.heappush(frontier, (h, counter, new_state, path + [(new_state, action, cost)], new_g))
                max_frontier = max(max_frontier, len(frontier))

    elapsed = time.time() - start
    return SearchResult(None, float('inf'), explored, generated, elapsed, max_frontier)
