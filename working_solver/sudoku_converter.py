sudoku1000=open('example_sudokus/1000 sudokus.txt','r')
sudoku_lines = sudoku1000.read().split('\n')

f = open("demofile3.txt", "w")
f.write("Woops! I have deleted the content!")
f.close()

for line in sudoku_lines:
  idx = 0
  file_name = f"example_sudokus/sudoku-example-{idx}"
  f = open(file_name, "w")
  for char in line:
    if char is not ".":
      row_nbr = int(idx / 9) + 1
      column_nbr = idx % 9
      total_dmacs_val = f"{row_nbr}{column_nbr}{char} 0"
      f.write(f"{total_dmacs_val}\n")
    idx += 1