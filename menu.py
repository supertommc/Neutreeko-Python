import button
import responses
import config


class Menu:
    def __init__(self, title_text):

        # title properties

        self._title_text = title_text
        self._title_font_size = 70
        self._title_y = 100
        self._title_color = (0, 0, 0)
        self._title_text_width, _ = config.Config.get_font_width_height(self._title_text, self._title_font_size)

        # all buttons properties

        self._buttons_color = (0, 0, 0)
        self._bar_color = (110, 110, 110)
        self._buttons_background_color = (90, 90, 90)
        self._buttons_pressed_color_offset = 20
        self._buttons_font_size = 28

        self._buttons_horizontal_offset = 20
        self._buttons_vertical_offset = 40

        self._buttons_height = 50
        self._small_buttons_width = 350
        self._large_buttons_width = 2 * self._small_buttons_width + self._buttons_vertical_offset

        self._left_small_buttons_x = config.Config.SCREEN_WIDTH // 2 - self._buttons_vertical_offset // 2 - self._small_buttons_width
        self._right_small_buttons_x = config.Config.SCREEN_WIDTH // 2 + self._buttons_vertical_offset // 2
        self._large_buttons_x = self._left_small_buttons_x
        self._first_button_y = 200

        self._buttons_list = []
        self._slide_buttons_list = []

    def get_title_text(self):
        return self._title_text

    def get_title_font_size(self):
        return self._title_font_size

    def get_title_x(self):
        return config.Config.SCREEN_WIDTH / 2 - self._title_text_width / 2

    def get_title_y(self):
        return self._title_y

    def get_title_color(self):
        return self._title_color

    def press(self, mx, my):
        for current_button in self._buttons_list:
            current_button.press(mx, my)

    def release(self):
        for current_button in self._slide_buttons_list:
            current_button.release()

    def drag(self, mx):
        for current_button in self._slide_buttons_list:
            current_button.drag(mx)


class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self, "NEUTREEKO")

        self.__player_vs_player_button = None
        self.__player_vs_player_button_text = "PLAYER VS PLAYER"
        self.__player_vs_player_button_response = responses.ChangeStateResponse(config.State.PLAYER_VS_PLAYER)

        self.__player_vs_bot_button = None
        self.__player_vs_bot_button_text = "PLAYER VS BOT"
        self.__player_vs_bot_button_response = responses.ChangeStateResponse(config.State.PLAYER_VS_BOT)

        self.__bot_vs_player_button = None
        self.__bot_vs_player_button_text = "BOT VS PLAYER"
        self.__bot_vs_player_button_response = responses.ChangeStateResponse(config.State.BOT_VS_PLAYER)

        self.__bot_vs_bot_button = None
        self.__bot_vs_bot_button_text = "BOT VS BOT"
        self.__bot_vs_bot_button_response = responses.ChangeStateResponse(config.State.BOT_VS_BOT)

        self.__options_button = None
        self.__options_button_text = "OPTIONS"
        self.__options_button_response = responses.ChangeStateResponse(config.State.OPTIONS_MENU)

        self.__create_buttons()

    def __create_buttons(self):
        button_y = self._first_button_y

        self.__player_vs_player_button = button.Button((self._large_buttons_x, button_y), self._large_buttons_width,
                                                       self._buttons_height, self._buttons_color,
                                                       self._buttons_background_color,
                                                       self._buttons_pressed_color_offset,
                                                       self.__player_vs_player_button_text, self._buttons_font_size,
                                                       self.__player_vs_player_button_response)
        self._buttons_list.append(self.__player_vs_player_button)
        button_y += self._buttons_height + self._buttons_vertical_offset

        self.__player_vs_bot_button = button.Button((self._large_buttons_x, button_y), self._large_buttons_width,
                                                    self._buttons_height, self._buttons_color,
                                                    self._buttons_background_color,
                                                    self._buttons_pressed_color_offset,
                                                    self.__player_vs_bot_button_text, self._buttons_font_size,
                                                    self.__player_vs_bot_button_response)
        self._buttons_list.append(self.__player_vs_bot_button)
        button_y += self._buttons_height + self._buttons_vertical_offset

        self.__bot_vs_player_button = button.Button((self._large_buttons_x, button_y), self._large_buttons_width,
                                                    self._buttons_height, self._buttons_color,
                                                    self._buttons_background_color,
                                                    self._buttons_pressed_color_offset,
                                                    self.__bot_vs_player_button_text, self._buttons_font_size,
                                                    self.__bot_vs_player_button_response)
        self._buttons_list.append(self.__bot_vs_player_button)
        button_y += self._buttons_height + self._buttons_vertical_offset

        self.__bot_vs_bot_button = button.Button((self._large_buttons_x, button_y), self._large_buttons_width,
                                                 self._buttons_height, self._buttons_color,
                                                 self._buttons_background_color, self._buttons_pressed_color_offset,
                                                 self.__bot_vs_bot_button_text, self._buttons_font_size,
                                                 self.__bot_vs_bot_button_response)
        self._buttons_list.append(self.__bot_vs_bot_button)
        button_y += self._buttons_height + self._buttons_vertical_offset

        self.__options_button = button.Button((self._large_buttons_x, button_y), self._large_buttons_width,
                                              self._buttons_height, self._buttons_color,
                                              self._buttons_background_color, self._buttons_pressed_color_offset,
                                              self.__options_button_text, self._buttons_font_size,
                                              self.__options_button_response)
        self._buttons_list.append(self.__options_button)

    def get_player_vs_player_button(self):
        return self.__player_vs_player_button

    def get_player_vs_bot_button(self):
        return self.__player_vs_bot_button

    def get_bot_vs_player_button(self):
        return self.__bot_vs_player_button

    def get_bot_vs_bot_button(self):
        return self.__bot_vs_bot_button

    def get_options_button(self):
        return self.__options_button


