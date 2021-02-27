
from pprint import pprint

# 0 - empty
# 1 - black
# 2 - white
game =  [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]



def valid_coord(coord):
    return coord >= 0 and coord < 5

def valid_coords(x, y):
    return valid_coord(x) and valid_coord(y)

def different_move(x, y, new_x, new_y):
    return not (x == new_x and y == new_y)

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

def make_move(game, move):
    x, y, new_x, new_y = move
    piece = game[y][x]

    if piece == 0 or game[new_y][new_x] != 0:
        return False
    
    game[y][x] = 0
    game[new_y][new_x] = piece

    return True

# Piece is 1 for black and 2 for white
def game_to_int(game, piece):
    game_int = 0
    for y in range(5):
        for x in range(5):
            if game[y][x] == piece:
                game_int = game_int | (1 << 5*y+x)
    return game_int

# Piece is 1 for black and 2 for white
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



print(game_to_int(game, 1))
print(check_game_over(game_, 2))

"""
moves = generate_moves(game, (2, 1))
print(moves)
print()
print()
pprint(game)
make_move(game, moves[0])
print()
pprint(game)

"""
