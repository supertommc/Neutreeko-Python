from p5 import *

game =  [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]


class Config:
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 700
    FONT_PATH = "fonts/Red_Rocket_Expanded_Italic.ttf"

    @staticmethod
    def get_font_width_height(font_text, font_size):
        image_font = create_font(Config.FONT_PATH, font_size)
        font_size = image_font.getsize(font_text)
        return font_size[0], font_size[1]


class Button:
    def __init__(self, position, width, height, color, background_color,  pressed_color_offset, text, text_size):
        self.x, self.y = position
        self.color = color
        self.background_color = background_color
        self.pressed_color_offset = pressed_color_offset
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size
        self.text_width, self.text_height = Config.get_font_width_height(text, text_size)

    def display(self):
        text_size(self.text_size)
        offset = 0
        if self.is_hover():
            offset = self.pressed_color_offset
        fill(self.background_color[0]+offset, self.background_color[1]+offset, self.background_color[2]+offset)
        rect(self.x, self.y, self.width, self.height)
        fill(self.color[0], self.color[1], self.color[2])

        text(self.text, self.x + self.width / 2 - text_width(self.text) / 2, self.y + self.height/2 - self.text_height / 2)

    def is_hover(self):
        return mouse_x > self.x and mouse_x < self.x + self.width and mouse_y > self.y and mouse_y < self.y + self.height


class Menu:
    def __init__(self):
        self.__title_text = "NEUTREEKO"
        self.__title_font_size = 50
        self.__title_y = 100
        self.__title_color = (0, 0, 0)

        self.__buttons_width = 370
        self.__buttons_height = 50
        self.__buttons_color = (0, 0, 0)
        self.__buttons_background_color = (90, 90, 90)
        self.__buttons_pressed_color_offset = 20
        self.__buttons_font_size = 20

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

    def __display_buttons(self):
        self.__player_vs_player_button.display()
        self.__player_vs_bot_button.display()
        self.__bot_vs_player_button.display()
        self.__bot_vs_bot_button.display()

    def display(self):
        self.__display_title()
        self.__display_buttons()


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
                draw_piece(game[i][j], (550-j*100, 150+i*100))


def setup():
    size(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
    game_font = create_font(Config.FONT_PATH, size=50)
    text_font(game_font)


def draw():
    # draw_board(game)
    # draw_menu()
    Menu().display()

run()



