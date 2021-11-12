class Variables:

    def __init__(self):
        self.variables_dict = {}
        self._initialize_dict()

    def set_value(self, key: str, value: int):
        self.variables_dict[key] = value

    def true_values(self):
        return [key for (key, value) in self.variables_dict.items() if value == 1]

    def false_values(self):
        return [key for (key, value) in self.variables_dict.items() if value == 0]

    def none_values(self):
        return [key for (key, value) in self.variables_dict.items() if value is None]

    def set_values_dict(self) -> dict:
        return {key: value for (key, value) in self.variables_dict.items() if value is not None}

    def read_sudoku(self, filename: str):
        with open(filename) as f:
            lines = f.readlines()

        for line in lines:
            number = line.split(" ")[0]
            self.variables_dict[number] = 1

    def _initialize_dict(self):
        key_list = [str(x) for x in range(111, 1000)]
        key_list = list(filter(lambda value: "0" not in str(value), key_list))
        nones = [None] * len(key_list)
        self.variables_dict = dict(zip(key_list, nones))

