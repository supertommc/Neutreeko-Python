game = [
    [1, 0, 1],
    [0, 0, 0],
    [2, 0, 2]
]

MAX = 999999
MIN = -999999

def get_other_piece(piece):
    return 1 if piece == 2 else 2

def check_game_over(game, piece):
    return game[1][1] == piece

def check_game_over_full(game):
    return check_game_over(game, 1) or check_game_over(game, 2)

def valid_coord(coord):
    return coord >= 0 and coord < 3

def valid_coords(x, y):
    return valid_coord(x) and valid_coord(y)

def different_move(x, y, new_x, new_y):
    return not (x == new_x and y == new_y)

def make_move(game, move):
    x, y, new_x, new_y = move
    piece = game[y][x]

    if piece == 0 or game[new_y][new_x] != 0:
        return False
    
    game[y][x] = 0
    game[new_y][new_x] = piece

    return True

def unmake_move(game, move):
    x, y, new_x, new_y = move
    piece = game[new_y][new_x]

    if piece == 0 or game[y][x] != 0:
        return False
    
    game[new_y][new_x] = 0
    game[y][x] = piece

    return True

def generate_moves(game, piece_pos):
    
    x, y = piece_pos

    if game[y][x] == 0:
        return False

    moves = []

    # Up and Down
    new_y = y + 1
    if new_y != 5:
        while valid_coord(new_y) and game[new_y][x] == 0:
            new_y += 1
        if different_move(x, y, x, new_y-1):
            moves.append((x, y, x, new_y-1))

    new_y = y - 1
    if new_y != -1:
        while valid_coord(new_y) and game[new_y][x] == 0:
            new_y -= 1
        if different_move(x, y, x, new_y+1):
            moves.append((x, y, x, new_y+1))

    # Left and Right
    new_x = x + 1
    if new_x != 5:
        while valid_coord(new_x) and game[y][new_x] == 0:
            new_x += 1
        if different_move(x, y, new_x-1, y):
            moves.append((x, y, new_x-1, y))

    new_x = x - 1
    if new_x != -1:
        while valid_coord(new_x) and game[y][new_x] == 0:
            new_x -= 1
        if different_move(x, y, new_x+1, y):
            moves.append((x, y, new_x+1, y))

    # Diagonal Up Right
    new_y = y - 1
    new_x = x + 1
    if new_x != 5 and new_y != -1:
        while valid_coords(new_x, new_y) and game[new_y][new_x] == 0:
            new_y -= 1
            new_x += 1
        if different_move(x, y, new_x-1, new_y+1):
            moves.append((x, y, new_x-1, new_y+1))

    # Diagonal Down Right
    new_y = y + 1
    new_x = x + 1
    if new_x != 5 and new_y != 5:
        while valid_coords(new_x, new_y) and game[new_y][new_x] == 0:
            new_y += 1
            new_x += 1
        if different_move(x, y, new_x-1, new_y-1):
            moves.append((x, y, new_x-1, new_y-1))
        
    # Diagonal Up Left
    new_y = y - 1
    new_x = x - 1
    if new_x != -1 and new_y != -1:
        while valid_coords(new_x, new_y) and game[new_y][new_x] == 0:
            new_y -= 1
            new_x -= 1
        if different_move(x, y, new_x+1, new_y+1):
            moves.append((x, y, new_x+1, new_y+1))

    # Diagonal Down Left
    new_y = y + 1
    new_x = x - 1
    if new_x != -1 and new_y != 5:
        while valid_coords(new_x, new_y) and game[new_y][new_x] == 0:
            new_y += 1
            new_x -= 1
        if different_move(x, y, new_x+1, new_y-1):
            moves.append((x, y, new_x+1, new_y-1))

    return moves

def generate_all_moves(game, piece):
    moves = []
    for i in range(3):
        for j in range(3):
            if game[i][j] == piece:
                moves.extend(generate_moves(game, (j, i)))
    return moves

def evaluate_position(piece, game):

    other_piece = get_other_piece(piece)

    if check_game_over(game, other_piece):
        return 10000
    elif check_game_over(game, piece):
        return -10000
    else:
        return 0


def minimax_alpha_beta(is_max, current_player, game, depth, alpha, beta):

    res = check_game_over_full(game)
    if res or depth == 0:
        return evaluate_position(current_player, game)

    moves = generate_all_moves(game, current_player)
    if is_max:
        best_score = MIN
        for move in moves:
            make_move(game, move)

            score = minimax_alpha_beta(not is_max, get_other_piece(current_player), game, depth-1, alpha, beta)
            best_score = max(score, best_score)

            unmake_move(game, move)
            print("\t"*(3-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": Score: " + str(score) + ": Alpha: " + str(alpha) + ": Beta: " + str(beta))

        return best_score
    else:
        best_score = MAX
        for move in moves:
            make_move(game, move)

            score = minimax_alpha_beta(not is_max, get_other_piece(current_player), game, depth-1, alpha, beta)
            best_score = min(best_score, score)

            unmake_move(game, move)
            print("\t"*(3-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": Score: " + str(score) + ": Alpha: " + str(alpha) + ": Beta: " + str(beta))

        return best_score
        

from pprint import pprint
def test():
    game = [
            [1, 0, 1],
            [0, 0, 0],
            [2, 0, 2]
            ]

    pprint(game)

    print(minimax_alpha_beta(True, 1, game, 3, 0, 0))

    pprint(game)



test()