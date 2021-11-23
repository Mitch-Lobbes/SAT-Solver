sudoku1000=open('example_sudokus/1000 sudokus.txt','r')
sudoku_lines = sudoku1000.read().split('\n')

f = open("demofile3.txt", "w")
f.write("Woops! I have deleted the content!")
f.close()

idx = 0
for line in sudoku_lines:
  file_name = f"example_sudokus/sudoku-example-{idx}"
  print(f"New file name: {file_name}")
  f = open(file_name, "w")
  print(f"Line: {line}")
  char_idx = 0
  for char in line:
    if char is not ".":
      row_nbr = int(char_idx / 9) + 1
      column_nbr = (char_idx % 9) + 1
      total_dmacs_val = f"{row_nbr}{column_nbr}{char} 0"
      f.write(f"{total_dmacs_val}\n")
    char_idx += 1
  idx += 1
f.close()
