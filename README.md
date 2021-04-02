# Neutreeko

* [The Game](#the-game)
* [The Implementation](#the-implementation)
* [Installing And Running](#installation-and-running)
* [How To Play](#how-to-play)


## The Game
Neutreeko is a board game which resulted from a merge between two other board games, [Neutron](https://en.wikipedia.org/wiki/Neutron_(game)) and [Teeko](https://en.wikipedia.org/wiki/Teeko). <br>
The game is played on a 5x5 board and each player has three pieces. A piece can be moved by sliding orthogonally or diagonally until it hits something, like another piece or the edge of the board. In order to win, a player must have his three pieces in a row, all connected, either orthogonally or diagonally. FOr more information regarding the game and its rules, here's the [official website](https://www.neutreeko.net/neutreeko.htm).


## The Implementation
This project was developed for the Artificial Intelligence class of the Master in Informatics and Computing Engineering course of the Faculty of Engineering of the University of Porto.<br>
The project consists of an implementation of the board game [Neutreeko](#the-game) and some intelligent agents that can play the game.<br>

The agents were developed using the Minimax algorithm with alpha beta pruning and there is also an openings database implemented, containing some opening lines that have already been studied by humans. The project is implemented using the Python programming language.


## Installing And Running
To install the game, one needs to have the [pygame](https://www.pygame.org/news) library installed. To install it, simply run <pre>pip install pygame</pre> on a command line and you should be good to go. To make sure you can use the library, open your python interpreter and type <pre>import pygame</pre> If no errors occur, then everything is working properly.<br>

Running the game is equally simple, just open a terminal window and type <pre>python pygamegraphics.py</pre>
<br>

After this, you should see a new window popup and the game should now be running.

## How To Play
Our application has a very intuitive graphical interface. When you launch the application, you are presented with a menu containing some options, like playing the game (Player vs. Player, Player vs. Computer, etc.) and changing the game's options.<br>
On the options menu, you can change the depth and difficulty of each intelligent agent, which are named *bot1*, *bot2* and *hint*. You can also change the speed of the game and choose if the agents can use the openings database or not.<br>
If you choose to play the game, you will see the board and a couple of buttons. To make a move, simply click on one of your pieces and then click on the tile you wish to move it to. Be aware that if you make an illegal move, it won't be played and you will have to make another one. You can also offer a draw and resign the game using their respective buttons, and there is also the option of asking the computer for a hint, which will generate a line on the board indicating you the computer's suggestion.


We wish you enjoy our project. If you find any bug on the code or have any suggestion, please let us know.