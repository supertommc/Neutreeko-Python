from p5 import *

game = [
    [0, 2, 0, 2, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 2, 0, 0],
    [0, 1, 0, 1, 0]
]


class Config:
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 700
    FONT_PATH = "fonts/TarrgetItalic-xzP8.otf"

    @staticmethod
    def get_font_width_height(font_text, font_size):
        image_font = create_font(Config.FONT_PATH, font_size)
        font_size = image_font.getsize(font_text)
        return font_size[0], font_size[1]


class Button:

    def __init__(self, position, width, height, new_color, background_color, pressed_color_offset, new_text, new_text_size):
        self._x, self._y = position
        self._color = new_color
        self._background_color = background_color
        self._pressed_color_offset = pressed_color_offset
        self._width = width
        self._height = height
        self._text = new_text
        self._text_size = new_text_size
        self._text_width, self._text_height = Config.get_font_width_height(new_text, new_text_size)

    def set_text(self, new_text, new_text_size):
        self._text = new_text
        self._text_size = new_text_size
        self._text_width, self._text_height = Config.get_font_width_height(new_text, new_text_size)

    def display(self):
        text_size(self._text_size)

        # draw button background
        offset = 0
        if self.is_hover():
            offset = self._pressed_color_offset
        fill(self._background_color[0] + offset, self._background_color[1] + offset, self._background_color[2] + offset)
        rect(self._x, self._y, self._width, self._height)

        # draw button text
        fill(self._color[0], self._color[1], self._color[2])
        text(self._text, self._x + self._width / 2 - text_width(self._text) / 2, self._y + self._height / 2 - self._text_height / 2)

    def is_hover(self):
        return mouse_x > self._x and mouse_x < self._x + self._width and mouse_y > self._y and mouse_y < self._y + self._height


class SlideButton(Button):

    def __init__(self, position, width, height, new_color, background_color, new_bar_color, pressed_color_offset, prefix, new_text_size, values):
        Button.__init__(self, position, width, height, new_color, background_color, pressed_color_offset, "", new_text_size)
        self.__bar_color = new_bar_color
        self.__prefix = prefix
        self.__values = values
        self.__current_value_index = 0
        self._text = self.__prefix + str(self.__values[self.__current_value_index])
        self.set_text(self.__prefix + str(self.__values[self.__current_value_index]), new_text_size)
        self.__bar_width = 0.1 * width
        self.__bar_height = height

    def display(self):
        text_size(self._text_size)

        # draw button background
        offset = 0
        if self.is_hover():
            offset = self._pressed_color_offset
        fill(self._background_color[0] + offset, self._background_color[1] + offset, self._background_color[2] + offset)
        rect(self._x, self._y, self._width, self._height)

        self.__display_bar()

        # draw button text
        fill(self._color[0], self._color[1], self._color[2])
        text(self._text, self._x + self._width / 2 - text_width(self._text) / 2, self._y + self._height / 2 - self._text_height / 2)

    def __get_bar_x(self):
        bar_ratio = self.__current_value_index / len(self.__values)
        return self._x + self._width * bar_ratio

    def __display_bar(self):

        bar_x = self.__get_bar_x()
        bar_y = self._y

        # draw bar background
        offset = 0
        if self.is_hover():
            offset = self._pressed_color_offset
        fill(self.__bar_color[0] + offset, self.__bar_color[1] + offset, self.__bar_color[2] + offset)
        rect(bar_x, bar_y, self.__bar_width, self.__bar_height)


