import config


"""
    Here are all the buttons classes used in the menus
"""


class Button:
    """
        This is the base and simple button that only execute its response when it is pressed
    """

    def __init__(self, position, width, height, new_color, background_color, pressed_color_offset, new_text,
                 new_text_size, response):
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
    """
        This is a more sophisticated button that has a slide bar to choose a number in the values list
    """

    def __init__(self, position, width, height, new_color, background_color, new_bar_color, pressed_color_offset,
                 prefix, new_text_size, values, initial_value_index, response):
        Button.__init__(self, position, width, height, new_color, background_color, pressed_color_offset, "",
                        new_text_size, response)
        self.__bar_color = new_bar_color
        self.__prefix = prefix
        self.__values = values
        self.__number_values = len(values)
        self.__current_value_index = initial_value_index
        self._text = self.__prefix + str(self.__values[self.__current_value_index])
        self.set_text(self.__prefix + str(self.__values[self.__current_value_index]), new_text_size)
        self.__bar_width = 0.1 * width
        self.__bar_height = height
        self.__bar_x, self.__bar_y = position
        self.__dragging = False
        self.update_bar_x_by_index()

    def get_bar_color(self):
        return self.__bar_color

    def get_bar_width(self):
        return self.__bar_width

    def get_bar_height(self):
        return self.__bar_height

    def get_bar_x(self):
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

    def update_bar_x_by_index(self):
        ratio = self.__current_value_index / self.__number_values
        self.__bar_x = self._x + self._width * ratio

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


class ToggleButton(Button):
    """
        This is a more sophisticated button that when you press it, it change the current value to the next in the
        values list
    """

    def __init__(self, position, width, height, new_color, background_color, pressed_color_offset, prefix, new_text_size, values, initial_value_index, response):
        Button.__init__(self, position, width, height, new_color, background_color, pressed_color_offset, "", new_text_size, response)

        self.__prefix = prefix
        self.__values = values
        self.__number_values = len(values)

        self.__current_value_index = initial_value_index
        self._text = self.__prefix + str(self.__values[self.__current_value_index])
        self.set_text(self.__prefix + str(self.__values[self.__current_value_index]), new_text_size)

    def get_current_value(self):
        return self.__values[self.__current_value_index]

    def update_text(self):
        self._text = self.__prefix + str(self.__values[self.__current_value_index])
        self.set_text(self.__prefix + str(self.__values[self.__current_value_index]), self._text_size)

    def update(self):
        self.__current_value_index = (self.__current_value_index + 1) % self.__number_values
        self.update_text()

    def press(self, mx, my):
        if self.is_hover(mx, my):
            self.update()
            self._response.on_press(self)
