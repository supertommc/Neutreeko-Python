import app


class StaticResponse:
    def __init__(self, next_state):
        self.__next_state = next_state

    def on_press(self):
        app.neutreeko.set_state(self.__next_state)


class SlideResponse:
    def __init__(self, bot):
        self.__bot = bot

    def on_drag(self, button):
        app.neutreeko.set_depth_bot(self.__bot, button.get_current_value())
