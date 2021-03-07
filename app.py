class State:
    MENU = 0
    PLAYER_VS_PLAYER = 1
    PLAYER_VS_BOT = 2
    BOT_VS_PLAYER = 3
    BOT_VS_BOT = 4
    GAME_OVER = 5


class Newtreeko:

    def __init__(self, initial_application_state):
        self.__current_application_state = initial_application_state

        self.__current_game_state = [
                                        [0, 2, 0, 2, 0],
                                        [0, 0, 1, 0, 0],
                                        [0, 0, 0, 0, 0],
                                        [0, 0, 2, 0, 0],
                                        [0, 1, 0, 1, 0]
                                    ]

        self.__current_player = 1
        self.__depth = 6