class OptionsMenu(Menu):

    def __init__(self, initial_depth_hint, initial_depth_bot_1, initial_depth_bot_2):
        Menu.__init__(self, "OPTIONS")

        self.__initial_depth_hint = initial_depth_hint
        self.__initial_depth_bot_1 = initial_depth_bot_1
        self.__initial_depth_bot_2 = initial_depth_bot_2

        self.__depth_hint_slide_button = None
        self.__depth_hint_slide_button_prefix = "DEPTH HINT: "
        self.__depth_hint_slide_button_values = range(1, 10)
        self.__depth_hint_slide_button_response = responses.SlideResponse(0)

        self.__evaluation_hint_toggle_button = None
        self.__evaluation_hint_toggle_button_prefix = "EVAL: "
        self.__evaluation_hint_toggle_button_values = ["EASY", "MEDIUM", "HARD"]
        self.__evaluation_hint_toggle_button_response = responses.EvaluationToggleResponse(0)

        self.__depth_bot_1_slide_button = None
        self.__depth_bot_1_slide_button_prefix = "DEPTH BOT 1: "
        self.__depth_bot_1_slide_button_values = range(1, 10)
        self.__depth_bot_1_slide_button_response = responses.SlideResponse(1)

        self.__evaluation_bot_1_toggle_button = None
        self.__evaluation_bot_1_toggle_button_prefix = "EVAL: "
        self.__evaluation_bot_1_toggle_button_values = ["EASY", "MEDIUM", "HARD"]
        self.__evaluation_bot_1_toggle_button_response = responses.EvaluationToggleResponse(1)

        self.__depth_bot_2_slide_button = None
        self.__depth_bot_2_slide_button_prefix = "DEPTH BOT 2: "
        self.__depth_bot_2_slide_button_values = range(1, 10)
        self.__depth_bot_2_slide_button_response = responses.SlideResponse(2)

        self.__evaluation_bot_2_toggle_button = None
        self.__evaluation_bot_2_toggle_button_prefix = "EVAL: "
        self.__evaluation_bot_2_toggle_button_values = ["EASY", "MEDIUM", "HARD"]
        self.__evaluation_bot_2_toggle_button_response = responses.EvaluationToggleResponse(2)

        self.__opening_book_toggle_button = None
        self.__opening_book_toggle_button_prefix = "OPENING BOOK: "
        self.__opening_book_toggle_button_values = ["ON", "OFF"]
        self.__opening_book_toggle_button_response = responses.OpeningBookToggleResponse()

        self.__back_button = None
        self.__back_button_text = "BACK"
        self.__back_button_response = responses.ChangeStateResponse(config.State.MAIN_MENU)

        self.__create_buttons()

    def __create_buttons(self):
        button_y = self._first_button_y

        # first row [Hint]

        self.__depth_hint_slide_button = button.SlideButton((self._left_small_buttons_x, button_y),
                                                            self._small_buttons_width,
                                                            self._buttons_height, self._buttons_color,
                                                            self._buttons_background_color,
                                                            self._bar_color,
                                                            self._buttons_pressed_color_offset,
                                                            self.__depth_hint_slide_button_prefix,
                                                            self._buttons_font_size,
                                                            self.__depth_hint_slide_button_values,
                                                            self.__initial_depth_hint,
                                                            self.__depth_hint_slide_button_response)
        self._buttons_list.append(self.__depth_hint_slide_button)
        self._slide_buttons_list.append(self.__depth_hint_slide_button)

        self.__evaluation_hint_toggle_button = button.ToggleButton((self._right_small_buttons_x, button_y),
                                                                   self._small_buttons_width,
                                                                   self._buttons_height, self._buttons_color,
                                                                   self._buttons_background_color,
                                                                   self._buttons_pressed_color_offset,
                                                                   self.__evaluation_hint_toggle_button_prefix,
                                                                   self._buttons_font_size,
                                                                   self.__evaluation_hint_toggle_button_values,
                                                                   self.__evaluation_hint_toggle_button_response)
        self._buttons_list.append(self.__evaluation_hint_toggle_button)
        button_y += self._buttons_height + self._buttons_vertical_offset

        # second row [Bot 1]

        self.__depth_bot_1_slide_button = button.SlideButton((self._left_small_buttons_x, button_y),
                                                             self._small_buttons_width,
                                                             self._buttons_height, self._buttons_color,
                                                             self._buttons_background_color,
                                                             self._bar_color,
                                                             self._buttons_pressed_color_offset,
                                                             self.__depth_bot_1_slide_button_prefix,
                                                             self._buttons_font_size,
                                                             self.__depth_bot_1_slide_button_values,
                                                             self.__initial_depth_bot_1,
                                                             self.__depth_bot_1_slide_button_response)
        self._buttons_list.append(self.__depth_bot_1_slide_button)
        self._slide_buttons_list.append(self.__depth_bot_1_slide_button)

        self.__evaluation_bot_1_toggle_button = button.ToggleButton((self._right_small_buttons_x, button_y),
                                                                    self._small_buttons_width,
                                                                    self._buttons_height, self._buttons_color,
                                                                    self._buttons_background_color,
                                                                    self._buttons_pressed_color_offset,
                                                                    self.__evaluation_bot_1_toggle_button_prefix,
                                                                    self._buttons_font_size,
                                                                    self.__evaluation_bot_1_toggle_button_values,
                                                                    self.__evaluation_bot_1_toggle_button_response)
        self._buttons_list.append(self.__evaluation_bot_1_toggle_button)
        button_y += self._buttons_height + self._buttons_vertical_offset

        # third row [Bot 2]

        self.__depth_bot_2_slide_button = button.SlideButton((self._left_small_buttons_x, button_y),
                                                             self._small_buttons_width,
                                                             self._buttons_height, self._buttons_color,
                                                             self._buttons_background_color,
                                                             self._bar_color,
                                                             self._buttons_pressed_color_offset,
                                                             self.__depth_bot_2_slide_button_prefix,
                                                             self._buttons_font_size,
                                                             self.__depth_bot_2_slide_button_values,
                                                             self.__initial_depth_bot_2,
                                                             self.__depth_bot_2_slide_button_response)
        self._buttons_list.append(self.__depth_bot_2_slide_button)
        self._slide_buttons_list.append(self.__depth_bot_2_slide_button)

        self.__evaluation_bot_2_toggle_button = button.ToggleButton((self._right_small_buttons_x, button_y),
                                                                    self._small_buttons_width,
                                                                    self._buttons_height, self._buttons_color,
                                                                    self._buttons_background_color,
                                                                    self._buttons_pressed_color_offset,
                                                                    self.__evaluation_bot_2_toggle_button_prefix,
                                                                    self._buttons_font_size,
                                                                    self.__evaluation_bot_2_toggle_button_values,
                                                                    self.__evaluation_bot_2_toggle_button_response)
        self._buttons_list.append(self.__evaluation_bot_2_toggle_button)
        button_y += self._buttons_height + self._buttons_vertical_offset

        # fourth row [Opening Book]

        self.__opening_book_toggle_button = button.ToggleButton((self._large_buttons_x, button_y),
                                                                self._large_buttons_width,
                                                                self._buttons_height, self._buttons_color,
                                                                self._buttons_background_color,
                                                                self._buttons_pressed_color_offset,
                                                                self.__opening_book_toggle_button_prefix,
                                                                self._buttons_font_size,
                                                                self.__opening_book_toggle_button_values,
                                                                self.__opening_book_toggle_button_response)
        self._buttons_list.append(self.__opening_book_toggle_button)
        button_y += self._buttons_height + self._buttons_vertical_offset

        # fifth row [Back]

        self.__back_button = button.Button((self._large_buttons_x, button_y), self._large_buttons_width,
                                           self._buttons_height, self._buttons_color,
                                           self._buttons_background_color,
                                           self._buttons_pressed_color_offset,
                                           self.__back_button_text, self._buttons_font_size,
                                           self.__back_button_response)
        self._buttons_list.append(self.__back_button)

    def get_depth_slide_button(self, bot):
        if bot == 0:
            return self.__depth_hint_slide_button
        elif bot == 1:
            return self.__depth_bot_1_slide_button
        elif bot == 2:
            return self.__depth_bot_2_slide_button
        return None

    def get_evaluation_toggle_button(self, bot):
        if bot == 0:
            return self.__evaluation_hint_toggle_button
        elif bot == 1:
            return self.__evaluation_bot_1_toggle_button
        elif bot == 2:
            return self.__evaluation_bot_2_toggle_button
        return None

    def get_opening_book_toggle_button(self):
        return self.__opening_book_toggle_button

    def get_back_button(self):
        return self.__back_button
