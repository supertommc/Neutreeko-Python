import config
import menu
import board


class Newtreeko:

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
        self.__game_board = board.Board(self.__game_state)

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


newtreeko = Newtreeko()
