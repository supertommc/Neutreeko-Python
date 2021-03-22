import button
import responses
import config


class Menu:
    def __init__(self):
        self.__title_text = "NEUTREEKO"
        self.__title_font_size = 70
        self.__title_y = 100
        self.__title_color = (0, 0, 0)
        self.__title_text_width, _ = config.Config.get_font_width_height(self.__title_text, self.__title_font_size)

        self.__buttons_width = 420
        self.__buttons_height = 50
        self.__buttons_color = (0, 0, 0)
        self.__bar_color = (110, 110, 110)
        self.__buttons_background_color = (90, 90, 90)
        self.__buttons_pressed_color_offset = 20
        self.__buttons_font_size = 28

        self.__buttons_block_y = 200
        self.__buttons_offset = 20

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

        self.__depth_slide_button_bot_1 = None
        self.__depth_slide_button_bot_1_prefix = "DEPTH BOT 1: "
        self.__depth_slide_button_bot_1_values = range(1, 10)
        self.__depth_slide_button_bot_1_response = responses.SlideResponse(1)

        self.__depth_slide_button_bot_2 = None
        self.__depth_slide_button_bot_2_prefix = "DEPTH BOT 2: "
        self.__depth_slide_button_bot_2_values = range(1, 10)
        self.__depth_slide_button_bot_2_response = responses.SlideResponse(2)

        self.__buttons_list = []

        self.__create_buttons()

    def __create_buttons(self):
        button_y = self.__buttons_block_y
        button_x = config.Config.SCREEN_WIDTH / 2 - self.__buttons_width / 2

        self.__player_vs_player_button = button.Button((button_x, button_y), self.__buttons_width,
                                                       self.__buttons_height, self.__buttons_color,
                                                       self.__buttons_background_color,
                                                       self.__buttons_pressed_color_offset,
                                                       self.__player_vs_player_button_text, self.__buttons_font_size,
                                                       self.__player_vs_player_button_response)
        self.__buttons_list.append(self.__player_vs_player_button)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__player_vs_bot_button = button.Button((button_x, button_y), self.__buttons_width,
                                                    self.__buttons_height, self.__buttons_color,
                                                    self.__buttons_background_color,
                                                    self.__buttons_pressed_color_offset,
                                                    self.__player_vs_bot_button_text, self.__buttons_font_size,
                                                    self.__player_vs_bot_button_response)
        self.__buttons_list.append(self.__player_vs_bot_button)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__bot_vs_player_button = button.Button((button_x, button_y), self.__buttons_width,
                                                    self.__buttons_height, self.__buttons_color,
                                                    self.__buttons_background_color,
                                                    self.__buttons_pressed_color_offset,
                                                    self.__bot_vs_player_button_text, self.__buttons_font_size,
                                                    self.__bot_vs_player_button_response)
        self.__buttons_list.append(self.__bot_vs_player_button)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__bot_vs_bot_button = button.Button((button_x, button_y), self.__buttons_width,
                                                 self.__buttons_height, self.__buttons_color,
                                                 self.__buttons_background_color, self.__buttons_pressed_color_offset,
                                                 self.__bot_vs_bot_button_text, self.__buttons_font_size,
                                                 self.__bot_vs_bot_button_response)
        self.__buttons_list.append(self.__bot_vs_bot_button)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__depth_slide_button_bot_1 = button.SlideButton((button_x, button_y), self.__buttons_width,
                                                             self.__buttons_height, self.__buttons_color,
                                                             self.__buttons_background_color, self.__bar_color,
                                                             self.__buttons_pressed_color_offset,
                                                             self.__depth_slide_button_bot_1_prefix,
                                                             self.__buttons_font_size,
                                                             self.__depth_slide_button_bot_1_values,
                                                             self.__depth_slide_button_bot_1_response)
        self.__buttons_list.append(self.__depth_slide_button_bot_1)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__depth_slide_button_bot_2 = button.SlideButton((button_x, button_y), self.__buttons_width,
                                                             self.__buttons_height, self.__buttons_color,
                                                             self.__buttons_background_color, self.__bar_color,
                                                             self.__buttons_pressed_color_offset,
                                                             self.__depth_slide_button_bot_2_prefix,
                                                             self.__buttons_font_size,
                                                             self.__depth_slide_button_bot_2_values,
                                                             self.__depth_slide_button_bot_2_response)
        self.__buttons_list.append(self.__depth_slide_button_bot_2)

    def get_title_text(self):
        return self.__title_text

    def get_title_font_size(self):
        return self.__title_font_size

    def get_title_x(self):
        return config.Config.SCREEN_WIDTH / 2 - self.__title_text_width / 2

    def get_title_y(self):
        return self.__title_y

    def get_title_color(self):
        return self.__title_color

    def get_buttons_width(self):
        return self.__buttons_width

    def get_buttons_height(self):
        return self.__buttons_height

    def get_buttons_color(self):
        return self.__buttons_color

    def get_buttons_background_color(self):
        return self.__buttons_background_color

    def get_buttons_pressed_color_offset(self):
        return self.__buttons_pressed_color_offset

    def get_buttons_font_size(self):
        return self.__buttons_font_size

    def get_buttons_block_y(self):
        return self.__buttons_block_y

    def get_buttons_offset(self):
        return self.__buttons_offset

    def get_player_vs_player_button_text(self):
        return self.__player_vs_player_button_text

    def get_player_vs_bot_button_text(self):
        return self.__player_vs_bot_button_text

    def get_bot_vs_player_button_text(self):
        return self.__bot_vs_player_button_text

    def get_bot_vs_bot_button_text(self):
        return self.__bot_vs_bot_button_text

    def get_depth_slide_button_bot_1_prefix(self):
        return self.__depth_slide_button_bot_1_prefix

    def get_depth_slide_button_bot_2_prefix(self):
        return self.__depth_slide_button_bot_1_prefix

    def get_player_vs_player_button(self):
        return self.__player_vs_player_button

    def get_player_vs_bot_button(self):
        return self.__player_vs_bot_button

    def get_bot_vs_player_button(self):
        return self.__bot_vs_player_button

    def get_bot_vs_bot_button(self):
        return self.__bot_vs_bot_button

    def get_depth_slide_button_bot_1(self):
        return self.__depth_slide_button_bot_1

    def get_depth_slide_button_bot_2(self):
        return self.__depth_slide_button_bot_2

    def press(self, mx, my):
        for button in self.__buttons_list:
            button.press(mx, my)

    def release(self):
        self.__depth_slide_button_bot_1.release()
        self.__depth_slide_button_bot_2.release()

    def drag(self, mx):
        self.__depth_slide_button_bot_1.drag(mx)
        self.__depth_slide_button_bot_2.drag(mx)
