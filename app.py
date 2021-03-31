import config
import menu
import board
from ai import AI
from openings_book import OpeningsBook


class Neutreeko:
    """
        Main Model Application Class
        This class has everything used in the application, including the main and options menus and the game board
    """

    def __init__(self):
        self.__state = config.State.MAIN_MENU
        self.__player = 1

        self.__depth_hint = 6
        self.__depth_bot_1 = 4
        self.__depth_bot_2 = 4

        self.__initial_depth_hint_index = self.__depth_hint - 1
        self.__initial_depth_bot_1_index = self.__depth_bot_1 - 1
        self.__initial_depth_bot_2_index = self.__depth_bot_2 - 1

        self.__initial_evaluation_index = 0

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

        self.__bot_1_evaluation_function = None

        self.__player_bots = {1: AI(1), 2: AI(2)}
        self.__hint_bots = {1: AI(1), 2: AI(2)}

        # 0 - hint ; 1 - depth_bot_1 ; 2 - depth_bot_2
        self.__depth_bots = [6, 4, 4]

        # self.__bot_1 = AI(1)
        # self.__bot_2 = AI(2)
        #
        # self.__hint_1 = AI(1)
        # self.__hint_2 = AI(2)

        self.__main_menu = menu.MainMenu()
        self.__options_menu = menu.OptionsMenu(self.__use_opening_book, self.__initial_depth_hint_index, self.__initial_depth_bot_1_index, self.__initial_depth_bot_2_index, self.__initial_evaluation_index)
        self.__game_board = board.Board(self.__opening_book, self.__game_state)

        # self.__bot_thread = None
        # self.__hint_thread = None

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

    def get_player_bots(self):
        return self.__player_bots

    def get_hint_bots(self):
        return self.__hint_bots

    # def join_hint_thread(self):
    #     if self.__hint_thread is not None:
    #         self.__hint_thread.join()
    #         self.__hint_thread = None

    def set_state(self, new_state):
        self.__state = new_state

    def set_depth_bot(self, bot, new_depth):
        # if bot == 0:
        #     self.__depth_hint = new_depth
        # elif bot == 1:
        #     self.__depth_bot_1 = new_depth
        # elif bot == 2:
        #     self.__depth_bot_2 = new_depth

        self.__depth_bots[bot] = new_depth

    # def set_hint_thread(self, hint_thread):
    #     self.__hint_thread = hint_thread

    def set_use_opening_book(self, new_use_opening_book):
        self.__use_opening_book = new_use_opening_book

    def generate_hint(self):
        self.__game_board.generate_hint(self.__depth_hint, self.__hint_bots)

    def reset_board(self):
        self.__game_board = board.Board(self.__opening_book, self.__game_state)

    def process_press(self, mx, my):
        """ Process mouse press event for each application element

        :param mx: x coord of mouse
        :param my: y coord of mouse
        """

        if self.__state == config.State.MAIN_MENU:
            self.__main_menu.press(mx, my)

        elif self.__state == config.State.OPTIONS_MENU:
            self.__options_menu.press(mx, my)

        else:
            self.__game_board.press(mx, my)

        # elif self.__state == config.State.PLAYER_VS_PLAYER:
        #     self.__game_board.press(mx, my)
        #
        # elif self.__state == config.State.PLAYER_VS_BOT and self.__game_board.get_player_turn() == 1:
        #     self.__game_board.press(mx, my)
        #
        # elif self.__state == config.State.BOT_VS_PLAYER and self.__game_board.get_player_turn() == 2:
        #     self.__game_board.press(mx, my)

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
            # if self.__bot_thread is not None:
            #     self.__bot_thread.join()
            #     self.__bot_thread = None
            # if self.__game_board.get_player_turn() == 1:
            #     if (self.__state == config.State.BOT_VS_PLAYER) or (self.__state == config.State.BOT_VS_BOT):
            #         if self.__use_opening_book:
            #             self.__game_board.apply_bot_move(self.__depth_bots, self.__player_bots, self.__opening_book)
            #         else:
            #             self.__game_board.apply_bot_move(self.__depth_bots, self.__player_bots, None)
            #
            # elif self.__game_board.get_player_turn() == 2:
            #     if (self.__state == config.State.PLAYER_VS_BOT) or (self.__state == config.State.BOT_VS_BOT):
            #         if self.__use_opening_book:
            #             self.__game_board.apply_bot_move(self.__depth_bots, self.__player_bots, self.__opening_book)
            #         else:
            #             self.__game_board.apply_bot_move(self.__depth_bots, self.__player_bots, None)

            first_condition = (self.__game_board.get_player_turn() == 1) and (self.__state == config.State.BOT_VS_PLAYER)
            second_condition = (self.__game_board.get_player_turn() == 2) and (self.__state == config.State.PLAYER_VS_BOT)
            third_condition = self.__state == config.State.BOT_VS_BOT

            if first_condition or second_condition or third_condition:
                if self.__use_opening_book:
                    self.__game_board.apply_bot_move(self.__depth_bots, self.__player_bots, self.__opening_book)
                else:
                    self.__game_board.apply_bot_move(self.__depth_bots, self.__player_bots, None)

        self.__game_board.check_game_over()


neutreeko = Neutreeko()
