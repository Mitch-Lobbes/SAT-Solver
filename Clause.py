class Clause:
    """
    Clause containing only "or" conjunctions
    """

    def __init__(self, positive_variables: list[str], negative_variables: list[str]):
        self._positive_variables = positive_variables
        self._negative_variables = negative_variables

    def contains_variable(self, variable: str) -> bool:
        return variable in self._negative_variables or variable in self._positive_variables

    def positive_variables(self) -> list[str]:
        return self._positive_variables

    def negative_variables(self) -> list[str]:
        return self._negative_variables

    def is_unit_clause(self) -> bool:
        return len(self._positive_variables) + len(self._negative_variables) == 1

    def variable_matches(self, variable: str, value: int):
        """
        If input variable matches the literal sign, i.e. is false and the sign is not returns true, otherwise false.
        """
        return (variable in self._positive_variables and value == 1) or (variable in self._negative_variables and value == 0)

    def remove_literal(self, variable: str):
        if variable in self._positive_variables:
            self._positive_variables.remove(variable)
        if variable in self._negative_variables:
            self._negative_variables.remove(variable)