from p5 import *
from app import *
from config import Config, State


class ButtonView:
    @staticmethod
    def display(button):
        """ Display button on screen

        :param button:
        :return:
        """
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
        """ Display slide button on screen

        :param button:
        :return:
        """
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


class MainMenuView:
    @staticmethod
    def display(main_menu):
        """ Display main menu on screen

        :param main_menu:
        :return:
        """

        # display title
        text_size(main_menu.get_title_font_size())
        fill(main_menu.get_title_color()[0], main_menu.get_title_color()[1], main_menu.get_title_color()[2])
        text(main_menu.get_title_text(), main_menu.get_title_x(), main_menu.get_title_y())

        # display buttons
        ButtonView.display(main_menu.get_player_vs_player_button())
        ButtonView.display(main_menu.get_player_vs_bot_button())
        ButtonView.display(main_menu.get_bot_vs_player_button())
        ButtonView.display(main_menu.get_bot_vs_bot_button())
        ButtonView.display(main_menu.get_options_button())


class OptionsMenuView:
    @staticmethod
    def display(options_menu):
        """ Display options menu on screen

        :param options_menu:
        :return:
        """
        # display title
        text_size(options_menu.get_title_font_size())
        fill(options_menu.get_title_color()[0], options_menu.get_title_color()[1], options_menu.get_title_color()[2])
        text(options_menu.get_title_text(), options_menu.get_title_x(), options_menu.get_title_y())

        # display buttons
        for i in range(3):
            SlideButtonView.display(options_menu.get_depth_slide_button(i))
            ButtonView.display(options_menu.get_evaluation_toggle_button(i))
        ButtonView.display(options_menu.get_opening_book_toggle_button())
        ButtonView.display(options_menu.get_back_button())


class PieceView:

    @staticmethod
    def display(piece):
        """ Display piece on screen

        :param piece:
        :return:
        """
        if piece.get_player() == 1:
            image(Config.black_piece_image, Config.get_circle_top_left_position(piece.get_x(), piece.get_y(), piece.get_radius()))

        elif piece.get_player() == 2:
            image(Config.white_piece_image, Config.get_circle_top_left_position(piece.get_x(), piece.get_y(), piece.get_radius()))


class TileView:

    @staticmethod
    def display(tile):
        """ Display tile on screen

        :param tile:
        :return:
        """
        fill(tile.get_color()[0], tile.get_color()[1], tile.get_color()[2])
        square(tile.get_position(), tile.get_edge())


class ScoreBarView:

    @staticmethod
    def display(score_bar):
        """ Display score bar on screen

        :param score_bar:
        :return:
        """
        black_pieces_color = config.Config.BLACK_PIECES_COLOR
        white_pieces_color = config.Config.WHITE_PIECES_COLOR

        fill(white_pieces_color[0], white_pieces_color[1], white_pieces_color[2])
        rect(score_bar.get_x(), score_bar.get_y(), score_bar.get_width(), score_bar.get_height())

        fill(black_pieces_color[0], black_pieces_color[1], black_pieces_color[2])
        rect(score_bar.get_x(), score_bar.get_bar_y(), score_bar.get_width(), score_bar.get_current_bar_height())


class PlayerMenuView:

    @staticmethod
    def display(player_menu):
        """ Display player menu on screen

        :param player_menu:
        :return:
        """

        # display title
        text_size(player_menu.get_text_font_size())
        fill(player_menu.get_text_color()[0], player_menu.get_text_color()[1], player_menu.get_text_color()[2])
        text(player_menu.get_current_text(), player_menu.get_text_x(), player_menu.get_text_y())

        # display buttons
        for button in player_menu.get_current_buttons_list():
            ButtonView.display(button)


class BoardMenuView:

    @staticmethod
    def display(board_menu):
        """ Display board menu on screen

        :param board_menu:
        :return:
        """

        # display buttons
        for button in board_menu.get_buttons():
            ButtonView.display(button)


class HintView:

    @staticmethod
    def display(hint):
        """ Display hint on screen

        :param hint:
        :return:
        """

        # display hint line
        line_color = hint.get_line_color()
        stroke(line_color[0], line_color[1], line_color[2])
        line(hint.get_start_move_position(), hint.get_dest_move_position())
        stroke(0, 0, 0)


class BoardView:

    @staticmethod
    def display(game_board):
        """ Display game board on screen

        :param game_board:
        :return:
        """

        # display board
        image(Config.board_image, (100, 100))

        # display pieces
        for tile in game_board.get_tiles():
            if tile.has_piece():
                PieceView.display(tile.get_piece())

        ScoreBarView.display(game_board.get_score_bar())
        BoardMenuView.display(game_board.get_board_menu())
        PlayerMenuView.display(game_board.get_player_menu(1))
        PlayerMenuView.display(game_board.get_player_menu(2))

        if game_board.get_hint() is not None:
            HintView.display(game_board.get_hint())


def setup():
    """ p5 setup

    :param:
    :return:
    """
    title("NEUTREEKO")
    size(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
    game_font = create_font(Config.FONT_PATH, size=50)
    text_font(game_font)
    Config.board_image = load_image(Config.BOARD_IMAGE_PATH)
    Config.white_piece_image = load_image(Config.WHITE_PIECE_IMAGE_PATH)
    Config.black_piece_image = load_image(Config.BLACK_PIECE_IMAGE_PATH)


def draw():
    """ Draw application each frame

    :param:
    :return:
    """
    clear()

    neutreeko.update()

    if neutreeko.get_state() == State.MAIN_MENU:
        MainMenuView.display(neutreeko.get_main_menu())

    elif neutreeko.get_state() == State.OPTIONS_MENU:
        OptionsMenuView.display(neutreeko.get_options_menu())

    else:
        BoardView.display(neutreeko.get_board())

        if neutreeko.get_board().get_move().is_happening():
            PieceView.display(neutreeko.get_board().get_move().get_piece())


def mouse_pressed():
    """ Catch mouse press event

    :param:
    :return:
    """
    neutreeko.process_press(mouse_x, mouse_y)


def mouse_released():
    """ Catch mouse release event

    :param:
    :return:
    """
    neutreeko.process_release()


def mouse_dragged():
    """ Catch mouse drag event

    :param:
    :return:
    """
    neutreeko.process_drag(mouse_x)


# run main loop
run(frame_rate=60)
