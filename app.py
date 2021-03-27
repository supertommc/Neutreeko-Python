import config
import menu
import board
import threading
from openings_book import OpeningsBook


class Neutreeko:

    def __init__(self):
        self.__state = config.State.MENU
        self.__player = 1
        self.__depth_bot_1 = 4
        self.__depth_bot_2 = 4
        self.__depth_hint = 6
        self.__game_state = [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]

        self.__opening_book = OpeningsBook()
        self.__opening_book.loadOpenings("openings.txt")

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

    def get_depth_hint(self):
        return self.__depth_hint

    def set_state(self, new_state):
        self.__state = new_state

    def change_player(self):
        self.__player = 2 if self.__player == 1 else 1

    def set_game_state(self, new_game_state):
        self.__game_state = new_game_state

    def set_depth_bot(self, bot, new_depth):
        if bot == 1:
            self.__depth_bot_1 = new_depth
        elif bot == 2:
            self.__depth_bot_2 = new_depth

    def generate_hint(self):
        self.__game_board.generate_hint(self.__depth_hint)

    def process_press(self, mx, my):

        if self.__state == config.State.MENU:
            self.__game_menu.press(mx, my)

        elif self.__state == config.State.PLAYER_VS_PLAYER:
            self.__game_board.press(mx, my)

        elif self.__state == config.State.PLAYER_VS_BOT and self.__game_board.get_player_turn() == 1:
            self.__game_board.press(mx, my)

        elif self.__state == config.State.BOT_VS_PLAYER and self.__game_board.get_player_turn() == 2:
            self.__game_board.press(mx, my)

    def process_release(self):
        if self.__state == config.State.MENU:
            self.__game_menu.release()

    def process_drag(self, mx):
        if self.__state == config.State.MENU:
            self.__game_menu.drag(mx)

    def update(self):
        if self.__game_board.is_game_over() or self.__game_board.is_bot_move_processing():
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
                    move_thread = threading.Thread(target=self.__game_board.apply_bot_move, args=(self.__depth_bot_1, self.__opening_book))
                    move_thread.start()

            elif self.__game_board.get_player_turn() == 2:
                if (self.__state == config.State.PLAYER_VS_BOT) or (self.__state == config.State.BOT_VS_BOT):
                    move_thread = threading.Thread(target=self.__game_board.apply_bot_move, args=(self.__depth_bot_2, self.__opening_book))
                    move_thread.start()

        self.__game_board.check_game_over()


neutreeko = Neutreeko()
