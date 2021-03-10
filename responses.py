import app


class StaticResponse:
    def __init__(self, next_state):
        self.__next_state = next_state

    def on_press(self):
        app.neutreeko.set_state(self.__next_state)
