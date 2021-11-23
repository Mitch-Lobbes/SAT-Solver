alpha = 0.4
num_conflicts = 0
plays = []
multiplier = 1

literals = set()  # TODO: Initialize

lastConflict = {}
Q = {}

for lit in literals:
    lastConflict[lit] = 0
    Q[lit] = 0

while True:
    # BCP
    unit_rule_literals = rules.unit_rule()
    plays.append(unit_rule_literals)

    if rules.contains_empty_clauses():
        multiplier = 1
    if not rules.contains_clauses():
        multiplier = 0.9

    for lit in plays:
        reward = multiplier / (num_conflicts - lastConflict[lit] + 1)
        Q[lit] = (1 - alpha) * Q[lit] + alpha * reward

    if rules.contains_empty_clauses():
        num_conflicts += 1
        # if decisionLevel == 0. return UNSAT
        if alpha > 0.06:
            alpha -= 10 ** -6

        # TODO: Conflict analysis -> Add new clauses MITCH

        c = variables_in_conflict_analysis
        u = first_uip_of_learned_clause

        for lit in c:
            lastConflict[lit] = num_conflicts

        plays.append(u)

    else:
        



    pass
