from gameUtils import GameUtils
from timeit import default_timer as timer
import random
from moveGenerator import MoveGenerator

# AI Class
# Represents the ai agent
class AI:

    # Constants
    MAX = 99999999
    MIN = -99999999

    WIN_SCORE = 10000
    LOSE_SCORE = -10000
    MAX_SCORE_NOT_WIN = 10
    MIN_SCORE_NOT_LOSE = -10

    # Constructor
    def __init__(self, piece):
        self.rel_scores = [
                                [1, 2, 2, 2, 1],
                                [2, 3, 3, 3, 2],
                                [2, 3, 5, 3, 2],
                                [2, 3, 3, 3, 2],
                                [1, 2, 2, 2, 1]
                            ]

        self.MAX = 99999999
        self.MIN = -99999999
        self.piece = piece
        self.other_piece = GameUtils.get_other_piece(self.piece)
        self.num_calls = 0
        self.__current_evaluation_function = self.evaluate_position_random

    def change_current_evaluation_function(self, difficulty_string):

        if difficulty_string == "RANDOM":
            self.__current_evaluation_function = self.evaluate_position_random
        elif difficulty_string == "EASY":
            self.__current_evaluation_function = self.evaluate_easy
        elif difficulty_string == "MEDIUM":
            self.__current_evaluation_function = self.evaluate_position_center
        elif difficulty_string == "HARD":
            self.__current_evaluation_function = self.check_all_neighbours
        elif difficulty_string == "HARD++":
            self.__current_evaluation_function = self.evaluate_position_all_combined
        else:
            print("Not implement yet")


    # Verifies if there are two pieces in a row and returns a score based on that
    def check_neighbours(self, piece_pos, game):
        x, y = piece_pos
        piece = game[x][y]

        val = 0

        x_left = x-1
        x_right = x+1
        y_up = y-1
        y_down = y+1

        if x_left > 0:
            if y_up > 0 and game[x_left][y_up] == piece:
                val += 1
            if y_down < 4 and game[x_left][y_down] == piece:
                val += 1
            if game[x_left][y] == piece:
                val += 1
        if x_right < 4:
            if y_up > 0 and game[x_right][y_up] == piece:
                val += 1
            if y_down < 4 and game[x_right][y_down] == piece:
                val += 1
            if game[x_right][y] == piece:
                val += 1
        if y_up > 0 and game[x][y_up] == piece:
            val += 1
        if y_down < 4 and game[x][y_down] == piece:
            val += 1
        return val

    # Checks if the ai has two pieces in a row on the board
    def check_all_neighbours(self, game):
        val = 0
        for i in range(len(game)):
            for j in range(len(game[0])):
                if game[i][j] == self.piece:
                    val += self.check_neighbours((i, j), game)
                elif game[i][j] == self.other_piece:
                    val -= self.check_neighbours((i, j), game)
        return val

    def evaluate_easy(self, game):
        return 0

    # Combines all the evaluation functions (two-in-a-row, positional and basic) into a single one
    def evaluate_position_all_combined(self, game):
        val = 0
        for i in range(len(game)):
            for j in range(len(game[0])):
                if game[i][j] == self.piece:
                    val += self.check_neighbours((i, j), game)
                    val += self.rel_scores[i][j]
                elif game[i][j] == self.other_piece:
                    val -= self.check_neighbours((i, j), game)
                    val -= self.rel_scores[i][j]
        # return val + random.randint(-1, 1)
        return val

    def evaluate_position_center(self, game):
        val = 0
        for i in range(len(game)):
            for j in range(len(game[0])):
                if game[i][j] == self.piece:
                    val += self.rel_scores[i][j]
                elif game[i][j] == self.other_piece:
                    val -= self.rel_scores[i][j]
        return val

    def evaluate_position_random(self, game):
        return 0 + random.randint(AI.MIN_SCORE_NOT_LOSE + 1, AI.MAX_SCORE_NOT_WIN - 1)

    # Evaluates a board position
    def evaluate_position(self, piece, game, depth):

        if GameUtils.check_game_over(game, self.piece):
            return AI.WIN_SCORE + depth
        elif GameUtils.check_game_over(game, self.other_piece):
            return AI.LOSE_SCORE - depth
        else:
            return self.__current_evaluation_function(game)
            
    # Applies the minimax algorithm to the given game state with a certain depth. Returns the move with the best score (calculated by the minimax)
    def minimax_with_move(self, is_max, current_player, game, depth):

        self.num_calls += 1

        res = self.evaluate_position(current_player, game, depth)
        if res >= 50 or res <= -50 or depth == 0:
            return res, 0

        pos_scores = []
        moves = moveGenerator.generate_all_moves(game, current_player)

        for move in moves:
            GameUtils.make_move(game, move)

            score = self.minimax_with_move(not is_max, GameUtils.get_other_piece(current_player), game, depth-1)[0]

            pos_scores.append((score, move))

            GameUtils.unmake_move(game, move)

        if is_max:
            return max(pos_scores, key=lambda x: x[0])
        else:
            return min(pos_scores, key=lambda x: x[0])

    # Applies the minimax algorithm to the given game state with a certain depth. Returns the move with the best score (calculated by the minimax)
    def minimax_alpha_beta_with_move_faster(self, is_max, current_player, game, depth, alpha, beta):

        self.num_calls += 1

        res = self.evaluate_position(current_player, game, depth)
        if res >= 50 or res <= -50 or depth == 0:
            return res, 0
        
        moves = moveGenerator.generate_all_moves(game, current_player)

        if is_max:
            score = self.MIN
            current_move = (0, 0, 0, 0)
            for move in moves:
                
                GameUtils.make_move(game, move)

                mini_or_max = self.minimax_alpha_beta_with_move_faster(not is_max, GameUtils.get_other_piece(current_player), game, depth-1, alpha, beta)
                if mini_or_max[0] > score:
                    score = mini_or_max[0]
                    current_move = move
                alpha = max(alpha, score)

                GameUtils.unmake_move(game, move)

                if alpha >= beta:
                    break
        
            return score, current_move
        else:
            score = self.MAX
            current_move = (0, 0, 0, 0)
            for move in moves:
                GameUtils.make_move(game, move)

                mini_or_max = self.minimax_alpha_beta_with_move_faster(not is_max, GameUtils.get_other_piece(current_player), game, depth-1, alpha, beta)
                if mini_or_max[0] < score:
                    score = mini_or_max[0]
                    current_move = move
                beta = min(beta, score)

                GameUtils.unmake_move(game, move)

                if beta <= alpha:
                    break

            return score, current_move

    # Generates all possible moves for a certain player and sorts them based on the resulting position's evaluation
    def generate_all_moves_sort(self, game, current_player, depth, is_max):
        moves = MoveGenerator.generate_all_moves(game, current_player)
        moves_with_score = []
        for move in moves:
            GameUtils.make_move(game, move)
            moves_with_score.append((move, self.evaluate_position(current_player, game, depth)))
            GameUtils.unmake_move(game, move)
        
        if is_max:
            return list(map(lambda y: y[0], sorted(moves_with_score, key=lambda x: x[1], reverse=True)))
        else:
            return list(map(lambda y: y[0], sorted(moves_with_score, key=lambda x: x[1])))


    # Applies the minimax algorithm to the given game state with a certain depth, but sorts the possible moves before analysing their respective nodes. Returns the move with the best score (calculated by the minimax)
    def minimax_alpha_beta_with_move_faster_order(self, is_max, current_player, game, depth, alpha, beta):

        self.num_calls += 1

        res = self.evaluate_position(current_player, game, depth)
        if res >= 50 or res <= -50 or depth == 0:
            return res, 0
        
        moves = self.generate_all_moves_sort(game, current_player, depth, is_max)

        if is_max:
            score = self.MIN
            current_move = (0, 0, 0, 0)
            for move in moves:
                
                GameUtils.make_move(game, move)

                mini_or_max = self.minimax_alpha_beta_with_move_faster_order(not is_max, GameUtils.get_other_piece(current_player), game, depth-1, alpha, beta)
                if mini_or_max[0] > score:
                    score = mini_or_max[0]
                    current_move = move
                alpha = max(alpha, score)

                GameUtils.unmake_move(game, move)

                if alpha >= beta:
                    break
        
            return score, current_move
        else:
            score = self.MAX
            current_move = (0, 0, 0, 0)
            for move in moves:
                GameUtils.make_move(game, move)

                mini_or_max = self.minimax_alpha_beta_with_move_faster_order(not is_max, GameUtils.get_other_piece(current_player), game, depth-1, alpha, beta)
                if mini_or_max[0] < score:
                    score = mini_or_max[0]
                    current_move = move
                beta = min(beta, score)

                GameUtils.unmake_move(game, move)

                if beta <= alpha:
                    break

            return score, current_move