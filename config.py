from p5 import create_font


class Config:
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 700
    BACKGROUND_COLOR = (204, 204, 204)
    FONT_PATH = "fonts/TarrgetItalic-xzP8.otf"
    BOARD_IMAGE_PATH = "images/board.PNG"
    BLACK_PIECE_IMAGE_PATH = "images/blackPiece.png"
    WHITE_PIECE_IMAGE_PATH = "images/whitePiece.png"

    board_image = None
    black_piece_image = None
    white_piece_image = None

    @staticmethod
    def get_font_width_height(font_text, font_size):
        image_font = create_font(Config.FONT_PATH, font_size)
        font_size = image_font.getsize(font_text)
        return font_size[0], font_size[1]

    @staticmethod
    def get_circle_top_left_position(center_x, center_y, radius):
        return center_x - radius // 2, center_y - radius // 2



class State:
    MENU = 0
    PLAYER_VS_PLAYER = 1
    PLAYER_VS_BOT = 2
    BOT_VS_PLAYER = 3
    BOT_VS_BOT = 4
    GAME_OVER = 5