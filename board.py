from moveGenerator import generate_all_moves
from gameUtils import GameUtils
from ai import AI
from boardmenu import BoardMenu
import config


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

    def __init__(self):
        self.__move_speed = 30

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
        x = 0
        y = 0
        start_x, start_y, dest_x, dest_y = self.get_coords()

        if dest_x - start_x != 0:
            x = (dest_x - start_x) / abs(dest_x - start_x)

        if dest_y - start_y != 0:
            y = (dest_y - start_y) / abs(dest_y - start_y)

        self.__direction = (x, y)

    def update_piece_position(self):
        piece_x, piece_y = self.__piece.get_position()
        direction_x, direction_y = self.__direction

        self.__piece.set_position((piece_x + direction_x * self.__move_speed, piece_y + direction_y * self.__move_speed))

    def piece_reach_dest_position(self):
        piece_x, piece_y = self.__piece.get_position()
        dest_x, dest_y = self.__dest_tile.get_piece_position()
        direction_x, direction_y = self.__direction
        offset_x = direction_x * self.__move_speed
        offset_y = direction_y * self.__move_speed

        reach_x = ((direction_x < 0) and (piece_x < dest_x - offset_x)) or ((direction_x > 0) and (piece_x > dest_x - offset_x))
        reach_y = ((direction_y < 0) and (piece_y < dest_y - offset_y)) or ((direction_y > 0) and (piece_y > dest_y - offset_y))

        return reach_x or reach_y

    def is_happening(self):
        return self.__piece is not None

    def start(self):
        self.__piece = self.__start_tile.extract_piece()
        self.__update_direction()

    def finish(self):
        self.__dest_tile.insert_piece(self.__piece)
        self.reset()

    def reset(self):
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
        self.__winning_offset = 5

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

    def get_bar_y(self):
        return self.__y + self.__height - self.__current_bar_height

    def update(self, player, score):
        ratio = -1
        if player == 1:
            if score >= AI.WIN_SCORE:
                ratio = 1.0
            elif score <= AI.LOSE_SCORE:
                ratio = 0.0
            else:
                score_normalize = AI.MAX_SCORE_NOT_WIN + score
                ratio = (score_normalize / (self.__range_values + self.__winning_offset))

        elif player == 2:
            if score >= AI.WIN_SCORE:
                ratio = 0.0
            elif score <= AI.LOSE_SCORE:
                ratio = 1.0
            else:
                score_normalize = AI.MAX_SCORE_NOT_WIN - score
                ratio = (score_normalize / (self.__range_values + self.__winning_offset))

        self.__current_bar_height = self.__height * ratio


