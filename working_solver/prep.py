import os
"""
for filename in os.listdir("example_sudokus"):
    if filename.startswith("sudoku-example"):
        num_vars = sum(1 for line in open(f'example_sudokus/{filename}') if line.strip())
        print(filename)
        print(num_vars)

        dir_name = f'example_sudokus/{num_vars}'

        if not os.path.exists(dir_name):
            os.mkdir(dir_name)

        os.rename(f'example_sudokus/{filename}', f"{dir_name}/{filename}")
"""
file_idx = 0
num_vars = 25
for filename in os.listdir("example_sudokus/27"):
    line_idx = 0
    dir_name = f'example_sudokus/{num_vars}'

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    f = open(f"{dir_name}/{file_idx}", "a")

    if filename.startswith("sudoku-example"):
        for line in open(f'example_sudokus/27/{filename}'):
            f.write(line)
            line_idx += 1
            if line_idx == num_vars:
                break
    f.close()
    file_idx += 1
    if file_idx == 10:
        num_vars += 1
        file_idx = 0
    if num_vars == 27:
        break


