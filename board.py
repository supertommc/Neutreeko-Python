from moveGenerator import MoveGenerator
from gameUtils import GameUtils
from ai import AI
import config
from playermenu import PlayerMenu
from boardmenu import BoardMenu

"""
    Here are all object classes used in the board except board menu and players menus
"""


class Piece:

    def __init__(self, position, radius, player, color):
        self.__x, self.__y = position
        self.__radius = radius
        self.__player = player
        self.__color = color

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_position(self):
        return self.__x, self.__y

    def get_radius(self):
        return self.__radius

    def get_player(self):
        return self.__player

    def get_color(self):
        return self.__color

    def set_position(self, new_position):
        self.__x, self.__y = new_position


class Tile:

    def __init__(self, coords, position, edge, color):
        self.__coord_x, self.__coord_y = coords
        self.__x, self.__y = position
        self.__edge = edge
        self.__color = color
        self.__is_pressed = False
        self.__piece = None
        self.__piece_radius = 50

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_center_position(self):
        return self.__x + self.__edge // 2, self.__y + self.__edge // 2

    def get_coord_x(self):
        return self.__coord_x

    def get_coord_y(self):
        return self.__coord_y

    def get_coords(self):
        return self.__coord_x, self.__coord_y

    def get_position(self):
        return self.__x, self.__y

    def get_edge(self):
        return self.__edge

    def get_color(self):
        return self.__color

    def get_piece(self):
        return self.__piece

    def get_piece_position(self):
        return self.__x + self.__piece_radius, self.__y + self.__piece_radius

    def extract_piece(self):
        piece = self.__piece
        self.__piece = None
        return piece

    def get_piece_player(self):
        if self.__piece is not None:
            return self.__piece.get_player()
        return 0

    def insert_piece(self, new_piece):
        self.__piece = new_piece
        radius = self.__piece.get_radius()
        self.__piece.set_position((self.__x + radius, self.__y + radius))

    def has_piece(self):
        return self.__piece is not None

    def is_hover(self, mx, my):
        return self.__x < mx < self.__x + self.__edge and self.__y < my < self.__y + self.__edge

    def is_pressed(self):
        return self.__is_pressed

    def press(self, mx, my):
        if self.is_hover(mx, my):
            self.__is_pressed = not self.__is_pressed


class Move:

    def __init__(self, speed):
        self.__speed = speed

        self.__start_tile = None
        self.__dest_tile = None
        self.__piece = None
        self.__direction = None

    def set_start_tile(self, start_tile):
        self.__start_tile = start_tile

    def set_dest_tile(self, dest_tile):
        self.__dest_tile = dest_tile

    def set_piece(self, piece):
        self.__piece = piece

    def set_speed(self, new_speed):
        self.__speed = new_speed

    def get_start_tile(self):
        return self.__start_tile

    def get_dest_tile(self):
        return self.__dest_tile

    def get_piece(self):
        return self.__piece

    def get_coords(self):
        start_x, start_y = self.__start_tile.get_coords()
        dest_x, dest_y = self.__dest_tile.get_coords()

        return start_x, start_y, dest_x, dest_y

    def is_start_tile_selected(self):
        return self.__start_tile is not None

    def is_dest_tile_selected(self):
        return self.__dest_tile is not None

    def __update_direction(self):
        """ Update move direction vector
        """
        x = 0
        y = 0
        start_x, start_y, dest_x, dest_y = self.get_coords()

        if dest_x - start_x != 0:
            x = (dest_x - start_x) / abs(dest_x - start_x)

        if dest_y - start_y != 0:
            y = (dest_y - start_y) / abs(dest_y - start_y)

        self.__direction = (x, y)

    def update_piece_position(self):
        """ Update piece position depending on the move direction and move speed
        """
        piece_x, piece_y = self.__piece.get_position()
        direction_x, direction_y = self.__direction

        self.__piece.set_position((piece_x + direction_x * self.__speed, piece_y + direction_y * self.__speed))

    def piece_reach_dest_position(self):
        """ Verify if piece reach its destiny position
        """
        piece_x, piece_y = self.__piece.get_position()
        dest_x, dest_y = self.__dest_tile.get_piece_position()
        direction_x, direction_y = self.__direction
        offset_x = direction_x * self.__speed
        offset_y = direction_y * self.__speed

        reach_x = ((direction_x < 0) and (piece_x < dest_x - offset_x)) or ((direction_x > 0) and (piece_x > dest_x - offset_x))
        reach_y = ((direction_y < 0) and (piece_y < dest_y - offset_y)) or ((direction_y > 0) and (piece_y > dest_y - offset_y))

        return reach_x or reach_y

    def is_happening(self):
        return self.__piece is not None

    def start(self):
        """ Start piece move
        """
        self.__piece = self.__start_tile.extract_piece()
        self.__update_direction()

    def finish(self):
        """ Finish piece move
        """
        self.__dest_tile.insert_piece(self.__piece)
        self.reset()

    def reset(self):
        """ Reset Move
        """
        self.__piece = None
        self.__start_tile = None
        self.__dest_tile = None
        self.__direction = None


