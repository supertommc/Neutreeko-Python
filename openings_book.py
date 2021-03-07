
from collections import deque

class OpeningsNode:
    def __init__(self, depth, move, parent):
        self.depth = depth
        self.move = move
        self.parent = parent
        self.children = []

    def addChildNode(self, child):
        self.children.append(child)

class OpeningsTree:
    def __init__(self):
        self.root = OpeningsNode(0, (0, 0, 0, 0), None)

    def bfsAddChild(self, child_move, target_move, target_depth):
        queue = deque()

        queue.append(self.root)

        while len(queue) != 0:
            node = queue.popleft()
            
            for child in node.children:
                queue.append(child)

            if node.move == target_move and node.depth == target_depth:
                node.addChildNode(child_move)
        
    def bfsPrint(self):
        queue = deque()

        queue.append(self.root)

        while len(queue) != 0:
            node = queue.popleft()
            
            for child in node.children:
                queue.append(child)

            print("\t"*node.depth + " " + str(node.move))

    def dfsPrint(self):

        node = self.root

        self.dfsAuxPrint(node)

    def dfsAuxPrint(self, node):
        
        print("\t"*(node.depth-1) + " " + str(node.move))

        for child in node.children:
            self.dfsAuxPrint(child)

    def dfsFindMove(self, stored_moves):
        node = self.root

        return self.dfsFindMoveAux(node, stored_moves)

    def dfsFindMoveAux(self, node, stored_moves):

        move = 0

        print("Depth node: " + str(node.depth))
        print("Len stored moves: " + str(len(stored_moves)))

        if (node.depth == len(stored_moves)):
            print("OLAAA")
            print(node.move)
            return node.move
        
        for child in node.children:
            if child.move != stored_moves[child.depth-1]:
                continue
            move = self.dfsFindMoveAux(child, stored_moves)

        return move
        


class OpeningsBook:

    def __init__(self):
        self.tree = OpeningsTree()

    def translateMoveNotation(self, move_letters_notation):
        x = ord(move_letters_notation[0]) - 97
        y = 5 - int(move_letters_notation[1])
        return x, y

    def translateFullMove(self, move):
        move1 = move[:2]
        move2 = move[3:]
        translated_move_1 = self.translateMoveNotation(move1)
        translated_move_2 = self.translateMoveNotation(move2)
        return translated_move_1[0], translated_move_1[1], translated_move_2[0], translated_move_2[1]

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
    
    def find_next_move(self, stored_moves):
        return self.tree.dfsFindMove(stored_moves)

        

book = OpeningsBook()

book.loadOpenings("openings.txt")

print(book.find_next_move([(1, 4, 2, 4), (2, 3, 2, 2)]))