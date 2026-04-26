# Trabalho 2 - Planejamento Automatico

Solucao em PDDL para o problema da cafeteria robotica. Um dominio base e tres extensoes, com quatro instancias cada.

Observacao de escopo: este repositorio resolve o problema como planejamento automatico em PDDL/OPTIC. Se a avaliacao exigir implementacao propria de algoritmos de busca em espaco de estados (BFS, UCS, A*, heuristicas etc.), isso e uma entrega diferente desta modelagem.

## Estrutura

```
pddl/
  base/                       (1 garcom; servir + limpar mesas pedidas)
  extension1_hot_drinks/      (bebida quente esfria em 4 u.t.)
  extension2_two_waiters/     (2 garcons; balcao com mutex; cada mesa tem 1 garcom)
  extension3_finish_and_clean/(cliente termina em 4 u.t.; limpar todas as mesas)
relatorio/                    (LaTeX)
```

Cada cenario tem `domain.pddl`, `problem1.pddl` ... `problem4.pddl`, `solve.sh` e `solve.ps1`.

## Modelagem

PDDL 2.1 com `:durative-actions` e `:fluents`, seguindo o mesmo perfil dos exemplos temporais do professor, como `voo2` e `jars`. As janelas temporais das extensoes 1 e 3 sao representadas por acoes durativas auxiliares (`hot-window` e `drinking`). Na extensao 1, `hot-window` comeca antes do preparo da bebida quente e cobre preparo + entrega, evitando que o solver adie artificialmente o resfriamento.

Escala: 1 unidade PDDL = 0,5 u.t. do enunciado, para evitar fracoes.

## Como rodar

Cada script chama o OPTIC dentro do container `azathoth/pddl` sobre os quatro problemas do cenario. Por padrao, os scripts usam `-N`, opcao do OPTIC que desativa a otimizacao da qualidade da solucao (`Don't optimise solution quality`). Na pratica, o planejador para quando encontra um plano viavel, sem tentar provar que o makespan/custo e minimo. Isso torna a execucao mais rapida, pois a otimizacao completa do OPTIC pode demorar muito mesmo em instancias pequenas.

```bash
./pddl/base/solve.sh
```

```powershell
.\pddl\base\solve.ps1
```

No Windows, use preferencialmente `solve.ps1` no PowerShell. O `solve.sh` precisa de um ambiente Unix real, como Git Bash ou WSL Ubuntu/Debian com integracao do Docker Desktop habilitada. A distribuicao interna `docker-desktop` do WSL nao suporta chamar o Docker CLI diretamente.

Para tentar otimizacao completa:

```bash
OPTIMIZE=1 ./pddl/base/solve.sh
```

```powershell
.\pddl\base\solve.ps1 -Optimize
```

Os scripts podem ser chamados tanto de dentro do diretorio do cenario quanto da raiz do projeto.

## Resultados atuais

Custos reportados pelo OPTIC em modo padrao (`-N`), convertidos para u.t. do enunciado. Como 1 unidade PDDL = 0,5 u.t., os valores abaixo sao os custos do OPTIC divididos por 2 e arredondados para uma casa decimal, removendo pequenos epsilons numericos do planejador.

| Cenario | p1 | p2 | p3 | p4 |
| --- | ---: | ---: | ---: | ---: |
| base | 15.5 | 22.5 | 24.0 | 38.0 |
| extension1_hot_drinks | 15.5 | 20.5 | 25.0 | 39.0 |
| extension2_two_waiters | 13.0 | 22.5 | 24.0 | 38.0 |
| extension3_finish_and_clean | 24.5 | 36.5 | 39.0 | 58.0 |

Esses valores sao cotas superiores: por padrao o OPTIC busca rapidamente um plano viavel. A otimizacao completa pode demorar bastante. Por isso, planos sem uso de bandeja sao aceitaveis como planos validos, mas nao demonstram que a bandeja seja inutil ou que o plano seja otimo.
