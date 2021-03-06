from timeit import default_timer as timer
import datetime
from pprint import pprint

MAX = 99999999
MIN = -99999999

game =  [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]

"""
        game =  [
            [0, 2, 1, 2, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]
"""

rel_scores = [
                [1, 2, 2, 2, 1],
                [2, 3, 3, 3, 2],
                [2, 3, 5, 3, 2],
                [2, 3, 3, 3, 2],
                [1, 2, 2, 2, 1]
            ]

def valid_coord(coord):
    return coord >= 0 and coord < 5

def valid_coords(x, y):
    return valid_coord(x) and valid_coord(y)

def different_move(x, y, new_x, new_y):
    return not (x == new_x and y == new_y)

def get_ones_positions(game_int):
    i = 1
    pos = 0
    positions = []
    for j in range(25):
        if i & game_int != 0:
            positions.append(pos)
        i = i << 1
        pos += 1
    
    return positions
    

def pos_valid(pos):
    return pos >= 0 and pos <= 24

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
    for i in range(len(game)):
        for j in range(len(game[0])):
            if game[i][j] == piece:
                moves.extend(generate_moves(game, (j, i)))
    return moves

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

# Piece is 1 for black and 2 for white
def game_to_int(game, piece):
    game_int = 0
    for y in range(5):
        for x in range(5):
            if game[y][x] == piece:
                game_int = game_int | (1 << 5*y+x)
    return game_int

def check_game_over_full(game):
    if check_game_over(game, 1):
        return 1
    elif check_game_over(game, 2):
        return 2
    else:
        return 0

def check_game_over(game, piece):
    game_int = game_to_int(game, piece)
    res = 0

    # Horizontal Row
    res |= game_int & (game_int >> 1) & (game_int >> 2) & 0x739ce7

    # Vertical Row
    res |= game_int & (game_int >> 5) & (game_int >> 10)

    # Diagonal Down Right
    res |= game_int & (game_int >> 6) & (game_int >> 12) & 0x1ce7

    # Diagonal Up Right
    res |= game_int & (game_int >> 4) & (game_int >> 8) & 0x739c

    return res != 0

def get_other_piece(piece):
    return 1 if piece == 2 else 2

"""
    peças no centro
    peças juntas sem estarem cercadas
    peças do adversario no meio das tuas peças
    casas que tu controlas e o adversario nao
"""
def evaluate_position(piece, game):

    other_piece = get_other_piece(piece)

    if check_game_over(game, 1):
        return 10000
    elif check_game_over(game, 2):
        return -10000
    else:
        val = 0
        for i in range(len(game)):
            for j in range(len(game[0])):
                if game[i][j] == 1:
                    val += rel_scores[i][j]
                elif game[i][j] == 2:
                    val -= rel_scores[i][j]
        return val

def minimax_alpha_beta(is_max, current_player, game, depth, alpha, beta):

    res = check_game_over_full(game)
    if res != 0 or depth == 0:
        return evaluate_position(current_player, game)

    pos_scores = []
    moves = generate_all_moves(game, current_player)

    if is_max:
        for move in moves:
            score = MIN
            make_move(game, move)

            score = max(score, minimax_alpha_beta(not is_max, get_other_piece(current_player), game, depth-1, alpha, beta))
            alpha = max(alpha, score)

            unmake_move(game, move)

            if alpha >= beta:
                #print("CUT!!!!")
                pos_scores.append(score)
                break
            else:
                pos_scores.append(score)

                print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(pos_scores) + ": Score: " + str(score) + ": Alpha: " + str(alpha) + ": Beta: " + str(beta))

        #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

        return max(pos_scores) if len(pos_scores) != 0 else MIN
    else:
        for move in moves:
            score = MAX
            make_move(game, move)

            score = min(score, minimax_alpha_beta(not is_max, get_other_piece(current_player), game, depth-1, alpha, beta))
            beta = min(beta, score)

            unmake_move(game, move)

            if beta <= alpha:
                #print("CUT!!!!")
                pos_scores.append(score)
                break
            else:
                pos_scores.append(score)

                print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(pos_scores) + ": Score: " + str(score)  + ": Alpha: " + str(alpha) + ": Beta: " + str(beta))

        #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

        return min(pos_scores) if len(pos_scores) != 0 else MAX
        


