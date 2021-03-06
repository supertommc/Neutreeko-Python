
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
    """
    def readNextMove(self, line, idx):
        for i, char in enumerate(line[idx:]):
            if char.isdigit():
                if line[idx+i+1].isdigit():
                    print(line[idx+i:idx+i+2])
                    if line[idx+i+2] == ">":
                        print("Ignoring")
                        continue
                    return line[idx+i+4:idx+i+4+5], int(line[idx+i:idx+i+2]), idx+i+4+5
                else:
                    print(line[idx+i:idx+i+1])
                    if line[idx+i+i] == ">":
                        print("Ignoring")
                        continue
                    return line[idx+i+3:idx+i+3+5], int(line[idx+i]), idx+i+3+5
    """
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
            

        

book = OpeningsBook()

book.loadOpenings("openings.txt")

book.tree.dfsPrint()