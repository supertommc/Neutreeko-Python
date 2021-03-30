import pygame
from app import *
from config import Config, State
import pygame.image
import pygame.mouse


class ButtonView:
    @staticmethod
    def display(button, screen):

        # draw button background
        offset = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button.is_hover(mouse_x, mouse_y):
            offset = button.get_pressed_color_offset()

        rect = pygame.Rect(button.get_x(), button.get_y(), button.get_width(), button.get_height())
        rect_color = (button.get_background_color()[0] + offset, button.get_background_color()[1] + offset, button.get_background_color()[2] + offset)
        pygame.draw.rect(screen, rect_color, rect)

        # draw button text
        my_font = pygame.font.Font(Config.FONT_PATH, button.get_text_size())  # Load font object.
        text_image = my_font.render(button.get_text(), True, button.get_color())  # Render text image.
        screen.blit(text_image, button.get_position())  # Draw image to screen.


class SlideButtonView:
    @staticmethod
    def display(button, screen):

        # draw button background
        offset = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button.is_hover(mouse_x, mouse_y):
            offset = button.get_pressed_color_offset()

        rect = pygame.Rect(button.get_x(), button.get_y(), button.get_width(), button.get_height())
        rect_color = (button.get_background_color()[0] + offset, button.get_background_color()[1] + offset,
                      button.get_background_color()[2] + offset)
        pygame.draw.rect(screen, rect_color, rect)

        # draw bar
        offset = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button.is_hover(mouse_x, mouse_y):
            offset = button.get_pressed_color_offset()

        rect = pygame.Rect(button.get_bar_x(), button.get_bar_y(), button.get_bar_width(), button.get_bar_height())
        rect_color = (button.get_bar_color()[0] + offset, button.get_bar_color()[1] + offset,
                      button.get_bar_color()[2] + offset)
        pygame.draw.rect(screen, rect_color, rect)

        # draw button text
        my_font = pygame.font.Font(Config.FONT_PATH, button.get_text_size())  # Load font object.
        text_image = my_font.render(button.get_text(), True, button.get_color())  # Render text image.
        screen.blit(text_image, button.get_position())  # Draw image to screen.


class MainMenuView:
    @staticmethod
    def display(main_menu, screen):

        # display title
        my_font = pygame.font.Font(Config.FONT_PATH, main_menu.get_title_font_size())
        text_image = my_font.render(main_menu.get_title_text(), True, main_menu.get_title_color())
        screen.blit(text_image, main_menu.get_title_position())

        # display buttons
        ButtonView.display(main_menu.get_player_vs_player_button(), screen)
        ButtonView.display(main_menu.get_player_vs_bot_button(), screen)
        ButtonView.display(main_menu.get_bot_vs_player_button(), screen)
        ButtonView.display(main_menu.get_bot_vs_bot_button(), screen)
        ButtonView.display(main_menu.get_options_button(), screen)


class OptionsMenuView:
    @staticmethod
    def display(options_menu, screen):
        # display title
        my_font = pygame.font.Font(Config.FONT_PATH, options_menu.get_title_font_size())
        text_image = my_font.render(options_menu.get_title_text(), True, options_menu.get_title_color())
        screen.blit(text_image, options_menu.get_title_position())

        # display buttons
        for i in range(3):
            SlideButtonView.display(options_menu.get_depth_slide_button(i), screen)
            ButtonView.display(options_menu.get_evaluation_toggle_button(i), screen)
        ButtonView.display(options_menu.get_opening_book_toggle_button(), screen)
        ButtonView.display(options_menu.get_back_button(), screen)


class PieceView:

    @staticmethod
    def display(piece, screen):
        if piece.get_player() == 1:
            black_piece_image_rect = Config.black_piece_image.get_rect()
            black_piece_image_rect = black_piece_image_rect.move(Config.get_circle_top_left_position(piece.get_x(), piece.get_y(), piece.get_radius()))
            screen.blit(Config.black_piece_image, black_piece_image_rect)

        elif piece.get_player() == 2:
            white_piece_image_rect = Config.white_piece_image.get_rect()
            white_piece_image_rect = white_piece_image_rect.move(Config.get_circle_top_left_position(piece.get_x(), piece.get_y(), piece.get_radius()))
            screen.blit(Config.white_piece_image, white_piece_image_rect)


