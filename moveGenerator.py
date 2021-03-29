
from gameUtils import GameUtils

class MoveGenerator:
    # Generates all possible moves for one of the pieces on the board
    def generate_moves(game, piece_pos):

        x, y = piece_pos

        if game[y][x] == 0:
            return False

        moves = []

        # Up and Down
        new_y = y + 1
        if new_y != 5:
            while GameUtils.valid_coord(new_y) and game[new_y][x] == 0:
                new_y += 1
            if new_y-1 != y:
                moves.append((x, y, x, new_y-1))

        new_y = y - 1
        if new_y != -1:
            while GameUtils.valid_coord(new_y) and game[new_y][x] == 0:
                new_y -= 1
            if new_y+1 != y:
                moves.append((x, y, x, new_y+1))

        # Left and Right
        new_x = x + 1
        if new_x != 5:
            while GameUtils.valid_coord(new_x) and game[y][new_x] == 0:
                new_x += 1
            if new_x-1 != x:
                moves.append((x, y, new_x-1, y))

        new_x = x - 1
        if new_x != -1:
            while GameUtils.valid_coord(new_x) and game[y][new_x] == 0:
                new_x -= 1
            if new_x+1 != x:
                moves.append((x, y, new_x+1, y))

        # Diagonal Up Right
        new_y = y - 1
        new_x = x + 1
        if new_x != 5 and new_y != -1:
            while GameUtils.valid_coords(new_x, new_y) and game[new_y][new_x] == 0:
                new_y -= 1
                new_x += 1
            if GameUtils.different_move(x, y, new_x-1, new_y+1):
                moves.append((x, y, new_x-1, new_y+1))

        # Diagonal Down Right
        new_y = y + 1
        new_x = x + 1
        if new_x != 5 and new_y != 5:
            while GameUtils.valid_coords(new_x, new_y) and game[new_y][new_x] == 0:
                new_y += 1
                new_x += 1
            if GameUtils.different_move(x, y, new_x-1, new_y-1):
                moves.append((x, y, new_x-1, new_y-1))
            
        # Diagonal Up Left
        new_y = y - 1
        new_x = x - 1
        if new_x != -1 and new_y != -1:
            while GameUtils.valid_coords(new_x, new_y) and game[new_y][new_x] == 0:
                new_y -= 1
                new_x -= 1
            if GameUtils.different_move(x, y, new_x+1, new_y+1):
                moves.append((x, y, new_x+1, new_y+1))

        # Diagonal Down Left
        new_y = y + 1
        new_x = x - 1
        if new_x != -1 and new_y != 5:
            while GameUtils.valid_coords(new_x, new_y) and game[new_y][new_x] == 0:
                new_y += 1
                new_x -= 1
            if GameUtils.different_move(x, y, new_x+1, new_y-1):
                moves.append((x, y, new_x+1, new_y-1))

        return moves

    # Generates all possible moves for a certain player
    def generate_all_moves(game, piece):
        moves = []
        for i in range(len(game)):
            for j in range(len(game[0])):
                if game[i][j] == piece:
                    moves.extend(MoveGenerator.generate_moves(game, (j, i)))
        return moves