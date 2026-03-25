"""Debug: trace optimal path costs for problems 1 and 2."""
from algorithms import ucs
from problems import create_problem_1, create_problem_2
from model.actions import format_action, apply_action, get_actions

for create_fn in [create_problem_1, create_problem_2]:
    state, gd, gc, name = create_fn()
    result = ucs(state, gd, gc)
    print(f"\n{'='*60}")
    print(f"{name} - UCS Cost: {result.cost}")
    print(f"{'='*60}")

    # Replay path to get individual action costs
    prev = state
    total = 0
    for s, a in result.path[1:]:
        for act in get_actions(prev):
            ns, c = apply_action(prev, act)
            if ns == s:
                print(f"  {format_action(act):45s} cost={c:3}  t={ns.time} barista_busy={ns.barista_busy_until} waiter_pos={ns.waiter_pos}")
                total += c
                break
        prev = s
    print(f"\n  Sum of costs: {total}")
