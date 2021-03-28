
class GameUtils:

    # Checks if a coordinate (x or y) is valid (inside the board).
    @staticmethod
    def valid_coord(coord):
        return coord >= 0 and coord < 5

    # Checks if a pair of coordinates (x, y) is valid
    @staticmethod
    def valid_coords(x, y):
        return GameUtils.valid_coord(x) and GameUtils.valid_coord(y)

    # Checks if two moves are different
    @staticmethod
    def different_move(x, y, new_x, new_y):
        return not (x == new_x and y == new_y)

    # Converts the game position for one of the players into an integer (encodes the player's pieces into bits in an integer)
    @staticmethod
    def game_to_int(game, piece):
        game_int = 0
        for y in range(5):
            for x in range(5):
                if game[y][x] == piece:
                    game_int = game_int | (1 << 5*y+x)
        return game_int

    # Converts the game into a tuple containing two integers, one with the position of the player 1's pieces and the other with player 2
    @staticmethod
    def full_game_to_tuple(game):
        return GameUtils.game_to_int(game, 1), GameUtils.game_to_int(game, 2)

    # Given a player's piece (1 or 2), returns the other
    @staticmethod
    def get_other_piece(piece):
        return 3-piece

    # Returns the bits of an integer that are set to one
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

    # Checks if the game is over
    @staticmethod
    def check_game_over_full(game):
        if GameUtils.check_game_over(game, 1):
            return 1
        elif GameUtils.check_game_over(game, 2):
            return 2
        else:
            return 0


    # Checks if the game is over for one player
    # Based on the following stack overflow thread
    # https://stackoverflow.com/questions/21336869/optimizing-finding-an-endgame
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

    # Makes a move on the board
    @staticmethod
    def make_move(game, move):
        x, y, new_x, new_y = move
        piece = game[y][x]

        if piece == 0 or game[new_y][new_x] != 0:
            return False
        
        game[y][x] = 0
        game[new_y][new_x] = piece

        return True

    # Unmakes a move on the board
    @staticmethod
    def unmake_move(game, move):
        x, y, new_x, new_y = move
        piece = game[new_y][new_x]

        if piece == 0 or game[y][x] != 0:
            return False
        
        game[new_y][new_x] = 0
        game[y][x] = piece

        return True