class ScoreBar:

    def __init__(self, position, width, height):
        self.__x, self.__y = position
        self.__width = width
        self.__height = height
        self.__current_bar_height = 0.5 * self.__height
        self.__range_values = AI.MAX_SCORE_NOT_WIN - AI.MIN_SCORE_NOT_LOSE

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def get_current_bar_height(self):
        return self.__current_bar_height

    def get_bar_x(self):
        return self.__x

    def get_bar_y(self):
        return self.__y + self.__height - self.__current_bar_height

    def reset(self):
        self.__current_bar_height = 0.5 * self.__height

    def update(self, player, score):
        """ Update bar based on player score

        :param player: player turn
        :param score: player score to use in the bar
        :return:
        """
        ratio = -1
        if player == 1:
            if score >= AI.WIN_SCORE:
                ratio = 1.0
            elif score <= AI.LOSE_SCORE:
                ratio = 0.0
            else:
                score_normalize = AI.MAX_SCORE_NOT_WIN + score
                ratio = score_normalize / self.__range_values

        elif player == 2:
            if score >= AI.WIN_SCORE:
                ratio = 0.0
            elif score <= AI.LOSE_SCORE:
                ratio = 1.0
            else:
                score_normalize = AI.MAX_SCORE_NOT_WIN - score
                ratio = score_normalize / self.__range_values

        self.__current_bar_height = self.__height * ratio


class Hint:

    def __init__(self, start_move_position, dest_move_position):
        self.__start_x, self.__start_y = start_move_position
        self.__start_move_position = start_move_position
        self.__dest_x, self.__dest_y = dest_move_position
        self.__dest_move_position = dest_move_position
        self.__line_color = (255, 0, 0)

    def get_start_move_position(self):
        return self.__start_move_position

    def get_dest_move_position(self):
        return self.__dest_move_position

    def get_line_color(self):
        return self.__line_color


