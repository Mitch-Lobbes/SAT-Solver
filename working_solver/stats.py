from StatCreator import StatCreator
from sat_solver import Algorithm
import os

sudoku_filepathes = []

"""
if filename_path.startswith("example_sudokus/21") or \
        filename_path.startswith("example_sudokus/22") or \
        filename_path.startswith("example_sudokus/23") or \
        filename_path.startswith("example_sudokus/24") or \
        filename_path.startswith("example_sudokus/25") or \
        filename_path.startswith("example_sudokus/26") or \
        filename_path.startswith("example_sudokus/27") or \
        filename_path.startswith("example_sudokus/28") or \
        filename_path.startswith("example_sudokus/29") :
            continue
"""

for path, subdirs, files in os.walk('example_sudokus'):
    for name in files:
        filename_path = os.path.join(path, name)
        if len(name) != 1:
            continue
        sudoku_filepathes.append(filename_path)

#print(sudoku_filepathes)

sudoku_filepathes.sort()

stat_creator = StatCreator()

algorithm = Algorithm.DYNAMIC_VARIABLE_ORDERING
print("HERE")
stat_creator.run(sudoku_filepathes=sudoku_filepathes, algorithm=algorithm, run=1)