class Board:

    def __init__(self, state):
        self.__initial_game_state = state
        self.__game_state = state
        self.__state = config.BoardState.PLAYER_TURN

        self.__move = Move()

        self.__score_bar_position = (650, 100)
        self.__score_bar_width = 50
        self.__score_bar_height = 500
        self.__score_bar = ScoreBar(self.__score_bar_position, self.__score_bar_width, self.__score_bar_height)

        self.__board_menu_position = (750, 100)
        self.__board_menu = BoardMenu(self.__board_menu_position)

        self.__x = 100
        self.__y = 100
        self.__edge = 500

        self.__tiles = []
        self.__tiles_color = (255, 255, 255)

        self.__pieces_radius = 50
        self.__player_1_pieces_color = (255, 0, 0)
        self.__player_2_pieces_color = (255, 255, 255)

        self.__player_turn = 1

        self.__create_tiles()
        self.__insert_pieces_from_state()

        self.__played_states = {}
        self.__played_moves = []

        self.__bot_1 = AI(1)
        self.__bot_2 = AI(2)

        self.__bot_move_processing = False

    def __create_tiles(self):
        for row in range(5):
            for col in range(5):
                tile = Tile((col, row), self.__get_tile_position(col, row), self.__edge // 5, self.__tiles_color)
                self.__tiles.append(tile)

    def __get_tile_position(self, col, row):
        return self.__x * (col + 1), self.__y * (row + 1)

    def __insert_pieces_from_state(self):
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

    def get_player_turn(self):
        return self.__player_turn

    def get_opponent_turn(self):
        return 2 if self.__player_turn == 1 else 1

    def get_state(self):
        return self.__game_state

    def get_played_moves(self):
        return self.__played_moves

    def is_bot_move_processing(self):
        return self.__bot_move_processing

    def set_game_state(self, new_state):
        self.__game_state = new_state
        self.__insert_pieces_from_state()

    def __update_game_state(self):
        self.__game_state = [[0] * 5 for _ in range(5)]

        for tile in self.__tiles:
            self.__game_state[tile.get_coord_y()][tile.get_coord_x()] = tile.get_piece_player()

    def __change_turn(self):
        self.__player_turn = 2 if self.__player_turn == 1 else 1
        self.__board_menu.change_player_turn(self.__player_turn)

    def finish_piece_move(self):
        self.__store_current_position()
        self.__store_move(self.__move.get_coords())
        self.__move.finish()
        self.__change_turn()
        self.__update_game_state()

    def __apply_move(self, move):
        initial_x, initial_y, final_x, final_y = move

        for tile in self.__tiles:
            if tile.get_coords() == (initial_x, initial_y):
                self.__move.set_start_tile(tile)

            elif tile.get_coords() == (final_x, final_y):
                self.__move.set_dest_tile(tile)

        self.__move.start()

    def __move_is_valid(self):
        move = self.__move.get_coords()
        valid_moves = generate_all_moves(self.__game_state, self.__player_turn)

        return move in valid_moves

    def __is_draw(self):
        for val in self.__played_states.values():
            if val == 3:
                return True
        return False

    def is_game_over(self):

        if self.__is_draw():
            self.__board_menu.change_menu(config.BoardMenuState.GAME_OVER_DRAW_MENU)
            return True

        result = GameUtils.check_game_over_full(self.__game_state)

        if result == 1:
            self.__board_menu.change_menu(config.BoardMenuState.GAME_OVER_WINNER_MENU)
            self.__board_menu.set_winner(1)
            return True

        elif result == 2:
            self.__board_menu.change_menu(config.BoardMenuState.GAME_OVER_WINNER_MENU)
            self.__board_menu.set_winner(2)
            return True

        return False

    def check_game_over(self):
        if self.__is_draw():
            self.__state = config.BoardState.GAME_OVER_DRAW
            return

        result = GameUtils.check_game_over_full(self.__game_state)

        if result == 1:
            self.__state = config.BoardState.GAME_OVER_WINNER_1

        elif result == 2:
            self.__state = config.BoardState.GAME_OVER_WINNER_1

    def __store_current_position(self):
        item = GameUtils.full_game_to_tuple(self.__game_state)
        if item in self.__played_states.keys():
            self.__played_states[item] += 1
        else:
            self.__played_states[item] = 1

    def __store_move(self, move):
        self.__played_moves.append(move)

    def __start_move(self):
        self.__state = config.BoardState.PIECE_MOVING
        self.__move.start()

    def __finish_move(self):
        self.__state = config.BoardState.PLAYER_TURN
        self.__move.finish()

    def reset(self):
        self.__game_state = self.__initial_game_state

        self.__played_states.clear()
        self.__played_moves.clear()

        self.__state = config.BoardState.PLAYER_TURN
        self.__player_turn = 1

    def apply_bot_move(self, depth):
        self.__bot_move_processing = True
        self.__state = config.BoardState.BOT_PROCESSING
        if self.__player_turn == 1:
            assert(self.__player_turn == 1)
            assert(self.__player_turn == self.__bot_1.piece)
            score, move = self.__bot_1.minimax_alpha_beta_with_move_faster(True, self.__player_turn, self.__game_state, depth, AI.MIN, AI.MAX)
        else:
            assert (self.__player_turn == 2)
            assert (self.__player_turn == self.__bot_2.piece)
            score, move = self.__bot_2.minimax_alpha_beta_with_move_faster(True, self.__player_turn, self.__game_state, depth, AI.MIN, AI.MAX)

        print("Move: " + str(move) + " with a score of " + str(score) + " of player: " + str(self.__player_turn))
        self.__score_bar.update(self.__player_turn, score)
        self.__apply_move(move)
        self.__bot_move_processing = False
        self.__state = config.BoardState.PLAYER_TURN

    def press(self, mx, my):

        if not self.__move.is_start_tile_selected():
            for tile in self.__tiles:
                if tile.is_hover(mx, my):
                    self.__move.set_start_tile(tile)
                    break
            print("Start tile: {}".format(self.__move.get_start_tile().get_coords()))

        elif not self.__move.is_dest_tile_selected():
            for tile in self.__tiles:
                if tile.is_hover(mx, my):
                    self.__move.set_dest_tile(tile)
                    break
            print("Dest tile: {}".format(self.__move.get_dest_tile().get_coords()))

            if self.__move_is_valid():
                self.__move.start()
                # self.finish_piece_move()

            else:
                print("Invalid Move!")
                self.__move.reset()


