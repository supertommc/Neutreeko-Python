import button
import config
import responses


class PlayerMenu:
    def __init__(self, position):
        self.__x, self.__y = position
        self.__turn_text = "YOUR TURN"
        self.__win_text = "YOU WIN"
        self.__lose_text = "YOU LOSE"
        self.__draw_text = "DRAW"
        self.__text_font_size = 20
        self.__text_color = (0, 0, 0)

        self.__buttons_width = 150
        self.__buttons_height = 40
        self.__buttons_color = (0, 0, 0)
        self.__buttons_background_color = (90, 90, 90)
        self.__buttons_pressed_color_offset = 20
        self.__buttons_font_size = 16
        self.__buttons_y = self.__y
        self.__left_button_x = self.__x
        self.__right_button_x = self.__x + 350

        self.__rematch_button = None
        self.__rematch_button_text = "Rematch"
        self.__rematch_button_response = responses.ChangeStateResponse(config.State.PLAYER_VS_PLAYER)

        self.__leave_button = None
        self.__leave_button_text = "Leave"
        self.__leave_button_response = responses.ChangeStateResponse(config.State.MENU)

        self.__resign_button = None
        self.__resign_button_text = "Resign"
        self.__resign_button_response = responses.ChangeStateResponse(config.State.PLAYER_VS_PLAYER)

        self.__offer_draw_button = None
        self.__offer_draw_button_text = "Offer draw"
        self.__offer_draw_button_response = responses.ChangeStateResponse(config.State.MENU)

        self.__cancel_draw_button = None
        self.__cancel_draw_button_text = "Cancel draw"
        self.__cancel_draw_button_response = responses.ChangeStateResponse(config.State.MENU)

        self.__accept_draw_button = None
        self.__accept_draw_button_text = "Accept draw"
        self.__accept_draw_button_response = responses.ChangeStateResponse(config.State.MENU)

        self.__decline_draw_button = None
        self.__decline_draw_button_text = "Decline draw"
        self.__decline_draw_button_response = responses.ChangeStateResponse(config.State.MENU)

        self.__current_text = self.__turn_text
        self.__text_x = 0
        self.__text_y = self.__y + 10
        self.__update_text_position()

        self.__current_buttons_list = []
        self.__create_buttons()

    def __create_buttons(self):

        self.__rematch_button = button.Button((self.__left_button_x, self.__buttons_y), self.__buttons_width,
                                              self.__buttons_height, self.__buttons_color,
                                              self.__buttons_background_color,
                                              self.__buttons_pressed_color_offset,
                                              self.__rematch_button_text, self.__buttons_font_size,
                                              self.__rematch_button_response)

        self.__resign_button = button.Button((self.__left_button_x, self.__buttons_y), self.__buttons_width,
                                             self.__buttons_height, self.__buttons_color,
                                             self.__buttons_background_color,
                                             self.__buttons_pressed_color_offset,
                                             self.__resign_button_text, self.__buttons_font_size,
                                             self.__resign_button_response)

        self.__leave_button = button.Button((self.__right_button_x, self.__buttons_y), self.__buttons_width,
                                            self.__buttons_height, self.__buttons_color,
                                            self.__buttons_background_color,
                                            self.__buttons_pressed_color_offset,
                                            self.__leave_button_text, self.__buttons_font_size,
                                            self.__leave_button_response)

        self.__offer_draw_button = button.Button((self.__right_button_x, self.__buttons_y), self.__buttons_width,
                                                 self.__buttons_height, self.__buttons_color,
                                                 self.__buttons_background_color,
                                                 self.__buttons_pressed_color_offset,
                                                 self.__offer_draw_button_text, self.__buttons_font_size,
                                                 self.__offer_draw_button_response)

        self.__cancel_draw_button = button.Button((self.__right_button_x, self.__buttons_y), self.__buttons_width,
                                                  self.__buttons_height, self.__buttons_color,
                                                  self.__buttons_background_color,
                                                  self.__buttons_pressed_color_offset,
                                                  self.__cancel_draw_button_text, self.__buttons_font_size,
                                                  self.__cancel_draw_button_response)

        self.__accept_draw_button = button.Button((self.__left_button_x, self.__buttons_y), self.__buttons_width,
                                                  self.__buttons_height, self.__buttons_color,
                                                  self.__buttons_background_color,
                                                  self.__buttons_pressed_color_offset,
                                                  self.__accept_draw_button_text, self.__buttons_font_size,
                                                  self.__accept_draw_button_response)

        self.__decline_draw_button = button.Button((self.__right_button_x, self.__buttons_y), self.__buttons_width,
                                                   self.__buttons_height, self.__buttons_color,
                                                   self.__buttons_background_color,
                                                   self.__buttons_pressed_color_offset,
                                                   self.__decline_draw_button_text, self.__buttons_font_size,
                                                   self.__decline_draw_button_response)

    def get_text_font_size(self):
        return self.__text_font_size

    def get_text_color(self):
        return self.__text_color

    def get_text_x(self):
        return self.__text_x

    def get_text_y(self):
        return self.__text_y

    def get_current_text(self):
        return self.__current_text

    def get_current_buttons_list(self):
        return self.__current_buttons_list

    def __update_text_position(self):
        text_width, _ = config.Config.get_font_width_height(self.__current_text, self.__text_font_size)
        self.__text_x = self.__x + 250 - text_width / 2

    def update(self, state):
        self.__current_buttons_list.clear()

        if state == config.BoardState.WAIT:
            self.__current_text = ""
            self.__current_buttons_list.append(self.__resign_button)
            self.__current_buttons_list.append(self.__offer_draw_button)

        elif state == config.BoardState.PLAYER_TURN:
            self.__current_text = self.__turn_text
            self.__update_text_position()
            self.__current_buttons_list.append(self.__resign_button)
            self.__current_buttons_list.append(self.__offer_draw_button)

        elif state == config.BoardState.OFFER_DRAW:
            self.__current_text = self.__turn_text
            self.__update_text_position()
            self.__current_buttons_list.append(self.__resign_button)
            self.__current_buttons_list.append(self.__cancel_draw_button)

        elif state == config.BoardState.OPPONENT_OFFERED_DRAW:
            self.__current_text = self.__turn_text
            self.__update_text_position()
            self.__current_buttons_list.append(self.__resign_button)
            self.__current_buttons_list.append(self.__accept_draw_button)
            self.__current_buttons_list.append(self.__decline_draw_button)

        elif state == config.BoardState.WIN:
            self.__current_text = self.__win_text
            self.__update_text_position()
            self.__current_buttons_list.append(self.__rematch_button)
            self.__current_buttons_list.append(self.__leave_button)

        elif state == config.BoardState.LOSE:
            self.__current_text = self.__lose_text
            self.__update_text_position()
            self.__current_buttons_list.append(self.__rematch_button)
            self.__current_buttons_list.append(self.__leave_button)

        elif state == config.BoardState.DRAW:
            self.__current_text = self.__draw_text
            self.__update_text_position()
            self.__current_buttons_list.append(self.__rematch_button)
            self.__current_buttons_list.append(self.__leave_button)

        else:
            print("Invalid state!")

    def press(self, mx, my):
        for current_button in self.__current_buttons_list:
            current_button.press(mx, my)
