class Config:
    """
        Application configurations
    """
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    BACKGROUND_COLOR = (204, 204, 204)
    BLACK_PIECES_COLOR = (0, 0, 0)
    WHITE_PIECES_COLOR = (255, 255, 255)
    FONT_PATH = "fonts/TarrgetItalic-xzP8.otf"
    BOARD_IMAGE_PATH = "images/board.PNG"
    BLACK_PIECE_IMAGE_PATH = "images/blackPiece.png"
    WHITE_PIECE_IMAGE_PATH = "images/whitePiece.png"

    board_image = None
    black_piece_image = None
    white_piece_image = None

    @staticmethod
    def get_circle_top_left_position(center_x, center_y, radius):
        return center_x - radius // 2, center_y - radius // 2


class State:
    """
        Application States Enumerator
    """
    MAIN_MENU = 0
    OPTIONS_MENU = 1
    PLAYER_VS_PLAYER = 2
    PLAYER_VS_BOT = 3
    BOT_VS_PLAYER = 4
    BOT_VS_BOT = 5


class BoardState:
    """
        Board States Enumerator
    """
    PLAYER_TURN = 0
    OFFER_DRAW = 1
    OPPONENT_OFFER_DRAW = 2
    WIN = 3
    LOSE = 4
    DRAW = 5
    WAIT = 6
