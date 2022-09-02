import random


def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                return (row, col)

def find_all_empty(board):
    empty_cells = []
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                coordinate = (row, col)
                empty_cells.append(coordinate)
    return empty_cells

def is_valid(pos, num, board):
    for row in range(9):
        if board[row][pos[1]] == num and pos[0] != row:
            return False
    for col in range(9):
        if board[pos[0]][col] == num and pos[1] != col:
           return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i,j) != pos:
                return False
        
    return True

def solve(board):
    find_cell = find_empty(board)
    if not find_cell:
        return True
    else:
        row,col = find_cell

    for i in range(1, 10):
        if is_valid(find_cell, str(i), board):
            board[row][col] = str(i)
            if solve(board):
                return True
            board[row][col] = '0'
    return False