def minimax(is_max, current_player, game, depth):

    res = check_game_over_full(game)
    if res != 0 or depth == 0:
        return evaluate_position(get_other_piece(current_player), game)

    pos_scores = []
    moves = generate_all_moves(game, current_player)

    for move in moves:
        make_move(game, move)

        score = minimax(not is_max, get_other_piece(current_player), game, depth-1)

        pos_scores.append(score)

        unmake_move(game, move)

        #print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(pos_scores))

    #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

    if is_max:
        return max(pos_scores)
    else:
        return min(pos_scores)
 

def minimax_with_move(is_max, current_player, game, depth):

    res = check_game_over_full(game)
    if res != 0 or depth == 0:
        return evaluate_position(get_other_piece(current_player), game)

    pos_scores = []
    moves = generate_all_moves(game, current_player)

    print("Moves: " + str(moves))

    for move in moves:
        make_move(game, move)

        score = minimax(not is_max, get_other_piece(current_player), game, depth-1)

        pos_scores.append((score, move))

        unmake_move(game, move)

        list_to_print = [x[0] for x in pos_scores]
        print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(list_to_print))
        #print("\t"*(3-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(list_to_print))

    #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

    if is_max:
        return max(pos_scores, key=lambda x: x[0])
    else:
        return min(pos_scores, key=lambda x: x[0])

def minimax_alpha_beta_with_move(is_max, current_player, game, depth, alpha, beta):

    res = check_game_over_full(game)
    if res != 0 or depth == 0:
        score = evaluate_position(current_player, game)
        #print("Evaluation score: " + str(score))
        return score, 0

    pos_scores = []
    moves = generate_all_moves(game, current_player)

    if is_max:
        for move in moves:
            score = MIN
            make_move(game, move)

            mini_or_max = minimax_alpha_beta_with_move(not is_max, get_other_piece(current_player), game, depth-1, alpha, beta)
            #print("Minimax: " + str(mini_or_max))
            score = max(score, mini_or_max[0])
            #print("Score: " + str(score))
            alpha = max(alpha, score)
            #print("Alpha: " + str(alpha))

            unmake_move(game, move)

            if alpha >= beta:
                #print("CUT!!!!")
                pos_scores.append((score, move))
                break
            else:
                pos_scores.append((score, move))

                list_to_print = [x[0] for x in pos_scores]
                #print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(list_to_print) + ": Score: " + str(score) + ": Alpha: " + str(alpha) + ": Beta: " + str(beta))

        #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

        return max(pos_scores, key=lambda x: x[0]) if len(pos_scores) != 0 else (MIN, 0)
    else:
        for move in moves:
            score = MAX
            make_move(game, move)

            mini_or_max = minimax_alpha_beta_with_move(not is_max, get_other_piece(current_player), game, depth-1, alpha, beta)
            #print("Minimax: " + str(mini_or_max))
            score = min(score, mini_or_max[0])
            beta = min(beta, score)

            unmake_move(game, move)

            if beta <= alpha:
                #print("CUT!!!!")
                pos_scores.append((score, move))
                break
            else:
                pos_scores.append((score, move))

                list_to_print = [x[0] for x in pos_scores]
                #print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(list_to_print) + ": Score: " + str(score) + ": Alpha: " + str(alpha) + ": Beta: " + str(beta))

        #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

        return min(pos_scores, key=lambda x: x[0]) if len(pos_scores) != 0 else (MAX, 0)
        

game_ =  [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]

game__ = [
            [0, 0, 0, 2, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 2, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]

"""
start = timer()
print("Minimax: " + str(minimax(True, 1, game__, 2)))
end = timer()
delta = end-start
pprint(game__)
print("Time minimax: " + str(delta))
"""
"""
start = timer()
print("Minimax: " + str(minimax_alpha_beta_with_move(True, 1, game_, 5, MIN, MAX)))
end = timer()
delta = end-start
pprint(game)
print("Time alpha beta: " + str(delta))
"""

def game_loop():

    state =  [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]

    current_player = 1

    while True:
        
        pprint(state)

        if check_game_over_full(state):
            print("Game Over!!")
            break

        score, move = minimax_alpha_beta_with_move(True, 1, state, 6, MIN, MAX)

        print("Player: " + str(current_player))
        print("Move: " + str(move) + " with a score of " + str(score))

        make_move(state, move)

        pprint(state)

        if check_game_over_full(state):
            print("Game Over!!")
            break

        initial_x = int(input("Initial x: "))
        initial_y = int(input("Initial y: "))
        final_x = int(input("Final x: "))
        final_y = int(input("Final y: "))

        player_move = (initial_x, initial_y, final_x, final_y)

        make_move(state, player_move)


game_loop()
