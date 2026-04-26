# Trabalho 2 - Planejamento Automatico

Solucao em PDDL para o problema da cafeteria robotica. Um dominio base e tres extensoes, com quatro instancias cada.

## Estrutura

```
pddl/
  base/                       (1 garcom; servir + limpar mesas pedidas)
  extension1_hot_drinks/      (bebida quente esfria em 4 u.t.)
  extension2_two_waiters/     (2 garcons; balcao com mutex; 1 mesa por garcom)
  extension3_finish_and_clean/(cliente termina em 4 u.t.; limpar todas as mesas)
relatorio/                    (LaTeX)
```

Cada cenario tem `domain.pddl`, `problem1.pddl` ... `problem4.pddl`, `solve.sh` e `solve.ps1`.

## Modelagem

PDDL 2.1 com `:durative-actions` e `:fluents` (mesmo perfil do `voo2` do prof). Sem `:processes`/`:events`. As janelas temporais das extensoes 1 e 3 sao representadas por durative-actions extras (`hot-window` e `drinking`).

Escala: 1 unidade PDDL = 0,5 u.t. do enunciado, para evitar fracoes.

## Como rodar

Cada script chama o OPTIC dentro do container `azathoth/pddl` sobre os quatro problemas do cenario. Por padrao, os scripts usam `-N` para buscar um plano viavel sem otimizar custo, pois a otimizacao completa do OPTIC pode demorar muito mesmo em instancias pequenas.

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
