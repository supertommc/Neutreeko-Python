import config
import menu
import board
from threading import Thread
from openings_book import OpeningsBook


class Neutreeko:
    """
        Main Model Application Class
        This class has everything used in the application, including the main and options menus and the game board
    """

    def __init__(self):
        self.__state = config.State.MAIN_MENU
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
        self.__use_opening_book = True

        self.__main_menu = menu.MainMenu()
        self.__options_menu = menu.OptionsMenu()
        self.__game_board = board.Board(self.__game_state)

    def get_state(self):
        return self.__state

    def get_player(self):
        return self.__player

    def get_game_state(self):
        return self.__game_state

    def get_main_menu(self):
        return self.__main_menu

    def get_options_menu(self):
        return self.__options_menu

    def get_board(self):
        return self.__game_board

    def set_state(self, new_state):
        self.__state = new_state

    def change_player(self):
        self.__player = 2 if self.__player == 1 else 1

    def set_game_state(self, new_game_state):
        self.__game_state = new_game_state

    def set_depth_bot(self, bot, new_depth):
        if bot == 0:
            self.__depth_hint = new_depth
        elif bot == 1:
            self.__depth_bot_1 = new_depth
        elif bot == 2:
            self.__depth_bot_2 = new_depth

    def generate_hint(self):
        self.__game_board.generate_hint(self.__depth_hint)

    def process_press(self, mx, my):
        """ Process mouse press event for each application element

        :param mx: x coord of mouse
        :param my: y coord of mouse
        """

        if self.__state == config.State.MAIN_MENU:
            self.__main_menu.press(mx, my)

        elif self.__state == config.State.OPTIONS_MENU:
            self.__options_menu.press(mx, my)

        elif self.__state == config.State.PLAYER_VS_PLAYER:
            self.__game_board.press(mx, my)

        elif self.__state == config.State.PLAYER_VS_BOT and self.__game_board.get_player_turn() == 1:
            self.__game_board.press(mx, my)

        elif self.__state == config.State.BOT_VS_PLAYER and self.__game_board.get_player_turn() == 2:
            self.__game_board.press(mx, my)

    def process_release(self):
        """ Process mouse release event for each application element
        """
        if self.__state == config.State.MAIN_MENU:
            self.__main_menu.release()
        elif self.__state == config.State.OPTIONS_MENU:
            self.__options_menu.release()

    def process_drag(self, mx):
        """ Process mouse drag event for each application element

        :param mx: x coord of mouse
        """
        if self.__state == config.State.MAIN_MENU:
            self.__main_menu.drag(mx)
        elif self.__state == config.State.OPTIONS_MENU:
            self.__options_menu.drag(mx)

    def update(self):
        """ Update application animations, verify if the game ends and apply bots moves
        """
        if self.__game_board.is_game_over() or self.__game_board.is_computer_processing():
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
                    if self.__use_opening_book:
                        Thread(target=self.__game_board.apply_bot_move, args=(self.__depth_bot_1, self.__opening_book)).start()
                    else:
                        Thread(target=self.__game_board.apply_bot_move, args=(self.__depth_bot_1, None)).start()

            elif self.__game_board.get_player_turn() == 2:
                if (self.__state == config.State.PLAYER_VS_BOT) or (self.__state == config.State.BOT_VS_BOT):
                    if self.__use_opening_book:
                        Thread(target=self.__game_board.apply_bot_move, args=(self.__depth_bot_2, self.__opening_book)).start()
                    else:
                        Thread(target=self.__game_board.apply_bot_move, args=(self.__depth_bot_2, None)).start()

        self.__game_board.check_game_over()


neutreeko = Neutreeko()
