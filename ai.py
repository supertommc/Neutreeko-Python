
from gameUtils import GameUtils
from moveGenerator import MoveGenerator

class AI:

    def __init__(self):
        self.rel_scores = [
                                [1, 2, 2, 2, 1],
                                [2, 3, 3, 3, 2],
                                [2, 3, 5, 3, 2],
                                [2, 3, 3, 3, 2],
                                [1, 2, 2, 2, 1]
                            ]

        self.MAX = 99999999
        self.MIN = -99999999

    """
        peças no centro
        peças juntas sem estarem cercadas
        peças do adversario no meio das tuas peças
        casas que tu controlas e o adversario nao
    """
    def evaluate_position(self, piece, game):

        other_piece = GameUtils.get_other_piece(piece)

        if GameUtils.check_game_over(game, 1):
            return 10000
        elif GameUtils.check_game_over(game, 2):
            return -10000
        else:
            val = 0
            for i in range(len(game)):
                for j in range(len(game[0])):
                    if game[i][j] == 1:
                        val += self.rel_scores[i][j]
                    elif game[i][j] == 2:
                        val -= self.rel_scores[i][j]
            return val


    def minimax_alpha_beta(self, is_max, current_player, game, depth, alpha, beta):

        res = GameUtils.check_game_over_full(game)
        if res != 0 or depth == 0:
            return self.evaluate_position(current_player, game)

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
                    #print("CUT!!!!")
                    pos_scores.append(score)
                    break
                else:
                    pos_scores.append(score)

                    print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(pos_scores) + ": Score: " + str(score) + ": Alpha: " + str(alpha) + ": Beta: " + str(beta))

            #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

            return max(pos_scores) if len(pos_scores) != 0 else self.MIN
        else:
            for move in moves:
                score = self.MAX
                GameUtils.make_move(game, move)

                score = min(score, self.minimax_alpha_beta(not is_max, GameUtils.get_other_piece(current_player), game, depth-1, alpha, beta))
                beta = min(beta, score)

                GameUtils.unmake_move(game, move)

                if beta <= alpha:
                    #print("CUT!!!!")
                    pos_scores.append(score)
                    break
                else:
                    pos_scores.append(score)

                    print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(pos_scores) + ": Score: " + str(score)  + ": Alpha: " + str(alpha) + ": Beta: " + str(beta))

            #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

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

            #print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(pos_scores))

        #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

        if is_max:
            return max(pos_scores)
        else:
            return min(pos_scores)
    

    def minimax_with_move(self, is_max, current_player, game, depth):

        res = GameUtils.check_game_over_full(game)
        if res != 0 or depth == 0:
            return self.evaluate_position(get_other_piece(current_player), game)

        pos_scores = []
        moves = MoveGenerator.generate_all_moves(game, current_player)

        print("Moves: " + str(moves))

        for move in moves:
            GameUtils.make_move(game, move)

            score = self.minimax(not is_max, GameUtils.get_other_piece(current_player), game, depth-1)

            pos_scores.append((score, move))

            GameUtils.unmake_move(game, move)

            list_to_print = [x[0] for x in pos_scores]
            print("\t"*(2-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(list_to_print))
            #print("\t"*(3-depth) + ": " + str(is_max) +  ": " + str(current_player) + ": " + str(move) + ": " + str(list_to_print))

        #print("\t"*(4-depth) + ": " + str(is_max) +  ": " + str(current_player) + " : " + str(len(pos_scores)) + " : " + str(pos_scores))

        if is_max:
            return max(pos_scores, key=lambda x: x[0])
        else:
            return min(pos_scores, key=lambda x: x[0])

    def minimax_alpha_beta_with_move(self, is_max, current_player, game, depth, alpha, beta):

        res = GameUtils.check_game_over_full(game)
        if res != 0 or depth == 0:
            score = self.evaluate_position(current_player, game)
            #print("Evaluation score: " + str(score))
            return score, 0

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