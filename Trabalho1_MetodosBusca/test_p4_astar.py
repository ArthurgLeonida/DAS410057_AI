"""
Test file: Run only Problem 4 with A* algorithms, increasing max_nodes
to investigate why Greedy finds a solution but A* does not.
"""

from algorithms import astar, greedy
from heuristics import heuristic_simple, heuristic_advanced
from problems import create_problem_4


def run():
    state, goal_del, goal_cl, name = create_problem_4()

    print(f"{'='*60}")
    print(f"  {name}")
    print(f"  Pedidos: {state.pending_orders}")
    print(f"  Mesas sujas: {state.dirty_tables}")
    print(f"{'='*60}")

    # First, run Greedy as baseline
    print("\n--- Greedy (h_simple) - baseline ---")
    r = greedy(state, goal_del, goal_cl, heuristic_simple, max_nodes=500000)
    print(f"  {r}")

    print("\n--- Greedy (h_advanced) - baseline ---")
    r = greedy(state, goal_del, goal_cl, heuristic_advanced, max_nodes=500000)
    print(f"  {r}")

    # Now test A* with increasing max_nodes
    limits = [3_000_000, 5_000_000]

    for max_n in limits:
        label = f"{max_n:,}"
        print(f"\n{'='*60}")
        print(f"  A* tests with max_nodes = {label}")
        print(f"{'='*60}")

        for h_name, h_fn in [("h_simple", heuristic_simple), ("h_advanced", heuristic_advanced)]:
            print(f"\n  --- A* ({h_name}) | max_nodes={label} ---")
            r = astar(state, goal_del, goal_cl, h_fn, max_nodes=max_n)
            print(f"  {r}")
            if r.path:
                print(f"  >>> SOLUTION FOUND with {h_name}! Cost={r.cost}")
                break
        else:
            continue
        break  # stop escalating if both heuristics found solution


if __name__ == "__main__":
    run()
