
from pprint import pprint
from gameUtils import GameUtils
from ai import AI
from moveGenerator import MoveGenerator

class Game:

    def __init__(self):
        self.state = [
                        [0, 2, 0, 2, 0],
                        [0, 1, 1, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 2, 0, 0],
                        [0, 0, 0, 1, 0]
                    ]

        self.played_states = []
        self.played_moves = []
    
    def store_current_position(self):
        self.played_states.append(GameUtils.full_game_to_tuple(self.state))

    def store_move(self, move):
        self.played_moves.append(move)


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

            if move in valid_moves:
                is_valid = True
        
        return move

    def game_loop(self):

        current_player = 1

        bot = AI()

        while True:
            
            pprint(self.state)

            if GameUtils.check_game_over_full(self.state):
                print("Game Over!!")
                break

            score, move = bot.minimax_alpha_beta_with_move(True, 1, self.state, 6, bot.MIN, bot.MAX)

            print("Player: " + str(current_player))
            print("Move: " + str(move) + " with a score of " + str(score))

            self.store_current_position()
            self.store_move(move)

            GameUtils.make_move(self.state, move)

            pprint(self.state)

            if GameUtils.check_game_over_full(self.state):
                print("Game Over!!")
                break

            self.askForInput(2)

            player_move = (initial_x, initial_y, final_x, final_y)

            self.store_current_position()
            self.store_move(player_move)

            GameUtils.make_move(self.state, player_move)
        
