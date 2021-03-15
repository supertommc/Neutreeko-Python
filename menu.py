import responses
import config


class Button:

    def __init__(self, position, width, height, new_color, background_color, pressed_color_offset, new_text, new_text_size, response):
        self._x, self._y = position
        self._color = new_color
        self._background_color = background_color
        self._pressed_color_offset = pressed_color_offset
        self._width = width
        self._height = height
        self._text = new_text
        self._text_size = new_text_size
        self._text_width, self._text_height = config.Config.get_font_width_height(new_text, new_text_size)
        self._response = response

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_color(self):
        return self._color

    def get_background_color(self):
        return self._background_color

    def get_pressed_color_offset(self):
        return self._pressed_color_offset

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_text(self):
        return self._text

    def get_text_size(self):
        return self._text_size

    def get_text_x(self):
        return self._x + self._width / 2 - self._text_width / 2

    def get_text_y(self):
        return self._y + self._height / 2 - self._text_height / 2

    def set_text(self, new_text, new_text_size):
        self._text = new_text
        self._text_size = new_text_size
        self._text_width, self._text_height = config.Config.get_font_width_height(new_text, new_text_size)

    def is_hover(self, mx, my):
        return self._x < mx < self._x + self._width and self._y < my < self._y + self._height

    def press(self, mx, my):
        if self.is_hover(mx, my):
            self._response.on_press()


