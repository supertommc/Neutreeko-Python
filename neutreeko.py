
from pprint import pprint
import datetime

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


class MoveGenerator:

    col1 = 0b0000100001000010000100001
    col2 = 0b0001000010000100001000010
    col3 = 0b0010000100001000010000100
    col4 = 0b0100001000010000100001000
    col5 = 0b1000010000100001000010000
    cols = [col1, col2, col3, col4, col5]

    row1 = 0b0000000000000000000011111
    row2 = 0b0000000000000001111100000
    row3 = 0b0000000000111110000000000
    row4 = 0b0000011111000000000000000
    row5 = 0b1111100000000000000000000
    rows = [row1, row2, row3, row4, row5]

    #         X
    #       X       Estas diagonais
    #     X
    diagr1 = 0b0000000000000000000100010
    diagr2 = 0b0000000000000010001000100
    diagr3 = 0b0000000001000100010001000
    diagr4 = 0b0000100010001000100010000
    diagr5 = 0b0001000100010001000000000
    diagr6 = 0b0010001000100000000000000
    diagr7 = 0b0100010000000000000000000
    diagrs = [diagr1, diagr2, diagr3, diagr4, diagr5, diagr6, diagr7]

    #     X
    #       X       Estas diagonais
    #         X
    diagl1 = 0b0000000000000001000001000
    diagl2 = 0b0000000000100000100000100
    diagl3 = 0b0000010000010000010000010
    diagl4 = 0b1000001000001000001000001
    diagl5 = 0b0100000100000100000100000
    diagl6 = 0b0010000010000010000000000
    diagl7 = 0b0001000001000000000000000
    diagls = [diagl1, diagl2, diagl3, diagl4, diagl5, diagl6, diagl7]

    def __init__(self):
        pass

        """
        game =  [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]
        """
    def find_col(self, piece_pos):
        return piece_pos % 5

    def find_row(self, piece_pos):
        return piece_pos // 5

    def find_diagr(self, col, row):
        if (row == 0 and (col == 0 or col == 4)) or (row == 4 and(col == 0 or col == 4)):
            return -1

        return col + row - 1

    def find_diagl(self, col, row):
        if (row == 0 and (col == 0 or col == 4)) or (row == 4 and(col == 0 or col == 4)):
            return -1
        
        return (4-col) + row - 1

    def match_cols(self, col, game_int_full):
        return self.cols[col] & game_int_full
    
    def match_rows(self, row, game_int_full):
        return self.rows[row] & game_int_full

    def match_diagr(self, diagr, game_int_full):
        return self.diagrs[diagr] & game_int_full
    
    def match_diagl(self, diagl, game_int_full):
        return self.diagls[diagl] & game_int_full

    def find_target(self, list, target):
        for i in range(len(list)):
            if list[i] == target:
                return i
        
    def get_ones_positions(self, game_int):
        i = 1
        pos = 0
        positions = []
        for j in range(25):
            if i & game_int != 0:
                positions.append(pos)
            i = i << 1
            pos += 1
        
        return positions

    def generate_all_moves(self, game_int_1, game_int_2):
        game_int_full = game_int_1 | game_int_2

    def generate_moves(self, piece_pos, game_int_full):
        moves = []
        mask = 1

        if game_int_full & (mask << piece_pos) == 0:
            return False

        col = self.find_col(piece_pos)
        row = self.find_row(piece_pos)
        diagr = self.find_diagr(col, row)
        diagl = self.find_diagl(col, row)
        
        # Up and Down
        res = self.match_cols(col, game_int_full)

        print(bin(res))

        ones = self.get_ones_positions(res)

        print(ones)

        idx = self.find_target(ones, piece_pos)

        print(idx)

        # Up
        if idx != 0:
            dest = ones[idx-1] + 5
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            moves.append((piece_pos, col))

        # Down
        if idx != len(ones)-1:
            dest = ones[idx+1] - 5
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            moves.append((piece_pos, 5*(row+1)+col))

        # Left And Right
        res = self.match_rows(row, game_int_full)
        print(bin(res))
        ones = self.get_ones_positions(res)
        print(ones)
        idx = self.find_target(ones, piece_pos)
        print(idx)

        # Left
        if idx != 0:
            dest = ones[idx-1] + 1
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            moves.append((piece_pos, 5*row))

        # Right
        if idx != len(ones)-1:
            dest = ones[idx+1] - 1
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            moves.append((piece_pos, 5*row+4))

        # Diagonal Up Right Down Left
        res = self.match_diagr(diagr, game_int_full)
        print("Res:")
        print(bin(res))
        ones = self.get_ones_positions(res)
        print(ones)
        idx = self.find_target(ones, piece_pos)
        print(idx)
        print(piece_pos)
        print("Diagr: " + str(diagr))

        if idx != 0:
            dest = ones[idx-1] - 4
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            moves.append((piece_pos, (diagr+1)*4) + col)

        if idx != len(ones)-1:
            dest = ones[idx+1]+4
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            moves.append((piece_pos, piece_pos - (diagr+1)*4))

        print(moves)



