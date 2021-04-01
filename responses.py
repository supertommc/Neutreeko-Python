import app
from config import State

"""
    Here are all responses used on buttons in menus and in board
"""


class ChangeStateResponse:
    """ Response to Button to change application state
    """
    def __init__(self, next_state):
        self.__next_state = next_state

    def on_press(self):
        app.neutreeko.set_state(self.__next_state)


class BotDepthSlideResponse:
    """ Response to SlideButton to change bot depth
    """
    def __init__(self, bot):
        self.__bot = bot

    def on_drag(self, button):
        app.neutreeko.set_depth_bot(self.__bot, button.get_current_value())


class SpeedSlideResponse:
    """ Response to SlideButton to change move speed
    """
    @staticmethod
    def on_drag(button):
        app.neutreeko.set_move_speed(button.get_current_value())


class RematchResponse:
    """ Response to Button to make a game rematch
    """
    @staticmethod
    def on_press():
        app.neutreeko.reset_board()


class LeaveResponse:
    """ Response to Button to leave game
    """
    @staticmethod
    def on_press():
        app.neutreeko.reset_board()
        app.neutreeko.set_state(State.MAIN_MENU)


class ResignResponse:
    """ Response to Button to resign game
    """
    def __init__(self, player):
        self.__player = player

    def on_press(self):
        app.neutreeko.get_board().resign_player(self.__player)


class OfferDrawResponse:
    """ Response to Button to offer a draw to opponent
    """
    def __init__(self, player):
        self.__player = player

    def on_press(self):
        app.neutreeko.get_board().offer_draw_player(self.__player)


class CancelDrawResponse:
    """ Response to Button to cancel the opponent draw offer
    """
    @staticmethod
    def on_press():
        app.neutreeko.get_board().cancel_draw()


class AcceptDrawResponse:
    """ Response to Button to accept the opponent draw offer
    """
    @staticmethod
    def on_press():
        app.neutreeko.get_board().accept_draw()


class HintResponse:
    """ Response to Button to ask for a hint to bot
    """
    @staticmethod
    def on_press():
        app.neutreeko.generate_hint()


class EvaluationToggleResponse:
    """ Response to ToggleButton to change the bot evaluation function
    """
    def __init__(self, bot):
        self.__bot = bot

    def on_press(self, button):
        if self.__bot == 0:
            hint_bots = app.neutreeko.get_hint_bots()
            hint_bots[1].change_current_evaluation_function(button.get_current_value())
            hint_bots[2].change_current_evaluation_function(button.get_current_value())
        else:
            player_bots = app.neutreeko.get_player_bots()
            player_bots[self.__bot].change_current_evaluation_function(button.get_current_value())


class OpeningBookToggleResponse:
    """ Response to ToggleButton to change the use of the opening book
    """
    @staticmethod
    def on_press(button):
        if button.get_current_value() == "ON":
            app.neutreeko.set_use_opening_book(True)
        elif button.get_current_value() == "OFF":
            app.neutreeko.set_use_opening_book(False)
        else:
            print("Invalid current value")
