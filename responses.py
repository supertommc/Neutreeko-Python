import app
from config import State
from threading import Thread


"""
    Here are all responses used on buttons in menus and in board
"""


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
        # app.neutreeko.get_board().reset()
        app.neutreeko.reset_board()


class RestartResponse:

    @staticmethod
    def on_press():
        # app.neutreeko.get_board().reset()
        app.neutreeko.reset_board()


class LeaveResponse:

    @staticmethod
    def on_press():
        app.neutreeko.reset_board()
        # app.neutreeko.get_board().reset()
        app.neutreeko.set_state(State.MAIN_MENU)


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
        # app.neutreeko.join_hint_thread()
        # thread = Thread(target=app.neutreeko.generate_hint)
        # thread.start()
        # app.neutreeko.set_hint_thread(thread)


class EvaluationToggleResponse:
    def __init__(self, bot):
        self.__bot = bot

    @staticmethod
    def on_press(button):
        # TODO: Implement this
        pass


class OpeningBookToggleResponse:

    @staticmethod
    def on_press(button):
        if button.get_current_value() == "ON":
            app.neutreeko.set_use_opening_book(True)
        elif button.get_current_value() == "OFF":
            app.neutreeko.set_use_opening_book(False)
        else:
            print("Invalid current value")
