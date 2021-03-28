from timeit import default_timer as timer
from game import Game
from ai import AI
from pprint import pprint
from gameUtils import GameUtils
from moveGenerator import generate_all_moves

game = Game()

ai = AI(1)
"""
print(ai.piece)
print(ai.other_piece)

GameUtils.unmake_move(game.state, (1, 4, 1, 1))
GameUtils.unmake_move(game.state, (3, 4, 4, 3))
GameUtils.unmake_move(game.state, (2, 3, 2, 2))
GameUtils.unmake_move(game.state, (0, 1, 1, 0))
GameUtils.unmake_move(game.state, (1, 0, 1, 4))

start = timer()
print("Minimax: " + str(ai.minimax_alpha_beta_with_move_faster(True, 1, game.state, 6, -9999999, 9999999)))
end = timer()
delta = end-start
pprint(game.state)
print("Time alpha beta: " + str(delta))
"""

print()
start = timer()
res = ai.minimax_alpha_beta_with_move_faster_order(True, 1, game.state, 6, -9999999, 9999999)
end = timer()
print("Minimax: " + str(res))
delta = end-start
pprint(game.state)
print("Time alpha beta faster: " + str(delta))
print("Num calls: " + str(ai.num_calls))

ai.num_calls = 0
"""
print()
start = timer()
res = ai.minimax_alpha_beta_with_move_faster(True, 1, game.state, 8, -9999999, 9999999)
end = timer()
print("Minimax: " + str(res))
delta = end-start
pprint(game.state)
print("Time alpha beta faster: " + str(delta))
print("Num calls: " + str(ai.num_calls))
"""
"""
print()
start = timer()
res = ai.minimax_with_move(True, 1, game.state, 6)
end = timer()
print("Minimax: " + str(res))
delta = end-start
pprint(game.state)
print("Time minimax: " + str(delta))
print("Num calls: " + str(ai.num_calls))
"""
#game = Game()
#game.game_loop()

"""
start = timer()

moves = ai.generate_all_moves_sort(game.state, 1, 6, True)

end = timer()
delta = end-start
print("Time: " + str(delta))
print(moves)

start = timer()

moves = generate_all_moves(game.state, 1)

end = timer()
delta = end-start
print("Time: " + str(delta))
print(moves)
"""

#game.game_loop()