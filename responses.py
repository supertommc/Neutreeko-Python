import app
from config import State


class ChangeStateResponse:
    def __init__(self, next_state):
        self.__next_state = next_state

    def on_press(self):
        app.neutreeko.set_state(self.__next_state)


class SlideResponse:
    def __init__(self, bot):
        self.__bot = bot

    def on_drag(self, button):
        app.neutreeko.set_depth_bot(self.__bot, button.get_current_value())


class RematchResponse:

    @staticmethod
    def on_press():
        app.neutreeko.get_board().reset()


class RestartResponse:

    @staticmethod
    def on_press():
        app.neutreeko.get_board().reset()


class LeaveResponse:
    def __init__(self, board):
        self.__board = board

    def on_press(self):
        self.__board.reset()
        app.neutreeko.set_state(State.MENU)


class ResignResponse:
    def __init__(self, player):
        self.__player = player

    def on_press(self):
        app.neutreeko.get_board().resign_player(self.__player)


class OfferDrawResponse:
    def __init__(self, player):
        self.__player = player

    def on_press(self):
        app.neutreeko.get_board().offer_draw_player(self.__player)


class CancelDrawResponse:

    @staticmethod
    def on_press():
        app.neutreeko.get_board().cancel_draw()


class AcceptDrawResponse:

    @staticmethod
    def on_press():
        app.neutreeko.get_board().accept_draw()


class HintResponse:

    @staticmethod
    def on_press():
        app.neutreeko.generate_hint()
