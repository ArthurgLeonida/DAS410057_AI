"""
Trabalho Prático 1 - Busca em Espaço de Estados
Cafeteria Robótica - Disciplina de Inteligência Artificial
Prof. Jomi F. Hübner
Alunos: Arthur Gislon Leonida, Ana Carolina de Moraes Dias

Implementação dos algoritmos de busca: BFS, DFS, UCS, Greedy, A*
"""

from algorithms import bfs, dfs, ucs, greedy, astar
from heuristics import heuristic_simple, heuristic_advanced
from problems import create_problem_1, create_problem_2, create_problem_3, create_problem_4


def run_experiments():
    problems = [create_problem_1, create_problem_2, create_problem_3, create_problem_4]
    algorithms = {
        "BFS": lambda s, gd, gc: bfs(s, gd, gc, max_nodes=500000),
        "DFS": lambda s, gd, gc: dfs(s, gd, gc, max_depth=50, max_nodes=500000),
        "UCS": lambda s, gd, gc: ucs(s, gd, gc, max_nodes=500000),
        "Greedy (h_simple)": lambda s, gd, gc: greedy(s, gd, gc, heuristic_simple, max_nodes=500000),
        "Greedy (h_advanced)": lambda s, gd, gc: greedy(s, gd, gc, heuristic_advanced, max_nodes=500000),
        "A* (h_simple)": lambda s, gd, gc: astar(s, gd, gc, heuristic_simple, max_nodes=500000),
        "A* (h_advanced)": lambda s, gd, gc: astar(s, gd, gc, heuristic_advanced, max_nodes=500000),
    }

    results = {}

    for prob_fn in problems:
        state, goal_del, goal_cl, name = prob_fn()
        print(f"\n{'='*60}")
        print(f"  {name}")
        print(f"  Pedidos: {state.pending_orders}")
        print(f"  Mesas sujas: {state.dirty_tables}")
        print(f"{'='*60}")

        results[name] = {}

        for alg_name, alg_fn in algorithms.items():
            print(f"\n  --- {alg_name} ---")
            try:
                result = alg_fn(state, goal_del, goal_cl)
                results[name][alg_name] = result
                print(f"  {result}")
            except Exception as e:
                print(f"  ERRO: {e}")
                results[name][alg_name] = None

    # Tabela resumo
    print("\n\n" + "="*100)
    print("TABELA RESUMO")
    print("="*100)
    header = f"{'Problema':<15} {'Algoritmo':<25} {'Custo':<10} {'Explorados':<12} {'Gerados':<12} {'Fronteira':<12} {'Tempo(s)':<10}"
    print(header)
    print("-"*100)

    for prob_name in results:
        for alg_name in results[prob_name]:
            r = results[prob_name][alg_name]
            if r and r.path:
                print(f"{prob_name:<15} {alg_name:<25} {r.cost:<10} {r.nodes_explored:<12} "
                      f"{r.nodes_generated:<12} {r.max_frontier:<12} {r.exec_time:<10.4f}")
            else:
                print(f"{prob_name:<15} {alg_name:<25} {'N/A':<10} {'N/A':<12} "
                      f"{'N/A':<12} {'N/A':<12} {'N/A':<10}")

    return results


if __name__ == "__main__":
    run_experiments()
