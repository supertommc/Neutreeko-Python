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


class PieceView:

    @staticmethod
    def display(piece):
        if piece.get_player() == 1:
            image(Config.white_piece_image, Config.get_circle_top_left_position(piece.get_x(), piece.get_y(), piece.get_radius()))

        elif piece.get_player() == 2:
            image(Config.black_piece_image, Config.get_circle_top_left_position(piece.get_x(), piece.get_y(), piece.get_radius()))

    @staticmethod
    def clear(piece):
        background_color = config.Config.BACKGROUND_COLOR
        fill(background_color[0], background_color[1], background_color[2])
        no_stroke()
        circle(piece.get_position(), piece.get_radius())


class TileView:

    @staticmethod
    def display(tile):
        fill(tile.get_color()[0], tile.get_color()[1], tile.get_color()[2])
        square(tile.get_position(), tile.get_edge())


class BoardView:

    @staticmethod
    def display(game_board):

        # display board
        image(Config.board_image, (100, 100))

        # display pieces
        for tile in game_board.get_tiles():
            if tile.has_piece():
                PieceView.display(tile.get_piece())


def setup():
    title("NEUTREEKO")
    size(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
    game_font = create_font(Config.FONT_PATH, size=50)
    text_font(game_font)
    Config.board_image = load_image(Config.BOARD_IMAGE_PATH)
    Config.white_piece_image = load_image(Config.WHITE_PIECE_IMAGE_PATH)
    Config.black_piece_image = load_image(Config.BLACK_PIECE_IMAGE_PATH)


def draw():
    clear()

    neutreeko.update()

    if neutreeko.get_state() == State.MENU:
        MenuView.display(neutreeko.get_menu())

    else:
        BoardView.display(neutreeko.get_board())

        if neutreeko.get_board().get_move().is_happening():
            PieceView.display(neutreeko.get_board().get_move().get_piece())


def mouse_pressed():
    neutreeko.process_press(mouse_x, mouse_y)


run()
