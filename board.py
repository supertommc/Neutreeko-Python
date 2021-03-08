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

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

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

    def set_piece(self, new_piece):
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


class Board:

    def __init__(self, state):
        self.__state = state

        self.__start_tile = None
        self.__dest_tile = None

        self.__x = 100
        self.__y = 100
        self.__edge = 500

        self.__tiles = []
        self.__tiles_color = (255, 255, 255)

        self.__pieces_radius = 50
        self.__player_1_pieces_color = (255, 255, 255)
        self.__player_2_pieces_color = (0, 0, 0)

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
                    piece = Piece(self.__get_piece_position(row, col), self.__pieces_radius, self.__state[row][col],
                                  self.__get_piece_color(self.__state[row][col]))
                    self.__tiles[i].set_piece(piece)
                i += 1

    @staticmethod
    def __get_piece_position(row, col):
        return 550 - col * 100, 150 + row * 100

    def __get_piece_color(self, player):
        if player == 1:
            return self.__player_1_pieces_color
        elif player == 2:
            return self.__player_2_pieces_color
        return None

    def get_tiles(self):
        return self.__tiles

    def set_state(self, new_state):
        self.__state = new_state
        self.__insert_pieces_from_state()

    def press(self, mx, my):

        if self.__start_tile is None:
            for tile in self.__tiles:
                if tile.is_hover(mx, my):
                    self.__start_tile = tile
                    break

            print("Start tile: {}".format(self.__start_tile.get_coords()))
            self.__dest_tile = None

        elif self.__dest_tile is None:
            for tile in self.__tiles:
                if tile.is_hover(mx, my):
                    self.__dest_tile = tile
                    break

            print("Dest tile: {}".format(self.__dest_tile.get_coords()))

            piece = self.__start_tile.get_piece()

            self.__dest_tile.set_piece(piece)

            self.__start_tile = None
            self.__dest_tile = None