class Menu:
    def __init__(self):
        self.__title_text = "NEUTREEKO"
        self.__title_font_size = 70
        self.__title_y = 100
        self.__title_color = (0, 0, 0)

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

        self.__player_vs_bot_button = None
        self.__player_vs_bot_button_text = "PLAYER VS BOT"

        self.__bot_vs_player_button = None
        self.__bot_vs_player_button_text = "BOT VS PLAYER"

        self.__bot_vs_bot_button = None
        self.__bot_vs_bot_button_text = "BOT VS BOT"

        self.__depth_slide_button = None
        self.__depth_slide_button_prefix = "DEPTH: "
        self.__depth_slide_button_values = range(10)

        self.__create_buttons()

    def __display_title(self):
        text_size(self.__title_font_size)
        fill(self.__title_color[0], self.__title_color[1], self.__title_color[2])
        text(self.__title_text, Config.SCREEN_WIDTH / 2 - text_width(self.__title_text) / 2, self.__title_y)

    def __create_buttons(self):
        button_y = self.__buttons_block_y
        button_x = Config.SCREEN_WIDTH / 2 - self.__buttons_width / 2

        self.__player_vs_player_button = Button((button_x, button_y), self.__buttons_width,
                                                self.__buttons_height, self.__buttons_color,
                                                self.__buttons_background_color, self.__buttons_pressed_color_offset,
                                                self.__player_vs_player_button_text, self.__buttons_font_size)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__player_vs_bot_button = Button((button_x, button_y), self.__buttons_width,
                                             self.__buttons_height, self.__buttons_color,
                                             self.__buttons_background_color, self.__buttons_pressed_color_offset,
                                             self.__player_vs_bot_button_text, self.__buttons_font_size)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__bot_vs_player_button = Button((button_x, button_y), self.__buttons_width,
                                             self.__buttons_height, self.__buttons_color,
                                             self.__buttons_background_color, self.__buttons_pressed_color_offset,
                                             self.__bot_vs_player_button_text, self.__buttons_font_size)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__bot_vs_bot_button = Button((button_x, button_y), self.__buttons_width,
                                          self.__buttons_height, self.__buttons_color,
                                          self.__buttons_background_color, self.__buttons_pressed_color_offset,
                                          self.__bot_vs_bot_button_text, self.__buttons_font_size)
        button_y += self.__buttons_height + self.__buttons_offset

        self.__depth_slide_button = SlideButton((button_x, button_y), self.__buttons_width,
                                                self.__buttons_height, self.__buttons_color,
                                                self.__buttons_background_color, self.__bar_color,
                                                self.__buttons_pressed_color_offset, self.__depth_slide_button_prefix,
                                                self.__buttons_font_size, self.__depth_slide_button_values)

    def __display_buttons(self):
        self.__player_vs_player_button.display()
        self.__player_vs_bot_button.display()
        self.__bot_vs_player_button.display()
        self.__bot_vs_bot_button.display()
        self.__depth_slide_button.display()

    def display(self):
        self.__display_title()
        self.__display_buttons()

    def press(self):
        print("X: {}".format(mouse_x))
        print("Y: {}".format(mouse_y))

    # def dragged(self):



def draw_menu():
    button = Button((100, 100), 100, 50, (100, 100, 100), "Play")
    button.display()


def draw_board(game):
    # Vertical Lines
    line((100, 100), (100, 600))
    line((200, 100), (200, 600))
    line((300, 100), (300, 600))
    line((400, 100), (400, 600))
    line((500, 100), (500, 600))
    line((600, 100), (600, 600))

    # Horizontal Lines
    line((100, 100), (600, 100))
    line((100, 200), (600, 200))
    line((100, 300), (600, 300))
    line((100, 400), (600, 400))
    line((100, 500), (600, 500))
    line((100, 600), (600, 600))

    draw_state(game)


def draw_piece(piece, position):
    if (piece == 1):
        fill(0, 0, 0)
        circle(position, 50)
    elif piece == 2:
        fill(255, 255, 255)
        circle(position, 50)


def draw_state(game):
    for i in range(len(game)):
        for j in range(len(game[0])):
            if game[i][j] != 0:
                draw_piece(game[i][j], (550 - j * 100, 150 + i * 100))


# def setup():
#     title("NEUTREEKO")
#     size(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
#     game_font = create_font(Config.FONT_PATH, size=50)
#     text_font(game_font)


def setup_game():
    title("NEUTREEKO")
    size(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
    game_font = create_font(Config.FONT_PATH, size=50)
    text_font(game_font)


def draw():
    # draw_board(game)
    # draw_menu()
    menu.display()


def mouse_dragged():
    menu.press()


menu = Menu()

run()
