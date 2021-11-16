import random
import copy

class Rules:

    def __init__(self, filepath: str):
        self._clauses: list[str] = []
        self._literals = set()
        self._read_rules(filepath=filepath)
        self._literal_dict = dict(zip(copy.copy(self._literals),[0]*len(self._literals)))
        self.jerslow_wang_heuristic()

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
        for idx, clause in enumerate(self._clauses):
            if not clause:
                return True
        return False

    def unit_rule(self):
        literals = []
        for clause in reversed(self._clauses):
            clause_literals = clause.split()
            if len(clause_literals) == 1:
                literals.extend(clause_literals)
                self._clauses.remove(clause)
                literal = clause_literals[0]
                #neg_literal = f"-{literal}" if not "-" in literal else literal[1:]
                for i in range(len(self._clauses) - 1, -1, -1):
                    clause_list = self._clauses[i].split()
                    if literal in clause_list:
                        if '-' in literal:
                            if literal in clause_list:
                                # TODO: Remove whole clause
                                del self._clauses[i]
                            else:
                                # TODO: REMOVE LITER
                                self._clauses[i] = self._clauses[i].replace(literal, "").strip()
                        # Positive literal
                        else:
                            if f"-{literal}" in clause_list:
                                # TODO: REMOVE LITER
                                self._clauses[i] = self._clauses[i].replace(f"-{literal}", "").strip()
                            else:
                                # TODO: Remove whole clause
                                del self._clauses[i]


        return literals
    
    def pick_random_literal(self):
        literal = random.sample(self._literals, 1)[0]
        self._literals.remove(literal)
        return literal

    def jerslow_wang_heuristic(self):
        self._literal_dict = dict(zip(copy.copy(self._literals), [0] * len(self._literals)))
        for clause in self._clauses:
            for literal in clause.split():
                self._literal_dict[literal] = self._literal_dict[literal] + 2**(-len(clause.split()))

    def get_literal(self):
        max_literal = max(self._literal_dict, key=self._literal_dict.get)
        neg_max_literal = f"-{max_literal}" if not "-" in max_literal else max_literal[1:]

        del self._literal_dict[max_literal]
        del self._literal_dict[neg_max_literal]

        return max_literal
