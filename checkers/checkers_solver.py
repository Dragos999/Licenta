import copy
import math
import time
# Reprezentare: 0 = gol, 1 = piesă bot, 2 = damă bot, -1 = piesă adversar, -2 = damă adversar

DIRECTION = {
    1: [(-1, -1), (-1, 1)],    # jucătorul bot (se deplasează în sus)
    -1: [(1, -1), (1, 1)],     # adversar (se deplasează în jos)
}

def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def deepcopy_board(board):
    return copy.deepcopy(board)

def get_piece_directions(piece):
    if abs(piece) == 2:
        return [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # damele se mișcă în toate direcțiile
    return DIRECTION[1 if piece > 0 else -1]

def get_all_moves(board, player):
    all_moves = []
    captures = []

    for x in range(8):
        for y in range(8):
            if (player == 1 and board[x][y] > 0) or (player == -1 and board[x][y] < 0):
                multi_jumps = []
                find_captures(board, x, y, [], multi_jumps, board[x][y])
                if multi_jumps:
                    captures.extend(multi_jumps)
                else:
                    steps = get_piece_directions(board[x][y])
                    for dx, dy in steps:
                        nx, ny = x + dx, y + dy
                        if in_bounds(nx, ny) and board[nx][ny] == 0:
                            all_moves.append([(x, y), (nx, ny)])

    return captures if captures else all_moves

def find_captures(board, x, y, path, results, piece):
    path = path + [(x, y)]
    found = False
    for dx, dy in get_piece_directions(piece):
        mid_x, mid_y = x + dx, y + dy
        end_x, end_y = x + 2*dx, y + 2*dy
        if in_bounds(end_x, end_y):
            enemy = board[mid_x][mid_y]
            if (enemy != 0 and (enemy * piece < 0)) and board[end_x][end_y] == 0:
                temp_board = deepcopy_board(board)
                temp_board[end_x][end_y] = temp_board[x][y]
                temp_board[x][y] = 0
                temp_board[mid_x][mid_y] = 0
                find_captures(temp_board, end_x, end_y, path, results, piece)
                found = True
    if not found and len(path) > 1:
        results.append(path)

def apply_move(board, move):
    new_board = deepcopy_board(board)
    start = move[0]
    end = move[-1]
    piece = new_board[start[0]][start[1]]
    new_board[start[0]][start[1]] = 0

    # Captură
    for i in range(1, len(move)):
        mid_x = (move[i-1][0] + move[i][0]) // 2
        mid_y = (move[i-1][1] + move[i][1]) // 2
        if abs(move[i][0] - move[i-1][0]) == 2:
            new_board[mid_x][mid_y] = 0

    new_board[end[0]][end[1]] = piece

    # Promovare în damă
    if piece == 1 and end[0] == 0:
        new_board[end[0]][end[1]] = 2
    elif piece == -1 and end[0] == 7:
        new_board[end[0]][end[1]] = -2

    return new_board

def evaluate(board):
    score = 0
    for x in range(8):
        for y in range(8):
            cell = board[x][y]
            if cell == 1:
                score += 3 + (7 - x) * 0.1  # piesele mai aproape de promovare sunt mai valoroase
            elif cell == 2:
                score += 5 + 0.5 * (x in [2,3,4,5])  # damele centrale sunt mai bune
            elif cell == -1:
                score -= 3 + x * 0.1
            elif cell == -2:
                score -= 5 + 0.5 * (x in [2,3,4,5])
    return score

def is_game_over(board):
    return not get_all_moves(board, 1) or not get_all_moves(board, -1)

def minimax(board, depth, alpha, beta, maximizing_player,st):

    final_board=[]
    if depth == 0 or is_game_over(board):
        return evaluate(board), None, None

    best_move = None
    player = 1 if maximizing_player else -1
    moves = get_all_moves(board, player)

    if maximizing_player:
        max_eval = -math.inf
        for move in moves:

            new_board = apply_move(board, move)
            eval_score, _,_ = minimax(new_board, depth - 1, alpha, beta, False,st)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
                final_board = new_board
            alpha = max(alpha, eval_score)
            if beta <= alpha or time.time()-st>=5.0:
                break
        return max_eval, best_move, final_board
    else:
        min_eval = math.inf
        for move in moves:

            new_board = apply_move(board, move)
            eval_score, _ ,_= minimax(new_board, depth - 1, alpha, beta, True,st)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
                final_board= new_board
            beta = min(beta, eval_score)
            if beta <= alpha or time.time()-st>=5.0:
                break
        return min_eval, best_move, final_board

"""
# Inițializare tablou simplu
initial_board = [
    [0, -1, 0, -1, 0, -1, 0, -1],
    [-1, 0, -1, 0, -1, 0, -1, 0],
    [0, -1, 0, 0, 0, -1, 0, -1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, -1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0]]
start=time.time()
score, best_move, board = minimax(initial_board, depth=10, alpha=-math.inf, beta=math.inf, maximizing_player=True,st=time.time())
print("Timp: ", time.time()-start)
print("Scor:", score)
print("Mutare optimă:", best_move[len(best_move)-1])
print(board)
for i in range(1,len(best_move)):
    print(best_move[i-1],best_move[i])"""