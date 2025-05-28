import time


def is_valid(board, row, col, num):
    # Verificăm rândul
    for i in range(9):
        if board[row][i] == num:
            return False
    # Verificăm coloana
    for i in range(9):
        if board[i][col] == num:
            return False
    # Verificăm submatricea 3x3
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def find_empty(board):
    # Găsim prima celulă goală (reprezentată de 0)
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True  # Sudoku rezolvat complet
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # backtrack

    return False

# Exemplu de utilizare:
board = [
    [0, 0, 0, 0, 0, 0, 8, 0, 5],
    [0, 0, 0, 0, 0, 9, 0, 0, 0],
    [0, 6, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 5, 0, 0, 0, 4],
    [0, 0, 0, 3, 0, 0, 0, 0, 0],
    [7, 0, 0, 0, 0, 6, 0, 0, 0],
    [0, 0, 0, 7, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 3, 6, 0],
    [4, 0, 8, 0, 0, 0, 0, 0, 0]
]


st=time.time()
solve_sudoku(board)
print(board)
print(time.time()-st)
