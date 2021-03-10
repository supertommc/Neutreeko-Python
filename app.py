import config
import menu
import board


class Neutreeko:

    def __init__(self):
        self.__state = config.State.MENU
        self.__player = 1
        self.__depth_bot_1 = 7
        self.__depth_bot_2 = 5
        self.__game_state = [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]
        self.__game_menu = menu.Menu()
        self.__game_board = board.Board(self.__game_state)

    def get_state(self):
        return self.__state

    def get_player(self):
        return self.__player

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

        if self.__game_board.is_game_over() or self.__game_board.is_draw():
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
                    self.__game_board.apply_bot_move(self.__depth_bot_1)

            elif self.__game_board.get_player_turn() == 2:
                if (self.__state == config.State.PLAYER_VS_BOT) or (self.__state == config.State.BOT_VS_BOT):
                    self.__game_board.apply_bot_move(self.__depth_bot_2)

        if self.__game_board.is_game_over():
            print("GAME OVER! Player: {} lost!".format(self.__game_board.get_player_turn()))

        elif self.__game_board.is_draw():
            print("DRAW!")


neutreeko = Neutreeko()