class Board:

    def __init__(self, opening_book, state, initial_speed):
        self.__opening_book = opening_book
        self.__initial_game_state = state
        self.__game_state = state
        self.__state = config.BoardState.PLAYER_TURN

        self.__x = 100
        self.__y = 100
        self.__edge = 500

        self.__pieces_radius = 50
        self.__player_1_pieces_color = (255, 0, 0)
        self.__player_2_pieces_color = (255, 255, 255)

        self.__tiles = []
        self.__tiles_color = (255, 255, 255)
        self.__create_tiles()
        self.__insert_pieces_from_state()

        self.__player_turn = 1

        self.__played_states = {}
        self.__played_moves = []

        self.__move = Move(initial_speed)

        self.__player_1_resign = False
        self.__player_2_resign = False
        self.__draw_accepted = False
        self.__game_over = False

        self.__computer_processing = False
        self.__opening_book_active = True

        self.__score_bar_x = self.__x + self.__edge + 50
        self.__score_bar_y = self.__y
        self.__score_bar_width = 50
        self.__score_bar_height = self.__edge
        self.__score_bar = ScoreBar((self.__score_bar_x, self.__score_bar_y), self.__score_bar_width, self.__score_bar_height)

        self.__board_menu_width = 150
        self.__board_menu_height = 300
        self.__board_menu_x = self.__score_bar_x + self.__score_bar_width + 50
        self.__board_menu_y = self.__y + self.__edge // 2 - self.__board_menu_height // 2
        self.__board_menu = BoardMenu((self.__board_menu_x, self.__board_menu_y), self.__board_menu_width, self.__board_menu_height)

        self.__player_1_menu = PlayerMenu(1, (self.__x, self.__y + self.__edge + 10))
        self.__player_2_menu = PlayerMenu(2, (self.__x, 50))

        self.__player_1_menu.update(config.BoardState.PLAYER_TURN)
        self.__player_2_menu.update(config.BoardState.WAIT)

        self.__hint = None

    def __create_tiles(self):
        """ Create board tiles
        """
        for row in range(5):
            for col in range(5):
                tile = Tile((col, row), self.__get_tile_position(col, row), self.__edge // 5, self.__tiles_color)
                self.__tiles.append(tile)

    def __get_tile_position(self, col, row):
        return self.__x * (col + 1), self.__y * (row + 1)

    def __insert_pieces_from_state(self):
        """ Insert pieces in board tiles
        """
        i = 0
        for row in range(len(self.__game_state)):
            for col in range(len(self.__game_state[0])):
                if self.__game_state[row][col] != 0:
                    piece = Piece((0, 0), self.__pieces_radius, self.__game_state[row][col],
                                  self.__get_piece_color(self.__game_state[row][col]))
                    self.__tiles[i].insert_piece(piece)
                i += 1

    def __get_piece_color(self, player):
        if player == 1:
            return self.__player_1_pieces_color
        elif player == 2:
            return self.__player_2_pieces_color
        return None

    def get_tiles(self):
        return self.__tiles

    def get_move(self):
        return self.__move

    def get_score_bar(self):
        return self.__score_bar

    def get_board_menu(self):
        return self.__board_menu

    def get_player_menu(self, player):
        if player == 1:
            return self.__player_1_menu
        elif player == 2:
            return self.__player_2_menu
        return None

    def get_player_turn(self):
        return self.__player_turn

    def get_state(self):
        return self.__game_state

    def get_played_moves(self):
        return self.__played_moves

    def get_hint(self):
        return self.__hint

    def is_computer_processing(self):
        return self.__computer_processing

    def is_opening_book_active(self):
        return self.__opening_book_active

    def is_game_over(self):
        return self.__game_over

    def resign_player(self, player):
        if player == 1:
            self.__player_1_resign = True
        elif player == 2:
            self.__player_2_resign = True

    def accept_draw(self):
        self.__draw_accepted = True

    def set_game_state(self, new_state):
        self.__game_state = new_state
        self.__insert_pieces_from_state()

    def set_opening_book_active(self, is_active):
        self.__opening_book_active = is_active

    def __update_game_state(self):
        """ Create the state matrix filled with zeros and update the state matrix based on the tiles pieces
        """
        self.__game_state = [[0] * 5 for _ in range(5)]

        for tile in self.__tiles:
            self.__game_state[tile.get_coord_y()][tile.get_coord_x()] = tile.get_piece_player()

    def __change_turn(self):
        """ Change player turn, updating the states of players menu
        """
        if self.__player_turn == 1:
            self.__player_turn = 2
            self.__player_1_menu.update(config.BoardState.WAIT)
            self.__player_2_menu.update(config.BoardState.PLAYER_TURN)

        elif self.__player_turn == 2:
            self.__player_turn = 1
            self.__player_1_menu.update(config.BoardState.PLAYER_TURN)
            self.__player_2_menu.update(config.BoardState.WAIT)

    def finish_piece_move(self):
        """ Finish piece move, store move, update game state and change player turn
        """
        self.__store_played_states()
        self.__store_move(self.__move.get_coords())
        self.__move.finish()
        self.__update_game_state()
        self.__change_turn()

        self.__hint = None

    def __apply_move(self, move):
        """ Apply move based on the current game state and start move animation

        :param move:
        :return:
        """
        initial_x, initial_y, final_x, final_y = move

        for tile in self.__tiles:
            if tile.get_coords() == (initial_x, initial_y):
                self.__move.set_start_tile(tile)

            elif tile.get_coords() == (final_x, final_y):
                self.__move.set_dest_tile(tile)

        self.__move.start()

    def __move_is_valid(self):
        """ Verify if the move is valid

        :return: True if move is in list of valid moves, else return False
        """
        move = self.__move.get_coords()
        valid_moves = MoveGenerator.generate_all_moves(self.__game_state, self.__player_turn)

        return move in valid_moves

    def __is_draw(self):
        """ Verify if the game end with a draw

        :return: True if it was a draw, else return False
        """
        for val in self.__played_states.values():
            if val == 3:
                return True
        return False

    def check_game_over(self):
        """ Verify if the game ended, updating the board view based on the board state

        :return:
        """

        if self.__is_draw() or self.__draw_accepted:
            self.__player_1_menu.update(config.BoardState.DRAW)
            self.__player_2_menu.update(config.BoardState.DRAW)
            self.__game_over = True

        result = GameUtils.check_game_over_full(self.__game_state)

        if (result == 1) or self.__player_2_resign:
            self.__player_1_menu.update(config.BoardState.WIN)
            self.__player_2_menu.update(config.BoardState.LOSE)
            self.__game_over = True

        elif (result == 2) or self.__player_1_resign:
            self.__player_1_menu.update(config.BoardState.LOSE)
            self.__player_2_menu.update(config.BoardState.WIN)
            self.__game_over = True

    def offer_draw_player(self, player):
        """ Player offer a draw to the opponent

        :param player: Player that offered a draw
        :return:
        """

        if player == 1:
            self.__player_1_menu.update(config.BoardState.OFFER_DRAW)
            self.__player_2_menu.update(config.BoardState.OPPONENT_OFFER_DRAW)

        elif player == 2:
            self.__player_1_menu.update(config.BoardState.OPPONENT_OFFER_DRAW)
            self.__player_2_menu.update(config.BoardState.OFFER_DRAW)

    def cancel_draw(self):
        """ The draw offer is canceled
        """
        if self.__player_turn == 1:
            self.__player_1_menu.update(config.BoardState.PLAYER_TURN)
            self.__player_2_menu.update(config.BoardState.WAIT)
        elif self.__player_turn == 2:
            self.__player_1_menu.update(config.BoardState.WAIT)
            self.__player_2_menu.update(config.BoardState.PLAYER_TURN)

    def __store_played_states(self):
        """ Store every position in a dictionary, which the key is the position and the value is the number of times
        that the position occurs
        """
        item = GameUtils.full_game_to_tuple(self.__game_state)
        if item in self.__played_states.keys():
            self.__played_states[item] += 1
        else:
            self.__played_states[item] = 1

    def __store_move(self, move):
        self.__played_moves.append(move)

    def generate_hint(self, depth, hints):
        """ Generate a hint for the corresponding player turn and create a Hint object to be drawn on the board

        :param depth: depth of the hint
        :param hints: hint bots of player 1 and player 2
        :return:
        """
        score, move = hints[self.__player_turn].minimax_alpha_beta_with_move_faster_order(True, self.__player_turn, self.__game_state, depth, AI.MIN, AI.MAX)
        start_x, start_y, dest_x, dest_y = move

        start_position = None
        dest_position = None

        for tile in self.__tiles:
            if tile.get_coords() == (start_x, start_y):
                start_position = tile.get_center_position()

            elif tile.get_coords() == (dest_x, dest_y):
                dest_position = tile.get_center_position()

        self.__hint = Hint(start_position, dest_position)

    def apply_bot_move(self, depths_bots, player_bots, opening_book):
        """ Apply the bot move. If the opening book is active and set, the bot will use the opening database sequence,
        else it will generate a move using minimax with alpha beta cuts

        :param depths_bots: depth of the bot corresponding to player 1 and player 2 dictionary
        :param player_bots: player 1 bot and player 2 dictionary
        :param opening_book: opening book object which finds the next sequence move
        :return:
        """

        move = None
        score = 0

        if opening_book is None:
            self.__opening_book_active = False

        if self.__opening_book_active:
            move = opening_book.find_next_move(self.__played_moves, self.__player_turn)
            print("Opening move: {}".format(move))
            if move is None:
                self.__opening_book_active = False

        if not self.__opening_book_active:
            score, move = player_bots[self.__player_turn].minimax_alpha_beta_with_move_faster_order(True, self.__player_turn, self.__game_state, depths_bots[self.__player_turn], AI.MIN, AI.MAX)
            print("Move: " + str(move) + " with a score of " + str(score) + " of player: " + str(self.__player_turn))

        self.__score_bar.update(self.__player_turn, score)
        self.__apply_move(move)
        self.__state = config.BoardState.PLAYER_TURN

    def press(self, mx, my):
        """ Process mouse event when the mouse is pressed over the board
        The user can select the tiles to the move using mouse presses of the specifics tiles and also the user can
        press the board menus buttons for example to offer draw, resign, leave, restart game or get a hint

        :param mx: x coord of mouse
        :param my: y coord of mouse
        """

        self.__board_menu.press(mx, my)
        self.__player_1_menu.press(mx, my)
        self.__player_2_menu.press(mx, my)

        if not self.__move.is_start_tile_selected():
            for tile in self.__tiles:
                if tile.is_hover(mx, my):
                    if tile.get_piece() is None:
                        return
                    if tile.get_piece().get_player() != self.__player_turn:
                        return
                    self.__move.set_start_tile(tile)
                    print("Start tile: {}".format(self.__move.get_start_tile().get_coords()))
                    break

        elif not self.__move.is_dest_tile_selected():
            for tile in self.__tiles:
                if tile.is_hover(mx, my):
                    if tile.get_coords() == self.__move.get_start_tile().get_coords():
                        return
                    self.__move.set_dest_tile(tile)
                    print("Dest tile: {}".format(self.__move.get_dest_tile().get_coords()))
                    break

            if self.__move_is_valid():
                self.__move.start()

            else:
                print("Invalid Move!")
                self.__move.reset()
