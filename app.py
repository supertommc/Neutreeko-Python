import config
import menu
import board
import ai
import gameUtils
from pprint import pprint


class Neutreeko:

    def __init__(self):
        self.__state = config.State.MENU
        self.__player = 1
        self.__depth = 6
        self.__game_state = [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]
        self.__game_menu = menu.Menu()
        self.__game_board = board.Board(self.__game_state, self)

        self.__bot_1 = ai.AI()
        self.__bot_2 = ai.AI()

    def get_state(self):
        return self.__state

    def get_player(self):
        return self.__player

    def get_depth(self):
        return self.__depth

    def get_game_state(self):
        return self.__game_state

    def get_menu(self):
        return self.__game_menu

    def get_board(self):
        return self.__game_board

    def set_state(self, new_state):
        self.__state = new_state

    def change_player(self):
        self.__player = 2 if self.__player == 1 else 1

    def set_depth(self, new_depth):
        self.__depth = new_depth

    def set_game_state(self, new_game_state):
        self.__game_state = new_game_state

    def process_press(self, mx, my):

        if self.__state == config.State.MENU:
            self.__game_menu.press(mx, my)

        elif self.__state == config.State.PLAYER_VS_PLAYER:
            self.__game_board.press(mx, my)

        elif self.__state == config.State.PLAYER_VS_BOT:
            self.__game_board.press(mx, my)

        elif self.__state == config.State.BOT_VS_PLAYER:
            self.__game_board.press(mx, my)

        elif self.__state == config.State.BOT_VS_BOT:
            self.__game_board.press(mx, my)

    def update(self):

        if gameUtils.GameUtils.check_game_over_full(self.__game_board.get_state()):
            return

        move = self.__game_board.get_move()

        if move.is_happening():

            if move.piece_reach_dest_position():
                self.__game_board.finish_piece_move()

            else:
                move.update_piece_position()

        else:
            if self.__game_board.get_player_turn() == 1:
                if (self.__state == config.State.BOT_VS_PLAYER) or (self.__state == config.State.BOT_VS_BOT):

                    print("Board input:")
                    pprint(self.__game_board.get_state())
                    score, move = self.__bot_1.minimax_alpha_beta_with_move(True, self.__game_board.get_player_turn(), self.__game_board.get_state(), self.__depth, self.__bot_1.MIN, self.__bot_1.MAX)
                    print("Player: 1")
                    print("Move: " + str(move) + " with a score of " + str(score))
                    self.__game_board.apply_move(move)
                    print("Player 2")

            elif self.__game_board.get_player_turn() == 2:
                if (self.__state == config.State.PLAYER_VS_BOT) or (self.__state == config.State.BOT_VS_BOT):

                    print("Board input:")
                    pprint(self.__game_board.get_state())
                    print(self.__depth)
                    score, move = self.__bot_2.minimax_alpha_beta_with_move(True, self.__game_board.get_player_turn(), self.__game_board.get_state(), self.__depth, self.__bot_2.MIN, self.__bot_2.MAX)
                    print("Player: 2")
                    print("Move: " + str(move) + " with a score of " + str(score))
                    self.__game_board.apply_move(move)
                    print("Player 1")

        if gameUtils.GameUtils.check_game_over_full(self.__game_board.get_state()):
            print("GAME OVER! Player: {} lost!".format(self.__game_board.get_player_turn()))



neutreeko = Neutreeko()
