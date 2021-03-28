
from collections import deque
import re

# Class used to represent a node of the openings tree
class OpeningsNode:

    # Constructor
    def __init__(self, depth, move, parent):
        self.depth = depth
        self.move = move
        self.parent = parent
        self.children = []
        self.winner = 0

    # Adds a child to the current node
    def addChildNode(self, child):
        self.children.append(child)

# Class used to represent the openings tree
class OpeningsTree:

    # Constructor
    def __init__(self):
        self.root = OpeningsNode(0, (0, 0, 0, 0), None)
        self.res_list = []
        self.res_list_offset = 0
        self.count = 0

    # Helper function
    # Prints the tree using breadth-first search
    def bfsPrint(self):
        queue = deque()

        queue.append(self.root)

        while len(queue) != 0:
            node = queue.popleft()
            
            for child in node.children:
                queue.append(child)

            print("\t"*node.depth + " " + str(node.move))

    # Helper function
    # Prints the tree using depth-first search
    def dfsPrint(self):

        node = self.root

        self.dfsAuxPrint(node)

    # Helper function
    # Traverses the tree and prints each node's move
    def dfsAuxPrint(self, node):
        
        print("\t"*(node.depth-1) + " " + str(node.move) + " " + str(node.depth) + " " + str(node.winner))

        for child in node.children:
            self.dfsAuxPrint(child)

    # Helper function
    # Finds the move to be played next, based on the already played moves and the available opening lines
    def dfsFindMove(self, stored_moves, piece):
        node = self.root

        return self.dfsFindMoveAux(node, stored_moves, piece)

    # Helper function
    # Traverses the tree and returns a move that results in a win or draw to the player
    def dfsFindMoveAux(self, node, stored_moves, piece):

        move = None
        
        if (node.depth == len(stored_moves)):
            candidate_move = None
            for child in node.children:
                if child.winner == piece:
                    return child.move
                elif child.winner == 5 and candidate_move == 0:
                    candidate_move = child.move
            return candidate_move
        
        for child in node.children:
            if child.move != stored_moves[child.depth-1]:
                continue
            move = self.dfsFindMoveAux(child, stored_moves, piece)

        return move

    # Consumes an item of the res_list attribute (used twhen loading the openings)
    def consume_res_list_item(self):
        item = self.res_list[self.res_list_offset]
        self.res_list_offset += 1
        return item

    # Helper function
    # Counts the number of leaves in the tree using depth-first search
    def dfsCountLeaves(self):
        self.dfsCountLeavesAux(self.root)
        c = self.count
        self.count = 0
        return c

    # Helper function
    # Traverses the tree and counts the number of leaves
    def dfsCountLeavesAux(self, node):
        if len(node.children) == 0:
            self.count += 1
        for child in node.children:
            self.dfsCountLeavesAux(child)

    # For each node of tree, adds the game result of that line (1 if player 1 wins, 2 if player 2 wins, 5 if it results in a draw or in a win to any player)
    # Uses a dfs from bottom-up (postorder)
    def dfsAddWinner(self):

        node = self.root
        
        self.dfsAddWinnerAux(node)

    # Traverses the tree and adds the result of the opening line to all nodes
    def dfsAddWinnerAux(self, node):

        if len(node.children) == 0:
            res = self.consume_res_list_item()
            if res != 5:
                if node.depth % 2 == 0:
                    node.winner = 2
                else:
                    node.winner = 1
            else:
                node.winner = 5
            return node.winner
        else:
            winner = 0
            for child in node.children:
                winner |= self.dfsAddWinnerAux(child)
            if winner != 1 and winner != 2:
                winner = 5
            node.winner = winner
            return node.winner

# Class used to represent the openings book
class OpeningsBook:

    # Constructor
    def __init__(self):
        self.tree = OpeningsTree()

    # Translates a board position from the official notation ([a-e][1-5]) to the internal notation used by the program
    def translateMoveNotation(self, move_letters_notation):
        x = ord(move_letters_notation[0]) - 97
        y = 5 - int(move_letters_notation[1])
        return x, y

    # Translates a move from the official notation ([a-e][1-5]-[a-e][1-5]) to the internal notation used by the program
    def translateFullMove(self, move):
        move1 = move[:2]
        move2 = move[3:]
        translated_move_1 = self.translateMoveNotation(move1)
        translated_move_2 = self.translateMoveNotation(move2)
        return translated_move_1[0], translated_move_1[1], translated_move_2[0], translated_move_2[1]

    # Reads the next move from the openings text file
    def readNextMove(self, line, idx):
        i = 0
        while i < len(line[idx:]):
            if line[idx+i] == "<":
                i = i+3
                continue
            elif line[idx+i].isdigit():
                if line[idx+i+1].isdigit():
                    return line[idx+i+4:idx+i+4+5], int(line[idx+i:idx+i+2]), idx+i+4+5
                else:
                    return line[idx+i+3:idx+i+3+5], int(line[idx+i]), idx+i+3+5
            i += 1

    # Loads the openings from a text file
    def loadOpenings(self, filename):
        f = open(filename, "r")
            
        file_str = f.read()

        f.close()

        offset = 0

        possible_parents = [self.tree.root]

        while offset < len(file_str):
            res = self.readNextMove(file_str, offset)
            if res == None:
                break
            move_notation, move_depth, offset = res
            move = self.translateFullMove(move_notation)
            if move_depth < len(possible_parents)+1:
                possible_parents = possible_parents[:move_depth]
                parent = possible_parents[-1]
                child = OpeningsNode(move_depth, move, parent)
                parent.addChildNode(child)
                possible_parents.append(child)
        
        self.loadDrawsAndNumMovesToWin(file_str)

    # Loads each opening line's result from the text file
    def loadDrawsAndNumMovesToWin(self, openings_str):
        lines = openings_str.splitlines()
        res_list = []

        pattern1 = "DRAW"
        pattern2 = "<..>"

        for line in lines:
            if re.search(pattern1, line):
                res_list.append(5)
            elif re.search(pattern2, line):
                res_list.append(1)
        
        self.tree.res_list = res_list
        self.tree.dfsAddWinner()

    
    def find_next_move(self, stored_moves, piece):
        return self.tree.dfsFindMove(stored_moves, piece)
