import copy

from Rules import Rules
from Variables import Variables

class Environment:

    def __init__(self, variables: Variables, rules: Rules, id: int):
        self._variables = variables
        self._initial_rules = rules
        self._backup_rules = copy.copy(self._initial_rules)
        self._key_variable: str
        self._already_flipped = False
        self._id = id

    def run(self):
        """
        Run environment with the current setup

        Returns: False if run failed, variable setup if successful
        """
        # Simplify initial rules
        success = True

        old_rules_ln = self._initial_rules.get_length()

        self._initial_rules.simplify_based_on_var_values(self._variables.set_values_dict())
        self._set_variables_based_on_pure_literals()
        self._set_variables_based_on_unit_clauses()

        print('Simplification Successful')

        if len(self._variables.none_values()) != 0:
            print('Now We Split')

            self.split_most_frequent()

        # Check condition
        if not self._initial_rules.is_empty() and len(self._variables.none_values()) == 0:
            # backtrack
            success = False

        return success, (self._variables, self._initial_rules)

    def split_most_frequent(self):
        print(f"Environment [{self._id}] is splitting")
        most_frequent_vars = self._initial_rules.get_most_frequent_vars()
        var_to_split = [var for var in most_frequent_vars if self._variables.variables_dict[var[0]] is None][0][0]
        occurrences = self._initial_rules.get_occurrences_for_variable(variable=var_to_split)
        value = 1 if occurrences[0] > occurrences[1] else 0
        self._variables.set_value(
            key=var_to_split,
            value=value
        )
        self._key_variable = var_to_split
        print(f"Key variable: {self._key_variable}")

    def flip_last_variable(self):
        print(f"Flipping last variable in environment [{self._id}]")
        if self._already_flipped or self._initial_rules.rules_are_violated(self._key_variable,self._variables.variables_dict ):
            return False
        # Check if rules are violated
        self._variables.variables_dict[self._key_variable] = 1 - self._variables.variables_dict[self._key_variable]
        self._already_flipped = True
        self._initial_rules = self._backup_rules
        return True

    def _set_variables_based_on_pure_literals(self):
        pure_literals = self._initial_rules.search_for_pure_literals()
        for literal, occurrences in pure_literals.items():
            self._variables.set_value(
                key=literal,
                value=0 if occurrences[0] == 0 else 1
            )

    def _set_variables_based_on_unit_clauses(self):
        unit_clauses = self._initial_rules.get_unit_clauses()
        for clause in unit_clauses:
            positive_vars = clause.positive_variables()
            negative_vars = clause.negative_variables()
            if len(positive_vars) != 0:
                # Set var to true
                self._variables.set_value(
                    key=positive_vars[0],
                    value=1
                )
            elif len(negative_vars) != 0:
                # Set var to false
                self._variables.set_value(
                    key=negative_vars[0],
                    value=0
                )
        pass
