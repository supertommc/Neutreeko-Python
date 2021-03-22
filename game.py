from pprint import pprint
from gameUtils import GameUtils
from ai import AI
from moveGenerator import MoveGenerator


class Game:

    def __init__(self):
        self.state = [
                        [0, 2, 0, 2, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 0],
                        [0, 1, 0, 1, 0]
                    ]

        self.played_states = {}
        self.played_moves = []
    
    def store_current_position(self):
        item = GameUtils.full_game_to_tuple(self.state)
        if item in self.played_states.keys():
            self.played_states[item] += 1
        else:
            self.played_states[item] = 1

    def store_move(self, move):
        self.played_moves.append(move)

    def check_draw(self):
        for val in self.played_states.values():
            if val == 3:
                return True
        return False

    def askForInput(self, piece):
        
        is_valid = False
        valid_moves = MoveGenerator.generate_all_moves(self.state, piece)
        move = (0, 0, 0, 0)

        while not is_valid:
            initial_x = int(input("Initial x: "))
            initial_y = int(input("Initial y: "))
            final_x = int(input("Final x: "))
            final_y = int(input("Final y: "))

            move = (initial_x, initial_y, final_x, final_y)

            is_valid = True

            if move in valid_moves:
                is_valid = True
        
        return move

    def ask_for_input_alt(self, piece):
        initial_x = int(input("Initial x: "))
        initial_y = int(input("Initial y: "))
        final_x = int(input("Final x: "))
        final_y = int(input("Final y: "))

        move = (initial_x, initial_y, final_x, final_y)

        return move

    def game_loop(self):

        current_player = 1

        bot1 = AI(1)
        bot2 = AI(2)

        while True:
            
            pprint(self.state)

            if GameUtils.check_game_over_full(self.state):
                print("Game Over!!")
                break

            
            player_move = self.ask_for_input_alt(1)

            self.store_current_position()
            self.store_move(player_move)

            score, move = bot1.minimax_alpha_beta_with_move_faster(True, 1, self.state, 6, -999999, 999999)
            print("Move: " + str(move) + " with a score of " + str(score))

            GameUtils.make_move(self.state, player_move)

            print("Player: " + str(current_player))

            pprint(self.state)

            if GameUtils.check_game_over_full(self.state):
                print("Game Over!!")
                break

            player_move = self.ask_for_input_alt(2)

            score, move = bot2.minimax_alpha_beta_with_move_faster(True, 2, self.state, 6, -999999, 999999)
            print("Move: " + str(move) + " with a score of " + str(score))

            self.store_current_position()
            self.store_move(player_move)

            GameUtils.make_move(self.state, player_move)
