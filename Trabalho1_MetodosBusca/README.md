# Trabalho 1 - Metodos de Busca

Implementacao de algoritmos de busca em espaco de estados para o planejamento de acoes de dois robos em uma cafeteria: um **barista** (prepara bebidas) e um **garcom** (entrega bebidas e limpa mesas).

## O Problema

A cafeteria possui um balcao (bar) e 4 mesas. O objetivo e entregar todas as bebidas pedidas e limpar as mesas sujas, minimizando o custo total. As restricoes incluem:

- **Bebidas frias**: 3 u.t. de preparo | **Bebidas quentes**: 5 u.t. de preparo
- **Garcom sem bandeja**: velocidade 2 m/u.t., carrega 1 bebida
- **Garcom com bandeja**: velocidade 1 m/u.t., carrega ate 3 bebidas
- Limpeza de mesas: 2 u.t. por m² (somente sem bandeja)

### Instancias

| Problema | Pedidos | Mesas sujas |
|----------|---------|-------------|
| 1 | 2 frias (mesa 2) | Mesas 3 e 4 |
| 2 | 2 frias + 2 quentes (mesa 3) | Mesa 1 |
| 3 | 2 quentes (mesa 4) + 2 quentes (mesa 1) | Mesa 3 |
| 4 | 2 frias (mesa 4) + 2 frias (mesa 1) + 4 quentes (mesa 3) | Mesa 2 |

## Algoritmos Implementados

- **BFS** - Busca em Largura
- **DFS** - Busca em Profundidade (com limite de profundidade)
- **UCS** - Busca de Custo Uniforme
- **Greedy** - Busca Gulosa (Best-First)
- **A\*** - com duas heuristicas admissiveis

### Heuristicas

- **h1 (simples)**: soma das estimativas individuais por tarefa (preparo + entrega + limpeza)
- **h2 (avancada)**: maximo entre o tempo restante do barista e do garcom (abordagem de gargalo)

## Estrutura do Projeto

```
Trabalho1_MetodosBusca/
├── main.py                  # Ponto de entrada - executa todos os experimentos
├── problems.py              # Definicao das 4 instancias do problema
├── heuristics.py            # Heuristicas h1 e h2
├── model/
│   ├── state.py             # Representacao do estado (dataclass imutavel)
│   ├── actions.py           # Gerador de acoes e transicoes de estado
│   └── constants.py         # Distancias, velocidades, tempos
└── algorithms/
    ├── common.py            # SearchResult (estrutura de retorno)
    ├── bfs.py               # Busca em Largura
    ├── dfs.py               # Busca em Profundidade
    ├── ucs.py               # Busca de Custo Uniforme
    ├── greedy.py            # Busca Gulosa
    └── astar.py             # A*
```

## Como Executar

```bash
python main.py
```

Executa os 7 algoritmos (BFS, DFS, UCS, Greedy h1, Greedy h2, A\* h1, A\* h2) nos 4 problemas e exibe uma tabela comparativa com custo, nos explorados, nos gerados, tamanho maximo da fronteira e tempo de execucao.

## Resultados Resumidos

Limite padrao: 500.000 nos. O Problema 4 foi testado adicionalmente com limite de 3.000.000 nos.

| Problema | Custo Otimo | Melhor Algoritmo | Observacao |
|----------|-------------|------------------|------------|
| 1 | 18 | BFS, UCS, Greedy h1, A\* | Todos os otimos concordam |
| 2 | 30 | UCS, A\* | BFS e Greedy h2 falharam (limite de 500k nos) |
| 3 | 37 | UCS, A\* | Apenas UCS, A\* e Greedy encontraram solucao |
| 4 | 61 | A\* h1 (limite estendido) | Greedy h1 encontra custo 64 (5% acima do otimo) |

### Problema 4: A\* com limite estendido

Com o limite padrao de 500k nos, apenas a Busca Gulosa com h1 encontrava solucao (custo 64). Ao estender o limite para 3M nos, o A\* com h1 encontrou a solucao otima:

| Algoritmo | Custo | Nos explorados | Nos gerados | Fronteira max | Tempo |
|-----------|-------|----------------|-------------|---------------|-------|
| Greedy h1 | 64 | 77 | 374 | 288 | 0,01s |
| A\* h1 | **61** | 826.571 | 4.964.009 | 1.125.573 | 145,5s |
| A\* h2 | N/A | >3.000.000 | - | - | - |

O plano otimo do A\* utiliza a **bandeja** para transportar duas bebidas simultaneamente, reduzindo viagens ao bar. A Busca Gulosa entrega todas individualmente, resultando em custo maior apesar de ambos os planos terem exatamente 45 acoes.

A h2 nao encontrou solucao mesmo com 3M nos porque suas estimativas mais baixas (operador max vs. soma) fazem o A\* expandir muito mais nos antes de provar otimalidade.