"""

    peças no centro
    peças juntas sem estarem cercadas
    peças do adversario no meio das tuas peças
    casas que tu controlas e o adverario nao


"""

"""

                        1
            
            x       y       z       w
        c v         


"""


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

def generate_moves_faster(game_int, piece_pos):
    
    mask = 1

    print(bin(game_int))
    print(piece_pos)


    if game_int & (mask << piece_pos) == 0:
        return False

    moves = []

    # Up

    if piece_pos > 4:
        pos = piece_pos-5
        print(pos)
        mask = mask << (pos)
        while game_int & mask == 0 and pos_valid(pos):
            mask = mask >> 5
            pos-= 5
        pos += 5
        if pos != piece_pos:
            moves.append((piece_pos, pos))
            
    # Down
    pos = piece_pos+5
    mask = mask << (pos)
    print(bin(mask))
    print(pos)
    if piece_pos < 20:
        while game_int & mask == 0 and pos_valid(pos):
            mask = mask << 5
            pos += 5
            print(bin(mask))
            print(pos)
        pos -= 5
        if pos != piece_pos:
            moves.append((piece_pos, pos))

    # Left
    return moves


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

def check_game_over_full(game):
    if check_game_over(game, 1):
        return 1
    elif check_game_over(game, 2):
        return 2
    else:
        return 0

def get_other_piece(piece):
    return 1 if piece == 2 else 2

def evaluate_position(piece, game):
    if check_game_over(game, piece):
        return 1
    else:
        return 0
    

def minimax(is_max, current_player, game, depth):
    #print(depth)
    #print(is_max)

    res = check_game_over_full(game)
    #print("Res: " + str(res))
    #print("Current Player: " + str(current_player))
    if res != 0:
        #print("Game Over!!")
        print("\t"*(4-depth) + ": " + str(current_player))
        if res != current_player:
            return 1
        else:
            return -1

    if depth == 0:
        print("\t"*(4-depth) + ": " + str(current_player))
        return 0
    
    pos_scores = []
    moves = generate_all_moves(game, current_player)
    for move in moves:
        #print("Move: ")
        #print(move)
        make_move(game, move)

        #pprint(game)

        score = minimax(not is_max, get_other_piece(current_player), game, depth-1)
        #print("Score of depth {}: {}".format(depth, score))
        #print()
        pos_scores.append(score)

        unmake_move(game, move)

    print("\t"*(4-depth) + ": " + str(current_player) + " : " + str(len(moves)) + " : " + str(len(pos_scores)))

    if is_max:
        return max(pos_scores)
    else:
        return min(pos_scores)
    
"""
    if is_max:
        return max(scores)
    else return min(scores)
"""


game_ =  [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]

t = game_to_int(game, 1)
t1 = game_to_int(game, 2)
full = t | t1
print(bin(t))
print(get_ones_positions(t))
print()
print()
pprint(game)
print(generate_moves_faster(full, 21))

"""
start_time = datetime.datetime.now()
print(generate_all_moves(game, 1))
end_time = datetime.datetime.now()
delta = end_time-start_time
print("Time: " + str(delta))
#print("Minimax: " + str(minimax(True, 1, game_, 4)))
"""
"""
pprint(game_)
make_move(game_, (1, 0, 0, 1))
pprint(game_)
unmake_move(game_, (1, 0, 0, 1))
pprint(game_)
"""

#print(generate_all_moves(game_, 2))

#print(bin(game_to_int(game, 1)))
#print(check_game_over(game_, 2))

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


print()
print()

pprint(game)
print()
generator = MoveGenerator()
generator.generate_moves(1, full)



"""
game_ =  [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]
"""
