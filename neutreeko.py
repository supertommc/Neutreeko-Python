
from pprint import pprint
import datetime
from timeit import default_timer as timer

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

    def generate_all_moves(self, game_int_1, game_int_2, piece):
        if piece == 1:
            target_game_int = game_int_1
        else:
            target_game_int = game_int_2
        game_int_full = game_int_1 | game_int_2
        ones = self.get_ones_positions(target_game_int)

        all_moves = []

        for i in ones:
            all_moves.extend(self.generate_moves(i, game_int_full))
        
        return all_moves

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
        ones = self.get_ones_positions(res)
        idx = self.find_target(ones, piece_pos)

        # Up
        if idx != 0:
            dest = ones[idx-1] + 5
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            if col != piece_pos:
                moves.append((piece_pos, col))

        
        # Down
        if idx != len(ones)-1:
            print("OLAAA")
            dest = ones[idx+1] - 5
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            c = 20 + col
            print("OLAAA")
            print(c)
            print(row)
            print(col)
            if c != piece_pos:
                moves.append((piece_pos, c))

        # Left And Right
        res = self.match_rows(row, game_int_full)
        ones = self.get_ones_positions(res)
        idx = self.find_target(ones, piece_pos)

        # Left
        if idx != 0:
            dest = ones[idx-1] + 1
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            c = 5*row
            if c != piece_pos:
                moves.append((piece_pos, c))

        
        # Right
        if idx != len(ones)-1:
            dest = ones[idx+1] - 1
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            c = 5*row+4
            if c != piece_pos:
                moves.append((piece_pos, c))

        # Diagonal Up Right Down Left
        res = self.match_diagr(diagr, game_int_full)
        ones = self.get_ones_positions(res)
        idx = self.find_target(ones, piece_pos)

        if idx != 0:
            dest = ones[idx-1] + 4
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            const = diagr + 1
            c = const+(const//5)*((const%5)+1)*4
            if c != piece_pos:
                moves.append((piece_pos, c))

        
        if idx != len(ones)-1:
            dest = ones[idx+1] - 4
            if dest != piece_pos:
                moves.append((piece_pos, dest))
        else:
            const = diagr + 1
            c = 5*const + (const//5)*((const-9)-(const%5)*5)
            if c != piece_pos:
                moves.append((piece_pos, c))

        # Diagonal Up Left Down Right
        res = self.match_diagl(diagl, game_int_full)
        ones = self.get_ones_positions(res)
        idx = self.find_target(ones, piece_pos)

        if idx != 0:
            dest = ones[idx-1] + 6
            if dest != piece_pos:
                moves.append(piece_pos, dest)
        else:
            const = diagl + 1
            c = 4 - const + 6 * (const // 5) * ((const % 5) + 1)
            if c != piece_pos:
                moves.append((piece_pos, c))

        if idx != len(ones)-1:
            dest = ones[idx+1] - 6
            if dest != piece_pos:
                moves.append(piece_pos, dest)
        else:
            const = diagl + 1
            c = 4 + 5 * const - (const // 5) * ((const % 5) + 1) * 6
            if c != piece_pos:
                moves.append((piece_pos, c))

        return moves




"""

                        1
            
            x       y       z       w
        c v         


"""

def clear_bit(value, bit):
    return value & ~(1<<bit)

def make_move(game_int_1, game_int_2, move):
    initial, destination = move
    mask = 1 << initial
    if game_int_1 & mask != 0:
        game_int_1 = clear_bit(game_int_1, initial)
        game_int_1 = game_int_1 | (1<<destination)
    elif game_int_2 & mask != 0:
        game_int_2 = clear_bit(game_int_2, initial)
        game_int_2 = game_int_2 | (1<<destination)

    return game_int_1, game_int_2

def unmake_move(game_int_1, game_int_2, move):
    initial, destination = move
    mask = 1 << destination
    if game_int_1 & mask != 0:
        game_int_1 = clear_bit(game_int_1, destination)
        game_int_1 = game_int_1 | (1<<initial)
    elif game_int_2 & mask != 0:
        game_int_2 = clear_bit(game_int_2, destination)
        game_int_2 = game_int_2 | (1<<initial)

    return game_int_1, game_int_2


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
 



game_ =  [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]
"""
t = game_to_int(game, 1)
t1 = game_to_int(game, 2)
full = t | t1
print(bin(full))
print()
print()
pprint(game)

print("Full: " + str(bin(full)))
print("t: " + str(bin(t)))
print("t1: " + str(bin(t1)))
print()
t, t1 = make_move(t, t1, (1, 2))
full = t | t1
print("Full: " + str(bin(full)))
print("t: " + str(bin(t)))
print("t1: " + str(bin(t1)))
print()
t, t1 = unmake_move(t, t1, (1, 2))
full = t | t1
print("Full: " + str(bin(full)))
print("t: " + str(bin(t)))
print("t1: " + str(bin(t1)))
"""

# ...




t = game_to_int(game, 1)
t1 = game_to_int(game, 2)
full = t | t1
generator = MoveGenerator()
start = timer()
moves = generator.generate_all_moves(t, t1, 1)
end = timer()
delta = end-start
pprint(game)
print(moves)
print("Time: " + str(delta))
#print("Minimax: " + str(minimax(True, 1, game_, 4)))

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
"""
t = game_to_int(game, 1)
t1 = game_to_int(game, 2)
full = t | t1

print()
print()

pprint(game)
print()
generator = MoveGenerator()
generator.generate_moves(23, full)
"""


"""
game_ =  [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]
"""
