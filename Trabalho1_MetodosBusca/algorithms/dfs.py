"""Busca em Profundidade (DFS) com limite de profundidade."""

import time

from model.actions import get_actions, apply_action, is_goal
from .common import SearchResult


def dfs(initial_state, goal_deliveries, goal_cleans, max_depth=50, max_nodes=500000):
    start = time.time()
    frontier = [(initial_state, [], 0)]
    visited = set()
    explored = 0
    generated = 1
    max_frontier = 1

    while frontier and explored < max_nodes:
        state, path, depth = frontier.pop()

        if state in visited:
            continue
        visited.add(state)
        explored += 1

        if is_goal(state, goal_deliveries, goal_cleans):
            elapsed = time.time() - start
            total_cost = sum(c for _, _, c in path)
            final_path = [(initial_state, None)] + [(s, a) for s, a, c in path]
            return SearchResult(final_path, total_cost, explored, generated, elapsed, max_frontier)

        if depth < max_depth:
            for action in get_actions(state):
                new_state, cost = apply_action(state, action)
                if new_state not in visited:
                    generated += 1
                    # path + [(new_state, action, cost)] ao invés de append é necessário 
                    # para manter o path original intacto para outros sucessores
                    frontier.append((new_state, path + [(new_state, action, cost)], depth + 1))
                    max_frontier = max(max_frontier, len(frontier))

    elapsed = time.time() - start
    return SearchResult(None, float('inf'), explored, generated, elapsed, max_frontier)
