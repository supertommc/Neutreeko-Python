import button
import config
import responses


class BoardMenu:

    def __init__(self, position, width, height):
        self.__x, self.__y = position
        self.__width = width
        self.__height = height

        self.__number_buttons = 3
        self.__buttons_offset = 20
        self.__buttons_width = self.__width
        self.__buttons_height = (self.__height - self.__buttons_offset * (self.__number_buttons - 2)) // 3
        self.__buttons_color = (0, 0, 0)
        self.__buttons_background_color = (90, 90, 90)
        self.__buttons_pressed_color_offset = 20
        self.__buttons_font_size = 16

        self.__hint_button = None
        self.__hint_button_text = "Hint"
        self.__hint_button_response = responses.HintResponse()

        self.__restart_button = None
        self.__restart_button_text = "Restart"
        self.__restart_button_response = responses.RestartResponse()

        self.__leave_button = None
        self.__leave_button_text = "Leave"
        self.__leave_button_response = responses.ChangeStateResponse(config.State.MENU)

        self.__buttons_list = []
        self.__create_buttons()

    def __create_buttons(self):
        button_x = self.__x
        button_y = self.__y

        self.__hint_button = button.Button((button_x, button_y), self.__buttons_width,
                                           self.__buttons_height, self.__buttons_color,
                                           self.__buttons_background_color,
                                           self.__buttons_pressed_color_offset,
                                           self.__hint_button_text, self.__buttons_font_size,
                                           self.__hint_button_response)

        self.__buttons_list.append(self.__hint_button)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__restart_button = button.Button((button_x, button_y), self.__buttons_width,
                                              self.__buttons_height, self.__buttons_color,
                                              self.__buttons_background_color,
                                              self.__buttons_pressed_color_offset,
                                              self.__restart_button_text, self.__buttons_font_size,
                                              self.__restart_button_response)

        self.__buttons_list.append(self.__restart_button)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__leave_button = button.Button((button_x, button_y), self.__buttons_width,
                                            self.__buttons_height, self.__buttons_color,
                                            self.__buttons_background_color,
                                            self.__buttons_pressed_color_offset,
                                            self.__leave_button_text, self.__buttons_font_size,
                                            self.__leave_button_response)

        self.__buttons_list.append(self.__leave_button)

    def get_buttons(self):
        return self.__buttons_list

    def press(self, mx, my):
        for but in self.__buttons_list:
            but.press(mx, my)
