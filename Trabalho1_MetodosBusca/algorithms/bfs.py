"""Busca em Largura (BFS)."""

import time
from collections import deque

from model.actions import get_actions, apply_action, is_goal
from .common import SearchResult


def bfs(initial_state, goal_deliveries, goal_cleans, max_nodes=500000):
    start = time.time()
    frontier = deque([(initial_state, [])])
    visited = {initial_state}
    explored = 0
    generated = 1
    max_frontier = 1

    while frontier and explored < max_nodes:
        state, path = frontier.popleft()
        explored += 1

        if is_goal(state, goal_deliveries, goal_cleans):
            elapsed = time.time() - start
            total_cost = sum(c for _, _, c in path)
            final_path = [(initial_state, None)] + [(s, a) for s, a, c in path]
            return SearchResult(final_path, total_cost, explored, generated, elapsed, max_frontier)

        for action in get_actions(state):
            new_state, cost = apply_action(state, action)
            if new_state not in visited:
                visited.add(new_state)
                generated += 1
                # path + [(new_state, action, cost)] ao invés de append é necessário 
                # para manter o path original intacto para outros sucessores
                frontier.append((new_state, path + [(new_state, action, cost)]))
                max_frontier = max(max_frontier, len(frontier))

    elapsed = time.time() - start
    return SearchResult(None, float('inf'), explored, generated, elapsed, max_frontier)