class SlideButton(Button):

    def __init__(self, position, width, height, new_color, background_color, new_bar_color, pressed_color_offset, prefix, new_text_size, values, response):
        Button.__init__(self, position, width, height, new_color, background_color, pressed_color_offset, "", new_text_size, response)
        self.__bar_color = new_bar_color
        self.__prefix = prefix
        self.__values = values
        self.__number_values = len(values)
        self.__current_value_index = 0
        self._text = self.__prefix + str(self.__values[self.__current_value_index])
        self.set_text(self.__prefix + str(self.__values[self.__current_value_index]), new_text_size)
        self.__bar_width = 0.1 * width
        self.__bar_height = height
        self.__bar_x, self.__bar_y = position
        self.__dragging = False

    def get_bar_color(self):
        return self.__bar_color

    def get_bar_width(self):
        return self.__bar_width

    def get_bar_height(self):
        return self.__bar_height

    def get_bar_x(self):
        # bar_ratio = self.__current_value_index / len(self.__values)
        # return self._x + self._width * bar_ratio
        return self.__bar_x

    def get_bar_y(self):
        return self.__bar_y

    def get_current_value(self):
        return self.__values[self.__current_value_index]

    def set_dragging(self, new_dragging):
        self.__dragging = new_dragging

    def update_text(self):
        self._text = self.__prefix + str(self.__values[self.__current_value_index])
        self.set_text(self.__prefix + str(self.__values[self.__current_value_index]), self._text_size)

    def update_bar_position(self, mx):
        self.__bar_x = mx

    def update(self, mx):
        if mx < self._x + self.__bar_width / 2:
            # update bar position
            self.__bar_x = self._x

            # update index
            self.__current_value_index = 0

        elif mx > self._x + self._width - self.__bar_width:
            # update bar position
            self.__bar_x = self._x + self._width - self.__bar_width

            # update index
            self.__current_value_index = self.__number_values - 1

        else:
            # update bar position
            self.__bar_x = mx

            # update index
            bar_ratio = (mx - self._x) / self._width
            self.__current_value_index = round(bar_ratio * self.__number_values)

        self.update_text()

    def press(self, mx, my):
        if self.is_hover(mx, my):
            self.__dragging = True

    def release(self):
        self.__dragging = False

    def drag(self, mx):
        if self.__dragging:
            self.update(mx)
            self._response.on_drag(self)


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
        self.__player_vs_player_button_response = responses.StaticResponse(config.State.PLAYER_VS_PLAYER)

        self.__player_vs_bot_button = None
        self.__player_vs_bot_button_text = "PLAYER VS BOT"
        self.__player_vs_bot_button_response = responses.StaticResponse(config.State.PLAYER_VS_BOT)

        self.__bot_vs_player_button = None
        self.__bot_vs_player_button_text = "BOT VS PLAYER"
        self.__bot_vs_player_button_response = responses.StaticResponse(config.State.BOT_VS_PLAYER)

        self.__bot_vs_bot_button = None
        self.__bot_vs_bot_button_text = "BOT VS BOT"
        self.__bot_vs_bot_button_response = responses.StaticResponse(config.State.BOT_VS_BOT)

        self.__depth_slide_button = None
        self.__depth_slide_button_prefix = "DEPTH: "
        self.__depth_slide_button_values = range(10)
        self.__depth_slide_button_response = responses.SlideResponse(1)

        self.__buttons_list = []

        self.__create_buttons()

    def __create_buttons(self):
        button_y = self.__buttons_block_y
        button_x = config.Config.SCREEN_WIDTH / 2 - self.__buttons_width / 2

        self.__player_vs_player_button = Button((button_x, button_y), self.__buttons_width,
                                                self.__buttons_height, self.__buttons_color,
                                                self.__buttons_background_color, self.__buttons_pressed_color_offset,
                                                self.__player_vs_player_button_text, self.__buttons_font_size,
                                                self.__player_vs_player_button_response)
        self.__buttons_list.append(self.__player_vs_player_button)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__player_vs_bot_button = Button((button_x, button_y), self.__buttons_width,
                                             self.__buttons_height, self.__buttons_color,
                                             self.__buttons_background_color, self.__buttons_pressed_color_offset,
                                             self.__player_vs_bot_button_text, self.__buttons_font_size,
                                             self.__player_vs_bot_button_response)
        self.__buttons_list.append(self.__player_vs_bot_button)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__bot_vs_player_button = Button((button_x, button_y), self.__buttons_width,
                                             self.__buttons_height, self.__buttons_color,
                                             self.__buttons_background_color, self.__buttons_pressed_color_offset,
                                             self.__bot_vs_player_button_text, self.__buttons_font_size,
                                             self.__bot_vs_player_button_response)
        self.__buttons_list.append(self.__bot_vs_player_button)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__bot_vs_bot_button = Button((button_x, button_y), self.__buttons_width,
                                          self.__buttons_height, self.__buttons_color,
                                          self.__buttons_background_color, self.__buttons_pressed_color_offset,
                                          self.__bot_vs_bot_button_text, self.__buttons_font_size,
                                          self.__bot_vs_bot_button_response)
        self.__buttons_list.append(self.__bot_vs_bot_button)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__depth_slide_button = SlideButton((button_x, button_y), self.__buttons_width,
                                                self.__buttons_height, self.__buttons_color,
                                                self.__buttons_background_color, self.__bar_color,
                                                self.__buttons_pressed_color_offset, self.__depth_slide_button_prefix,
                                                self.__buttons_font_size, self.__depth_slide_button_values,
                                                self.__depth_slide_button_response)
        self.__buttons_list.append(self.__depth_slide_button)

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

    def get_depth_slide_button_prefix(self):
        return self.__depth_slide_button_prefix

    def get_player_vs_player_button(self):
        return self.__player_vs_player_button

    def get_player_vs_bot_button(self):
        return self.__player_vs_bot_button

    def get_bot_vs_player_button(self):
        return self.__bot_vs_player_button

    def get_bot_vs_bot_button(self):
        return self.__bot_vs_bot_button

    def get_depth_slide_button(self):
        return self.__depth_slide_button

    def press(self, mx, my):
        for button in self.__buttons_list:
            button.press(mx, my)

    def release(self):
        self.__depth_slide_button.release()

    def drag(self, mx):
        self.__depth_slide_button.drag(mx)
