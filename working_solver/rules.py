import random
import copy

from helper import negate_literal

ALPHA = 1
BETA = 2

class Rules:

    def __init__(self, filepath: str):
        self._filepath = filepath
        self._clauses: list[str] = []
        self._literals = set()
        self._read_rules(filepath=filepath)
        self._variables = set([lit for lit in self._literals if "-" not in lit])
        self._dynamic_weight_values = dict.fromkeys(self._variables,0)

        self._literal_dict = dict(zip(copy.copy(self._literals), [0] * len(self._literals)))
        self.jerslow_wang_heuristic()
        #self._bohm_dict = {k: [0] * 9 for k in self._literals}
        #self._bohm_dict_values = {k: [0] * 9 for k in self._variables}
        #self.bohms_heuristic()

    def _read_rules(self, filepath: str):
        with open(filepath) as f:
            lines = f.readlines()[1:]
            self._clauses = [clause[:-3] for clause in lines]
            for clause in self._clauses:
                for literal in clause.split():
                    variable = literal.replace("-", "")
                    self._literals.add(variable)
                    self._literals.add(f"-{variable}")
            # print(f"Length of variables: {len(self._literals)}")

    def remove_clause(self, literal: str) -> None:
        for clause in reversed(self._clauses):
            if literal in clause.split():
                self._clauses.remove(clause)

    def shorten_clause(self, literal: str) -> None:
        variable = literal[1:] if '-' in literal else f'-{literal}'
        for i in range(len(self._clauses) - 1, -1, -1):
            if variable in self._clauses[i].split():
                self._clauses[i] = self._clauses[i].replace(variable, "").strip()

    def remove_or_shorten_clauses_containing_literal(self, literal: str):
        variable = literal.replace("-", "")
        for i in range(len(self._clauses) - 1, -1, -1):
            if variable in self._clauses[i]:
                # Negative literal
                if '-' in literal:
                    if literal in self._clauses[i]:
                        del self._clauses[i]
                    else:
                        self._clauses[i] = self._clauses[i].replace(variable, "").strip()
                # Positive literal
                else:
                    if f"-{literal}" in self._clauses[i]:
                        self._clauses[i] = self._clauses[i].replace(f"-{literal}", "").strip()
                    else:
                        del self._clauses[i]

    def contains_clauses(self):
        return len(self._clauses) > 0

    def contains_empty_clauses(self):
        for clause in self._clauses:
            if not clause.strip():
                return True
        return False

    def unit_rule(self):
        literals = set()
        for clause in self._clauses:
            clause_literals = clause.split()
            if len(clause_literals) == 1:
                literals.add(clause_literals[0])
        return literals

    def jerslow_wang_heuristic(self):
        self._literal_dict = dict(zip(copy.copy(self._literals), [0] * len(self._literals)))
        for clause in self._clauses:
            for literal in clause.split():
                self._literal_dict[literal] = self._literal_dict[literal] + 2 ** (-len(clause.split()))

    def bohms_heuristic(self):
        #self._bohm_dict = dict(zip(copy.copy(self._literals), copy.copy([[0] * 9] * len(self._literals))))
        self._variables = set([lit for lit in self._literals if "-" not in lit])

        self._bohm_dict = {k: [0] * 9 for k in self._literals}
        self._bohm_dict_values = {k: [0] * 9 for k in self._variables}

        for clause in self._clauses:
            clause_ln = len(clause.split())
            for lit in clause.split():
                self._bohm_dict[lit][clause_ln-1] = self._bohm_dict[lit][clause_ln-1] + 1

        for variable, h_values in self._bohm_dict_values.items():
            for i in range(9):
                pos_var_occurrences = self._bohm_dict[variable][i]
                neg_var_occurrences = self._bohm_dict[f"-{variable}"][i]
                h_value = ALPHA * max(pos_var_occurrences, neg_var_occurrences) + BETA * min(pos_var_occurrences, neg_var_occurrences)
                h_values[i] = h_value

    def moms_heuristic(self):
        for i in range(2, 9):
            smallest_clauses = [clause for clause in self._clauses if len(clause.split()) == i]
            if smallest_clauses:
                break

        elements = []

        for clause in smallest_clauses:
            clause = clause.split()
            elements.extend(clause)

        self._variables = set([lit for lit in self._literals if "-" not in lit])

        highest_val = 0
        for var in self._variables:
            # k = 2
            f_x = elements.count(var)
            f_x_prime = elements.count(negate_literal(var))

            current_val = (f_x + f_x_prime) + 2**2 + (f_x * f_x_prime)
            if current_val > highest_val:
                highest_val = current_val
                highest_var = var

        negative_literal = negate_literal(highest_var)

        if highest_var in self._literal_dict:
            del self._literal_dict[highest_var]
        if negative_literal in self._literal_dict:
            del self._literal_dict[negative_literal]

        return negative_literal

    def dynamical_weight_variable_ordering(self):
        self._variables = set([lit for lit in self._literals if "-" not in lit])
        self._dynamic_weight_values = dict.fromkeys(self._literals, 0)

        r = len(self._clauses) / len(self._variables)
        w = 5 if r < 6.3 else 6 - 3.33*r if r <= 7.2 else 2
        for clause in self._clauses:
            for lit in clause.split():
                self._dynamic_weight_values[lit] += w**(-len(clause.split()))

        highest_val = 0
        for var in self._variables:
            neg_var = negate_literal(var)
            combined_val = self._dynamic_weight_values[var] + self._dynamic_weight_values[neg_var]
            if combined_val > highest_val:
                highest_val = combined_val
                highest_var = var

        negative_literal = negate_literal(highest_var)

        if highest_var in self._literal_dict:
            del self._literal_dict[highest_var]
        if negative_literal in self._literal_dict:
            del self._literal_dict[negative_literal]

        return negative_literal

    def basic_DPLL(self):
        # Return random literal
        return random.sample(self._literals, 1)[0]


    def get_literal(self):
        max_literal = max(self._literal_dict, key=self._literal_dict.get)
        neg_max_literal = negate_literal(literal=max_literal)

        del self._literal_dict[max_literal]
        del self._literal_dict[neg_max_literal]

        return max_literal
