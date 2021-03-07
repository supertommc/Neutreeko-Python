from p5 import *
from app import *
from config import Config, State


class ButtonView:
    @staticmethod
    def display(button):
        text_size(button.get_text_size())

        # draw button background
        offset = 0
        if button.is_hover(mouse_x, mouse_y):
            offset = button.get_pressed_color_offset()
        fill(button.get_background_color()[0] + offset, button.get_background_color()[1] + offset, button.get_background_color()[2] + offset)
        rect(button.get_x(), button.get_y(), button.get_width(), button.get_height())

        # draw button text
        fill(button.get_color()[0], button.get_color()[1], button.get_color()[2])
        text(button.get_text(), button.get_text_x(), button.get_text_y())


class SlideButtonView:
    @staticmethod
    def display(button):
        text_size(button.get_text_size())

        # draw button background
        offset = 0
        if button.is_hover(mouse_x, mouse_y):
            offset = button.get_pressed_color_offset()
        fill(button.get_background_color()[0] + offset, button.get_background_color()[1] + offset,
             button.get_background_color()[2] + offset)
        rect(button.get_x(), button.get_y(), button.get_width(), button.get_height())

        # draw bar
        offset = 0
        if button.is_hover(mouse_x, mouse_y):
            offset = button.get_pressed_color_offset()
        fill(button.get_bar_color()[0] + offset, button.get_bar_color()[1] + offset, button.get_bar_color()[2] + offset)
        rect(button.get_bar_x(), button.get_bar_y(), button.get_bar_width(), button.get_bar_height())

        # draw button text
        fill(button.get_color()[0], button.get_color()[1], button.get_color()[2])
        text(button.get_text(), button.get_text_x(), button.get_text_y())


class MenuView:
    @staticmethod
    def display(menu):

        # display title
        text_size(menu.get_title_font_size())
        fill(menu.get_title_color()[0], menu.get_title_color()[1], menu.get_title_color()[2])
        text(menu.get_title_text(), menu.get_title_x(), menu.get_title_y())

        # display buttons
        ButtonView.display(menu.get_player_vs_player_button())
        ButtonView.display(menu.get_player_vs_bot_button())
        ButtonView.display(menu.get_bot_vs_player_button())
        ButtonView.display(menu.get_bot_vs_bot_button())
        SlideButtonView.display(menu.get_depth_slide_button())


class GameView:
    @staticmethod
    def display(game_state):
        GameView.display_lines()
        GameView.display_state(game_state)

    @staticmethod
    def display_lines():
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

    @staticmethod
    def display_state(game_state):
        for i in range(len(game_state)):
            for j in range(len(game_state[0])):
                if game_state[i][j] != 0:
                    GameView.display_piece(game_state[i][j], (550 - j * 100, 150 + i * 100))

    @staticmethod
    def display_piece(piece, position):
        if piece == 1:
            fill(0, 0, 0)
            circle(position, 50)

        elif piece == 2:
            fill(255, 255, 255)
            circle(position, 50)


def setup():
    title("NEUTREEKO")
    size(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
    game_font = create_font(Config.FONT_PATH, size=50)
    text_font(game_font)


def draw():
    clear()

    if newtreeko.get_state() == State.MENU:
        MenuView.display(newtreeko.get_menu())

    elif newtreeko.get_state() == State.PLAYER_VS_PLAYER:
        GameView.display(newtreeko.get_game_state())

    elif newtreeko.get_state() == State.PLAYER_VS_BOT:
        GameView.display(newtreeko.get_game_state())

    elif newtreeko.get_state() == State.BOT_VS_PLAYER:
        GameView.display(newtreeko.get_game_state())

    elif newtreeko.get_state() == State.BOT_VS_BOT:
        GameView.display(newtreeko.get_game_state())


def mouse_pressed():
    newtreeko.process_press(mouse_x, mouse_y)



# def mouse_dragged():
#     menu.press()

run()
