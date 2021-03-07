
class GameUtils:

    @staticmethod
    def valid_coord(coord):
        return coord >= 0 and coord < 5

    @staticmethod
    def valid_coords(x, y):
        return GameUtils.valid_coord(x) and GameUtils.valid_coord(y)

    @staticmethod
    def different_move(x, y, new_x, new_y):
        return not (x == new_x and y == new_y)

    # Piece is 1 for black and 2 for white
    @staticmethod
    def game_to_int(game, piece):
        game_int = 0
        for y in range(5):
            for x in range(5):
                if game[y][x] == piece:
                    game_int = game_int | (1 << 5*y+x)
        return game_int

    # Piece is 1 for black and 2 for white
    @staticmethod
    def full_game_to_tuple(game):
        return GameUtils.game_to_int(game, 1), GameUtils.game_to_int(game, 2)


    @staticmethod
    def get_other_piece(piece):
        return 1 if piece == 2 else 2

    @staticmethod
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

    @staticmethod
    def check_game_over_full(game):
        if GameUtils.check_game_over(game, 1):
            return 1
        elif GameUtils.check_game_over(game, 2):
            return 2
        else:
            return 0

    @staticmethod
    def check_game_over(game, piece):
        game_int = GameUtils.game_to_int(game, piece)
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

    @staticmethod
    def make_move(game, move):
        x, y, new_x, new_y = move
        piece = game[y][x]

        if piece == 0 or game[new_y][new_x] != 0:
            return False
        
        game[y][x] = 0
        game[new_y][new_x] = piece

        return True

    @staticmethod
    def unmake_move(game, move):
        x, y, new_x, new_y = move
        piece = game[new_y][new_x]

        if piece == 0 or game[y][x] != 0:
            return False
        
        game[new_y][new_x] = 0
        game[y][x] = piece

        return True