class TileView:

    @staticmethod
    def display(tile):
        fill(tile.get_color()[0], tile.get_color()[1], tile.get_color()[2])
        square(tile.get_position(), tile.get_edge())


class ScoreBarView:

    @staticmethod
    def display(score_bar, screen):
        black_pieces_color = config.Config.BLACK_PIECES_COLOR
        white_pieces_color = config.Config.WHITE_PIECES_COLOR

        rect = pygame.Rect(score_bar.get_x(), score_bar.get_y(), score_bar.get_width(), score_bar.get_height())
        pygame.draw.rect(screen, white_pieces_color, rect)

        rect = pygame.Rect(score_bar.get_bar_x(), score_bar.get_bar_y(), score_bar.get_width(), score_bar.get_current_bar_height())
        pygame.draw.rect(screen, black_pieces_color, rect)


class PlayerMenuView:

    @staticmethod
    def display(player_menu, screen):

        my_font = pygame.font.Font(Config.FONT_PATH, player_menu.get_text_font_size())
        text_image = my_font.render(player_menu.get_current_text(), True, player_menu.get_text_color())
        screen.blit(text_image, player_menu.get_text_position())

        # display buttons
        for button in player_menu.get_current_buttons_list():
            ButtonView.display(button, screen)


class BoardMenuView:

    @staticmethod
    def display(board_menu, screen):

        # display buttons
        for button in board_menu.get_buttons():
            ButtonView.display(button, screen)


class HintView:

    @staticmethod
    def display(hint, screen):

        # display hint line
        pygame.draw.line(screen, hint.get_line_color(), hint.get_start_move_position(), hint.get_dest_move_position())


class BoardView:

    @staticmethod
    def display(game_board, screen):

        # display board
        image_rect = Config.board_image.get_rect()
        image_rect = image_rect.move((100, 100))
        screen.blit(Config.board_image, image_rect)

        # display pieces
        for tile in game_board.get_tiles():
            if tile.has_piece():
                PieceView.display(tile.get_piece(), screen)

        ScoreBarView.display(game_board.get_score_bar(), screen)
        BoardMenuView.display(game_board.get_board_menu(), screen)
        PlayerMenuView.display(game_board.get_player_menu(1), screen)
        PlayerMenuView.display(game_board.get_player_menu(2), screen)

        if game_board.get_hint() is not None:
            HintView.display(game_board.get_hint(), screen)


def draw(screen):

    neutreeko.update()

    if neutreeko.get_state() == State.MAIN_MENU:
        MainMenuView.display(neutreeko.get_main_menu(), screen)

    elif neutreeko.get_state() == State.OPTIONS_MENU:
        OptionsMenuView.display(neutreeko.get_options_menu(), screen)

    else:
        BoardView.display(neutreeko.get_board(), screen)

        if neutreeko.get_board().get_move().is_happening():
            PieceView.display(neutreeko.get_board().get_move().get_piece(), screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("NEUTREEKO")
    Config.board_image = pygame.image.load(Config.BOARD_IMAGE_PATH)
    Config.black_piece_image = pygame.image.load(Config.BLACK_PIECE_IMAGE_PATH)
    Config.white_piece_image = pygame.image.load(Config.WHITE_PIECE_IMAGE_PATH)

    clock = pygame.time.Clock()
    dt = 0
    while True:

        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            elif e.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                neutreeko.process_press(mouse_x, mouse_y)
            elif e.type == pygame.MOUSEBUTTONUP:
                neutreeko.process_release()
            elif e.type == pygame.MOUSEMOTION:
                mouse_x, _ = pygame.mouse.get_pos()
                neutreeko.process_drag(mouse_x)

        screen.fill(Config.BACKGROUND_COLOR)
        draw(screen)
        pygame.display.update()

        dt = clock.tick(120)

        pygame.display.flip()


if __name__ == '__main__':
    main()
