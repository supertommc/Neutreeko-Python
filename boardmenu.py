import button
import config
import responses


class PlayerTurnMenu:

    def __init__(self, position, title_font_size, title_color):
        self.__x, self.__y = position
        self.__title_text = "PLAYER TURN"
        self.__title_font_size = title_font_size
        self.__title_color = title_color
        self.__title_width, _ = config.Config.get_font_width_height(self.__title_text, self.__title_font_size)
        self.__title_x = self.__x
        self.__title_y = self.__y

        self.__piece_x = self.__x + self.__title_width // 2
        self.__piece_y = self.__y + 100

        self.__player = 1

    def get_title_x(self):
        return self.__title_x

    def get_title_y(self):
        return self.__title_y

    def get_title_text(self):
        return self.__title_text

    def get_title_font_size(self):
        return self.__title_font_size

    def get_title_color(self):
        return self.__title_color

    def get_piece_x(self):
        return self.__piece_x

    def get_piece_y(self):
        return self.__piece_y

    def get_player(self):
        return self.__player

    def change_player_turn(self, new_player):
        self.__player = new_player


class GameOverMenu:
    def __init__(self, position, title_font_size, title_color):
        self._x, self._y = position

        self._title_text = "Game Over"
        self._title_font_size = title_font_size
        self._title_color = title_color
        self._title_x = self._x
        self._title_y = self._y

        # Description implemented in subclasses

        self._buttons_width = 420
        self._buttons_height = 50
        self._buttons_color = (0, 0, 0)
        self._buttons_background_color = (90, 90, 90)
        self._buttons_pressed_color_offset = 20
        self._buttons_font_size = 28

        self._buttons_block_y = 200
        self._buttons_offset = 20

        self._rematch_button = None
        self._rematch_button_text = "Rematch"
        self._rematch_button_response = responses.StaticResponse(config.State.PLAYER_VS_PLAYER)

        self._leave_button = None
        self._leave_button_text = "Leave"
        self._leave_button_response = responses.StaticResponse(config.State.MENU)

        self.__buttons_list = []
        self.__create_buttons()

    def __create_buttons(self):
        button_y = self._buttons_block_y
        button_x = self._x

        self.__rematch_button = button.Button((button_x, button_y), self._buttons_width,
                                              self._buttons_height, self._buttons_color,
                                              self._buttons_background_color,
                                              self._buttons_pressed_color_offset,
                                              self._rematch_button_text, self._buttons_font_size,
                                              self._rematch_button_response)
        self.__buttons_list.append(self.__rematch_button)
        button_y += self._buttons_height + self._buttons_offset

        self.__leave_button = button.Button((button_x, button_y), self._buttons_width,
                                            self._buttons_height, self._buttons_color,
                                            self._buttons_background_color,
                                            self._buttons_pressed_color_offset,
                                            self._leave_button_text, self._buttons_font_size,
                                            self._leave_button_response)
        self.__buttons_list.append(self.__leave_button)


class GameOverWinnerMenu(GameOverMenu):

    def __init__(self, position, title_font_size, title_color, winner_text_font_size, winner_text_color):
        GameOverMenu.__init__(self, position, title_font_size, title_color)

        self.__player = None

        self.__winner_text = "Winner"
        self.__winner_text_font_size = winner_text_font_size
        self.__winner_text_color = winner_text_color
        self.__winner_text_width, _ = config.Config.get_font_width_height(self._title_text, self._title_font_size)
        self.__winner_text_x = self._x
        self.__winner_text_y = self._y + 100

        self.__piece_x = self.__winner_text_width + 50
        self.__piece_y = self._y + 100

    def set_winner(self, new_player):
        self.__player = new_player


class GameOverDrawMenu(GameOverMenu):
    def __init__(self, position, title_font_size, title_color, draw_text_font_size, draw_text_color):
        GameOverMenu.__init__(self, position, title_font_size, title_color)

        self.__winner_text = "Draw"
        self.__draw_text_font_size = draw_text_font_size
        self.__draw_text_color = draw_text_color
        self.__winner_text_width, _ = config.Config.get_font_width_height(self._title_text, self._title_font_size)
        self.__draw_text_x = self._x
        self.__draw_text_y = self._y + 100


class BoardMenu:

    def __init__(self, position):
        self.__position = position
        self.__title_font_size = 50
        self.__title_color = (0, 0, 0)
        self.__winner_font_size = 40
        self.__winner_color = (0, 0, 0)
        self.__draw_description_font_size = 20
        self.__draw_description_color = (0, 0, 0)

        self.__player_turn_menu = PlayerTurnMenu(self.__position, self.__title_font_size, self.__title_color)

        self.__game_over_winner_menu = GameOverWinnerMenu(self.__position, self.__title_font_size, self.__title_color,
                                                          self.__winner_font_size, self.__winner_color)

        self.__game_over_draw_menu = GameOverDrawMenu(self.__position, self.__title_font_size, self.__title_color,
                                                      self.__draw_description_font_size, self.__draw_description_color)

        self.__menus = {
            config.BoardMenuState.PLAYER_TURN_MENU: self.__player_turn_menu,
            config.BoardMenuState.GAME_OVER_WINNER_MENU: self.__game_over_winner_menu,
            config.BoardMenuState.GAME_OVER_DRAW_MENU: self.__game_over_draw_menu
        }

        self.__current_menu = self.__player_turn_menu
        self.__current_state = config.BoardMenuState.PLAYER_TURN_MENU

    def get_current_state(self):
        return self.__current_state

    def change_player_turn(self, new_player):
        self.__player_turn_menu.change_player_turn(new_player)

    def set_winner(self, new_player):
        self.__game_over_winner_menu.set_winner(new_player)

    def change_menu(self, state):
        self.__current_state = state
        self.__current_menu = self.__menus[state]
