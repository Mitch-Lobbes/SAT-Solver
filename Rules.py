from typing import Tuple

from Clause import Clause


class Rules:

    def __init__(self, filepath: str):
        self._rules = []
        self._clauses = []
        self._variables_set = set()
        self._read_rules(filepath=filepath)
        self._convert_rules_to_clauses()

    def get_length(self):
        return len(self._clauses)

    def is_empty(self):
        return len(self._clauses) == 0

    def _read_rules(self, filepath: str):
        with open(filepath) as f:
            self._rules = f.readlines()[1:]

    def _convert_rules_to_clauses(self):
        for rule in self._rules:
            variables = rule.split()
            negative_vars = [var[1:] for var in variables if '-' in var]
            positive_vars = [var for var in variables if '-' not in var and var != "0"]
            self._variables_set.update(negative_vars)
            self._variables_set.update(positive_vars)

            clause = Clause(
                negative_variables=negative_vars,
                positive_variables=positive_vars
            )
            self._clauses.append(clause)

    def _count_variable_occurrences(self):
        # Initialize all to zero
        variable_occurrences = {}
        for var in self._variables_set:
            variable_occurrences[var] = [0, 0]

        for clause in self._clauses:
            positive_variables = clause.positive_variables()
            negative_variables = clause.negative_variables()
            for var in positive_variables:
                variable_occurrences[var][0] += 1
            for var in negative_variables:
                variable_occurrences[var][1] += 1
        return variable_occurrences

    def _get_most_frequent_var(self) -> str:
        return list(self._variable_occurrences.keys())[
            list(self._variable_occurrences.values()).index(max(self._variable_occurrences.values()))]

    def get_most_frequent_vars(self) -> list:
        variable_occurrences = self._count_variable_occurrences()
        return sorted(variable_occurrences.items(), key=lambda x: x[1], reverse=True)

    def get_occurrences_for_variable(self, variable: str) -> list[int, int]:
        var_occurrence = self._count_variable_occurrences()
        return var_occurrence[variable]

    def simplify_based_on_var_values(self, variables: dict):
        self._remove_clause_or_rule(variables=variables)

    def _remove_clause_or_rule(self, variables: dict):
        for clause in reversed(self._clauses):
            for variable in variables.keys():
                if clause.contains_variable(variable=variable):
                    if clause.variable_matches(variable=variable, value=variables[variable]):
                        # We can remove the whole clause
                        #del self._clauses[self._clauses.index(clause)]
                        self._clauses.remove(clause)
                        break
                    else:
                        # Remove the one literal
                        clause.remove_literal(variable=variable)

    def search_for_pure_literals(self):
        var_occurrence = self._count_variable_occurrences()
        pure_literals = {k: v for (k, v) in var_occurrence.items() if
                         (v[0] == 0 and v[1] != 0) or (v[1] == 0 and v[0] != 0)}
        return pure_literals

    def get_unit_clauses(self):
        return [clause for clause in self._clauses if clause.is_unit_clause()]