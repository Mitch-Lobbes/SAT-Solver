# VSIDS: Variable State Independent Decaying Sum
# LBD: Literal Block Distance

literals = set()
activity = {}

for literal in literals:
    activity[literal] = 0

while True:
    if rules.contains_empty_clauses():
        variables_resolved_in_conflict_analysis = ... # TODO: Mitch do that
        variables_in_learned_clause = ... # TODO: Mitch do that

        for literal in conflict_analysis_literals:
            activity[literal] += 1

        for literal in variables_in_learned_clause:
            lbd = dist(learned_clause) # TODO: Mitch do that
            quality = 1 / lbd
            activity[literal] += quality

    else:
        v = max(activity)
        return v 

