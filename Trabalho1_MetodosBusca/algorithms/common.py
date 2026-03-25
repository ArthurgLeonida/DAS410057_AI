"""Estruturas comuns aos algoritmos de busca."""

from model.actions import format_action


class SearchResult:
    def __init__(self, path, cost, nodes_explored, nodes_generated, exec_time, max_frontier):
        self.path = path
        self.cost = cost
        self.nodes_explored = nodes_explored
        self.nodes_generated = nodes_generated
        self.exec_time = exec_time
        self.max_frontier = max_frontier

    def __str__(self):
        if not self.path:
            return "Nenhuma solução encontrada!"
        lines = [
            f"Custo total: {self.cost}",
            f"Passos: {len(self.path) - 1}",
            f"Nós explorados: {self.nodes_explored}",
            f"Nós gerados: {self.nodes_generated}",
            f"Tamanho máximo da fronteira: {self.max_frontier}",
            f"Tempo de execução: {self.exec_time:.4f}s",
            "",
            "Plano de ações:",
        ]
        for i, (state, action) in enumerate(self.path):
            if action:
                lines.append(f"  t={state.time}: {format_action(action)}")
        return "\n".join(lines)
