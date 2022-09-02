from audioop import avg
import numpy as np
from dokusan import generators


def generate_board(level):
    if level.lower() == "easy":
        return np.array(list(str(generators.random_sudoku(avg_rank=50)))).reshape(9,9)
    elif level.lower() == "medium":
        return np.array(list(str(generators.random_sudoku(avg_rank=100)))).reshape(9,9)
    elif level.lower() == "hard":
        return np.array(list(str(generators.random_sudoku(avg_rank=200)))).reshape(9,9)

