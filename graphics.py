from p5 import *

game =  [
            [0, 2, 0, 2, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 1, 0, 1, 0]
        ]

class Button:
    def __init__(self, position, width, height, color, text):
        self.x, self.y = position
        self.color = color
        self.width = width
        self.height = height
        self.text = text

    def display(self):
        offset = 0
        if self.is_hover():
            offset = 30
        fill(self.color[0]+offset, self.color[1]+offset, self.color[2]+offset)
        rect(self.x, self.y, self.width, self.height)
        fill(0, 0, 0)
        text(self.text, self.x + 40, self.y+self.height/2-1)

    def is_hover(self):
        return mouse_x > self.x and mouse_x < self.x + self.width and mouse_y > self.y and mouse_y < self.y + self.height

def draw_menu():
    button = Button((100, 100), 100, 50, (100, 100, 100), "Play")
    button.display()

def draw_board(game):
    # Vertical Lines
    line((100, 100), (100, 600))
    line((200, 100), (200, 600))
    line((300, 100), (300, 600))
    line((400, 100), (400, 600))
    line((500, 100), (500, 600))
    line((600, 100), (600, 600))

    # Horizontal Lines
    line((100, 100), (600, 100))
    line((100, 200), (600, 200))
    line((100, 300), (600, 300))
    line((100, 400), (600, 400))
    line((100, 500), (600, 500))
    line((100, 600), (600, 600))

    draw_state(game)

def draw_piece(piece, position):
    if (piece == 1):
        fill(0, 0, 0)
        circle(position, 50)
    elif piece == 2:
        fill(255, 255, 255)
        circle(position, 50)


def draw_state(game):
    for i in range(len(game)):
        for j in range(len(game[0])):
            if game[i][j] != 0:
                draw_piece(game[i][j], (550-j*100, 150+i*100))


def setup():
    size(700, 700)

def draw():
    draw_board(game)
    #draw_menu()


run()


