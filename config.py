from p5 import create_font


class Config:
    SCREEN_WIDTH = 700
    SCREEN_HEIGHT = 700
    FONT_PATH = "fonts/TarrgetItalic-xzP8.otf"

    @staticmethod
    def get_font_width_height(font_text, font_size):
        image_font = create_font(Config.FONT_PATH, font_size)
        font_size = image_font.getsize(font_text)
        return font_size[0], font_size[1]
