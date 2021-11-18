import matplotlib.pyplot as plt


def plot_sudoku(matrix):
    fig, ax = plt.subplots()
    # hide axes
    # fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    table = ax.table(
        cellText=matrix,
        loc='center',
        cellLoc='right',
    )
    # fig.tight_layout()

    idx = 0

    for key, cell in table.get_celld().items():
        #print(key)
        #print(cell)
        #if idx == 5:
            #cell.set_linewidth(5)
        idx += 1

    plt.show()


matrix = [[2, 6, 9, 1, 7, 8, 5, 3, 4],
          [2, 6, 9, 1, 7, 8, 5, 3, 4],
          [2, 6, 9, 1, 7, 8, 5, 3, 4],
          [2, 6, 9, 1, 7, 8, 5, 3, 4],
          [2, 6, 9, 1, 7, 8, 5, 3, 4],
          [2, 6, 9, 1, 7, 8, 5, 3, 4],
          [2, 6, 9, 1, 7, 8, 5, 3, 4],
          [2, 6, 9, 1, 7, 8, 5, 3, 4],
          [2, 6, 9, 1, 7, 8, 5, 3, 4]]

#plot_sudoku(matrix)


def negate_literal(literal: str) -> str:
    return f"-{literal}" if not "-" in literal else literal[1:]
