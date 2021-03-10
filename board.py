from moveGenerator import MoveGenerator
from pprint import pprint


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
        # TODO: self.__pressed_color = pressed_color
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
        self.__move_speed = 5.5

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
        # TODO: do finish condition
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


class Board:

    def __init__(self, state, neutreeko):
        self.__state = state
        self.__neutreeko = neutreeko

        self.__move = Move()

        self.__x = 100
        self.__y = 100
        self.__edge = 500

        self.__tiles = []
        self.__tiles_color = (255, 255, 255)

        self.__pieces_radius = 50
        self.__player_1_pieces_color = (255, 255, 255)
        self.__player_2_pieces_color = (0, 0, 0)

        self.__player_turn = 1

        self.__create_tiles()
        self.__insert_pieces_from_state()

    def __create_tiles(self):
        for row in range(5):
            for col in range(5):
                tile = Tile((col, row), self.__get_tile_position(col, row), self.__edge // 5, self.__tiles_color)
                self.__tiles.append(tile)

    def __get_tile_position(self, col, row):
        return self.__x * (col + 1), self.__y * (row + 1)

    def __insert_pieces_from_state(self):
        i = 0
        for row in range(len(self.__state)):
            for col in range(len(self.__state[0])):
                if self.__state[row][col] != 0:
                    piece = Piece((0, 0), self.__pieces_radius, self.__state[row][col],
                                  self.__get_piece_color(self.__state[row][col]))
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

    def get_player_turn(self):
        return self.__player_turn

    def get_opponent_turn(self):
        return 2 if self.__player_turn == 1 else 1

    def get_state(self):
        return self.__state

    def set_state(self, new_state):
        self.__state = new_state
        self.__insert_pieces_from_state()

    def __update_state(self):
        self.__state = [[0] * 5 for _ in range(5)]

        for tile in self.__tiles:
            self.__state[tile.get_coord_y()][tile.get_coord_x()] = tile.get_piece_player()

    def __change_turn(self):
        self.__player_turn = 2 if self.__player_turn == 1 else 1

    def finish_piece_move(self):
        self.__move.finish()
        self.__change_turn()
        self.__update_state()

    def apply_move(self, move):
        initial_x, initial_y, final_x, final_y = move

        for tile in self.__tiles:
            if tile.get_coords() == (initial_x, initial_y):
                self.__move.set_start_tile(tile)

            elif tile.get_coords() == (final_x, final_y):
                self.__move.set_dest_tile(tile)

        self.__move.start()
        # pprint(self.__state)

    def __move_is_valid(self):
        move = self.__move.get_coords()
        valid_moves = MoveGenerator.generate_all_moves(self.__state, self.__player_turn)

        return move in valid_moves

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
                pprint(self.__state)

            else:
                print("Invalid Move!")
                self.__move.reset()


