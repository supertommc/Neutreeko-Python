from gameUtils import GameUtils
from moveGenerator import MoveGenerator


class AI:

    MAX = 99999999
    MIN = -99999999

    WIN_SCORE = 10000
    LOSE_SCORE = -10000
    MAX_SCORE_NOT_WIN = 5
    MIN_SCORE_NOT_LOSE = -5

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

    def check_all_neighbours(self, game):
        val = 0
        for i in range(len(game)):
            for j in range(len(game[0])):
                if game[i][j] == self.piece:
                    val += self.check_neighbours((i, j), game)
                    val += self.rel_scores[i][j]
                elif game[i][j] == self.other_piece:
                    val -= self.check_neighbours((i, j), game)
                    val -= self.rel_scores[i][j]
        return val

    def evaluate_position(self, piece, game, depth):

        if GameUtils.check_game_over(game, self.piece):
            return AI.WIN_SCORE + depth
        elif GameUtils.check_game_over(game, self.other_piece):
            return AI.LOSE_SCORE - depth
        else:
            return self.check_all_neighbours(game)
            #return 0 + random.randint(AI.MIN_SCORE_NOT_LOSE, AI.MAX_SCORE_NOT_WIN)
            """
            val = 0
            for i in range(len(game)):
                for j in range(len(game[0])):
                    if game[i][j] == self.piece:
                        val += self.rel_scores[i][j]
                    elif game[i][j] == self.other_piece:
                        val -= self.rel_scores[i][j]
            return val
            """
            


    def minimax_alpha_beta(self, is_max, current_player, game, depth, alpha, beta):

        res = self.evaluate_position(current_player, game)
        if res >= 10000 or res <= 10000 or depth == 0:
            return res

        pos_scores = []
        moves = MoveGenerator.generate_all_moves(game, current_player)

        if is_max:
            for move in moves:
                score = self.MIN
                GameUtils.make_move(game, move)

                score = max(score, self.minimax_alpha_beta(not is_max, GameUtils.get_other_piece(current_player), game, depth-1, alpha, beta))
                alpha = max(alpha, score)

                GameUtils.unmake_move(game, move)

                if alpha >= beta:
                    pos_scores.append(score)
                    break
                else:
                    pos_scores.append(score)

            return max(pos_scores) if len(pos_scores) != 0 else self.MIN
        else:
            for move in moves:
                score = self.MAX
                GameUtils.make_move(game, move)

                score = min(score, self.minimax_alpha_beta(not is_max, GameUtils.get_other_piece(current_player), game, depth-1, alpha, beta))
                beta = min(beta, score)

                GameUtils.unmake_move(game, move)

                if beta <= alpha:
                    pos_scores.append(score)
                    break
                else:
                    pos_scores.append(score)

            return min(pos_scores) if len(pos_scores) != 0 else self.MAX
            


    def minimax(self, is_max, current_player, game, depth):

        res = GameUtils.check_game_over_full(game)
        if res != 0 or depth == 0:
            return self.evaluate_position(get_other_piece(current_player), game)

        pos_scores = []
        moves = MoveGenerator.generate_all_moves(game, current_player)

        for move in moves:
            GameUtils.make_move(game, move)

            score = self.minimax(not is_max, GameUtils.get_other_piece(current_player), game, depth-1)

            pos_scores.append(score)

            GameUtils.unmake_move(game, move)

        if is_max:
            return max(pos_scores)
        else:
            return min(pos_scores)
    

    def minimax_with_move(self, is_max, current_player, game, depth):


        res = self.evaluate_position(current_player, game, depth)
        if res >= 50 or res <= -50 or depth == 0:
            return res, 0

        pos_scores = []
        moves = MoveGenerator.generate_all_moves(game, current_player)

        for move in moves:
            GameUtils.make_move(game, move)

            score = self.minimax_with_move(not is_max, GameUtils.get_other_piece(current_player), game, depth-1)[0]

            pos_scores.append((score, move))

            GameUtils.unmake_move(game, move)

        if is_max:
            return max(pos_scores, key=lambda x: x[0])
        else:
            return min(pos_scores, key=lambda x: x[0])

    def minimax_alpha_beta_with_move(self, is_max, current_player, game, depth, alpha, beta):

        res = GameUtils.check_game_over_full(game)
        if res != 0 or depth == 0:
            score = self.evaluate_position(current_player, game, depth)
            #print("Evaluation score: " + str(score))
            return score, 0


        """
        res = self.evaluate_position(current_player, game, depth)
        if res >= 10000 or res <= 10000 or depth == 0:
            return res, 0
        """

        pos_scores = []
        moves = MoveGenerator.generate_all_moves(game, current_player)

        if is_max:
            for move in moves:
                score = self.MIN
                GameUtils.make_move(game, move)

                mini_or_max = self.minimax_alpha_beta_with_move(not is_max, GameUtils.get_other_piece(current_player), game, depth-1, alpha, beta)
                #print("Minimax: " + str(mini_or_max))
                score = max(score, mini_or_max[0])
                #print("Score: " + str(score))
                alpha = max(alpha, score)
                #print("Alpha: " + str(alpha))

                GameUtils.unmake_move(game, move)

                if alpha >= beta:
                    #print("CUT!!!!")
                    pos_scores.append((score, move))
                    break
                else:
                    pos_scores.append((score, move))

                    list_to_print = [x[0] for x in pos_scores]
                    #print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(list_to_print) + ": Score: " + str(score) + ": Alpha: " + str(alpha) + ": Beta: " + str(beta))

            #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

            return max(pos_scores, key=lambda x: x[0]) if len(pos_scores) != 0 else (self.MIN, 0)
        else:
            for move in moves:
                score = self.MAX
                GameUtils.make_move(game, move)

                mini_or_max = self.minimax_alpha_beta_with_move(not is_max, GameUtils.get_other_piece(current_player), game, depth-1, alpha, beta)
                #print("Minimax: " + str(mini_or_max))
                score = min(score, mini_or_max[0])
                beta = min(beta, score)

                GameUtils.unmake_move(game, move)

                if beta <= alpha:
                    #print("CUT!!!!")
                    pos_scores.append((score, move))
                    break
                else:
                    pos_scores.append((score, move))

                    list_to_print = [x[0] for x in pos_scores]
                    #print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(list_to_print) + ": Score: " + str(score) + ": Alpha: " + str(alpha) + ": Beta: " + str(beta))

            #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

            return min(pos_scores, key=lambda x: x[0]) if len(pos_scores) != 0 else (self.MAX, 0)

    def minimax_alpha_beta_with_move_faster(self, is_max, current_player, game, depth, alpha, beta):

        res = self.evaluate_position(current_player, game, depth)
        if res >= 50 or res <= -50 or depth == 0:
            return res, 0
        
        moves = MoveGenerator.generate_all_moves(game, current_player)

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

    def minimax_alpha_beta_with_move_faster_order(self, is_max, current_player, game, depth, alpha, beta):

        res = self.evaluate_position(current_player, game, depth)
        if res >= 50 or res <= -50 or depth == 0:
            return res, 0
        
        moves = self.generate_all_moves_sort(game, current_player, depth, is_max)

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