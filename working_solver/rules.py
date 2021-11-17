import random
import copy


class Rules:

    def __init__(self, filepath: str):
        self._filepath = filepath
        self._clauses: list[str] = []
        self._literals = set()
        self._read_rules(filepath=filepath)
        self._literal_dict = dict(zip(copy.copy(self._literals), [0] * len(self._literals)))
        self.jerslow_wang_heuristic()
        self.three_three_clauses = []

    def clauses_containing_three_three_literals(self):
        clauses = []
        for clause in self._clauses:
            for lit in clause.split():
                if lit.replace("-", "").startswith("33"):
                    clauses.append(clause)
                    break
        self.three_three_clauses = clauses
        return clauses

    def _read_rules(self, filepath: str):
        with open(filepath) as f:
            lines = f.readlines()[1:]
            self._clauses = [clause[:-3] for clause in lines]
            for clause in self._clauses:
                for literal in clause.split():
                    variable = literal.replace("-", "")
                    self._literals.add(variable)
                    self._literals.add(f"-{variable}")
            print(f"Length of variables: {len(self._literals)}")

    def _reset_literals(self):
        self._literals = set()
        for clause in self._clauses:
            for literal in clause.split():
                variable = literal.replace("-", "")
                self._literals.add(variable)
                self._literals.add(f"-{variable}")
        self._literal_dict = dict(zip(copy.copy(self._literals), [0] * len(self._literals)))

    def remove_clause(self, literal: str) -> None:
        for clause in reversed(self._clauses):
            if literal in clause.split():
                self._clauses.remove(clause)

    def shorten_clause(self, literal: str) -> None:
        before = self.clauses_containing_three_three_literals()
        variable = literal[1:] if '-' in literal else f'-{literal}'
        for i in range(len(self._clauses) - 1, -1, -1):
            if variable in self._clauses[i].split():
                #print(f"Clause before: {self._clauses[i]}")
                before_reassign = self.clauses_containing_three_three_literals()
                self._clauses[i] = self._clauses[i].replace(variable, "").strip()
                after_reassign = self.clauses_containing_three_three_literals()
                #print(f"Clause after: {self._clauses[i]}")
        after = self.clauses_containing_three_three_literals()
        x = 5

    def remove_or_shorten_clauses_containing_literal(self, literal: str):
        # "111"  "-112"
        variable = literal.replace("-", "")
        for i in range(len(self._clauses) - 1, -1, -1):
            if variable in self._clauses[i]:
                # Negative literal
                if '-' in literal:
                    if literal in self._clauses[i]:
                        # TODO: Remove whole clause
                        del self._clauses[i]
                    else:
                        # TODO: REMOVE LITER
                        self._clauses[i] = self._clauses[i].replace(variable, "").strip()
                # Positive literal
                else:
                    if f"-{literal}" in self._clauses[i]:
                        # TODO: REMOVE LITER
                        self._clauses[i] = self._clauses[i].replace(f"-{literal}", "").strip()
                    else:
                        # TODO: Remove whole claiuse
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

        """
        literals = []
        for clause in reversed(self._clauses):
            clause_literals = clause.split()
            if len(clause_literals) == 1:
                literals.extend(clause_literals)
                self._clauses.remove(clause)
                literal = clause_literals[0]
                negation = literal[1:] if '-' in literal else f'-{literal}'
                # neg_literal = f"-{literal}" if not "-" in literal else literal[1:]
        return literals
        """

    def pick_random_literal(self):
        #self._reset_literals()
        #literal = random.sample(self._literals, 1)[0]
        #self._literals.remove(literal)
        literal = self._clauses[0].split()[0]
        return literal

    def jerslow_wang_heuristic(self):
        #self._reset_literals()
        #print(len(self._literals))
        self._literal_dict = dict(zip(copy.copy(self._literals), [0] * len(self._literals)))
        for clause in self._clauses:
            for literal in clause.split():
                self._literal_dict[literal] = self._literal_dict[literal] + 2 ** (-len(clause.split()))

    def get_literal(self):

        max_literal = max(self._literal_dict, key=self._literal_dict.get)
        neg_max_literal = f"-{max_literal}" if not "-" in max_literal else max_literal[1:]

        del self._literal_dict[max_literal]
        del self._literal_dict[neg_max_literal]

        return max_literal
