# Suggestions for speeding up the program are welcome!

class Move:
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    z1 = 0
    prev = None

def readint(question):
    done = False
    while not done:
        try:
            s2 = int(input(question))
            done = True
        except ValueError:
            print("Illegal format! Enter an integer")
    return(s2)

print("\nNeutreeko (c) 2001, 2002 J K Haugland")
print("\nEnter 0 for standard Neutreeko")
print("\nOtherwise, enter board size:")
b1 = 0
b2 = 0
b6 = 0
while b1 < 3 or b1 > 7:
    b1 = readint("Width = ")
    if b1 == 0:
        b1 = 5
        b2 = 5
        b6 = 1
        print("\nWidth = 5")
        print("Height = 5")
        print("Winning condition: three in a row, orthogonally or diagonally")
    if b1 < 3:
        print("Too narrow")
    if b1 > 7:
        print("Too wide")
while b2 < 3 or b2 > 7:
    b2 = readint("Height = ")
    if b2 < 3:
        print("Too low")
    if b2 > 7:
        print("Too high")
if b6 == 0:
    print("")
while b6 < 1 or b6 > 5 or (b6 == 3 and (b1 == 3 or b2 == 3)) or (b6 == 4 and b1 < 5 and b2 < 5) or (b6 == 5 and (b1 % 2 == 0 or b2 % 2 == 0 or b1 * b2 < 25)):
    print("Enter winning condition:")
    print("1 = three in a row, orthogonally or diagonally")
    print("2 = three in a row, orthogonally")
    if b1 > 3 and b2 > 3:
        print("3 = three in a row, diagonally") # width or height = 3 would make it possible to be trapped with no legal moves
    if b1 > 4 or b2 > 4:
        print("4 = three in a straight line, any equidistant") # either width or height must be greater than 3 to make this distinct from no. 1
    if (b1 == 5 or b1 == 7) and (b2 == 5 or b2 == 7):
        print("5 = occupy the centre") # only possible when width and height are odd - also cf. no. 3
    b6 = readint("")
if b1 == b2:
    b5 = 8
else:
    b5 = 4
b3 = b1 * b2
b4 = (b3 * (b3 - 1) * (b3 - 2)) // 6
print("\nCounting positions...")
drawPosition = 500 # just a code; should be set higher than the maximal depth
illegalPosition = 600 # also just a code
s = [[[0 for x in range(b3)] for y in range(b3)] for z in range(b3)]
t = [[0 for x in range(4)] for y in range(b4)]
u = [[[0 for x in range(b2)] for y in range(b1)] for z in range(b4)]
v = [0 for x in range(b4)]
w = [[0 for x in range(b2)] for y in range(b1)]
x3 = [[drawPosition for x in range(b4)] for y in range(b4)]
y3 = [[0 for x in range(6)] for y in range(25)]
p = [0 for x in range(25)]
q = [[0 for x in range(b5)] for y in range(b3)]
piece = ["o", " ", "x"]
letter = ["A", "B", "C", "D", "E", "F", "G"]
choice = ["" for x in range(25)]
for a in range(b3):
    b = a % b1
    c = a // b1
    q[a][0] = a
    q[a][1] = (b1 - 1 - b) + b1 * c
    q[a][2] = b + b1 * (b2 - 1 - c)
    q[a][3] = (b1 - 1 - b) + b1 * (b2 - 1 - c)
    if b5 == 8:
        q[a][4] = c + b1 * b
        q[a][5] = (b1 - 1 - c) + b1 * b
        q[a][6] = c + b1 * (b1 - 1 - b)
        q[a][7] = (b1 - 1 - c) + b1 * (b1 - 1 - b)
d = -1
for a in range(b3 - 2):
    for b in range(a + 1, b3 - 1):
        for c in range(b + 1, b3):
            d += 1
            for e in range(b1):
                for f in range(b2):
                    u[d][e][f] = 0
            u[d][a % b1][a // b1] = 1
            u[d][b % b1][b // b1] = 1
            u[d][c % b1][c // b1] = 1
            v[d] = 0
            if b6 == 5:
                if a == (b3 - 1) // 2 or b == (b3 - 1) // 2 or c == (b3 - 1) // 2:
                    v[d] = 1
            else:
                if (a % b1) + (c % b1) == 2 * (b % b1) and (a // b1) + (c // b1) == 2 * (b // b1):
                    if (a % b1) - (c % b1) <= 2 and (c % b1) - (a % b1) <= 2 and (a // b1) - (c // b1) <= 2 and (c // b1) - (a // b1) <= 2:
                        v[d] = 1
                if b6 == 2 and (a % b1) != (c % b1) and (a // b1) != (c // b1):
                    v[d] = 0
                if b6 == 3 and ((a % b1) == (c % b1) or (a // b1) == (c // b1)):
                    v[d] = 0
                if (a % b1) + (c % b1) == 2 * (b % b1) and (a // b1) + (c // b1) == 2 * (b // b1) and b6 == 4:
                    v[d] = 1
            s[a][b][c] = d
            s[a][c][b] = d
            s[b][a][c] = d
            s[b][c][a] = d
            s[c][a][b] = d
            s[c][b][a] = d
            t[d][0] = a
            t[d][1] = b
            t[d][2] = c
            t[d][3] = 2
for a in range(b4):
    for b in range(1, b5):
        if t[a][3] == 1:
            t[a][3] = 2
        c = 0
        while c < b3 and t[a][3] == 2:
            if u[a][c % b1][c // b1] != u[a][q[c][b] % b1][q[c][b] // b1]:
                if u[a][c % b1][c // b1] == 1:
                    t[a][3] = 1
                else:
                    t[a][3] = 0
            c += 1
        if t[a][3] == 2:
            t[a][3] = 1
j = 0
for a in range(b4):
    for b in range(b4):
        if v[b] == 1:
            x3[a][b] = 0
        if v[a] == 1:
            x3[a][b] = illegalPosition
        if u[a][t[b][0] % b1][t[b][0] // b1] == 1 or u[a][t[b][1] % b1][t[b][1] // b1] == 1 or u[a][t[b][2] % b1][t[b][2] // b1] == 1:
            x3[a][b] = illegalPosition
        if x3[a][b] == 0:
            j += 1
            if (j % 100000 == 0):
                print("-", end = "")
print("0 ", j)
c = 1
while j > 0:
    j = 0
    for a in range(b4):
        if t[a][3] == 1:
            for b in range(b4):
                if x3[a][b] == drawPosition:
                    stopped = False
                    for k in range(3):
                        d = t[a][k] % b1
                        e = t[a][k] // b1
                        for f in range(-1, 2):
                            for g in range(-1, 2):
                                if f * f + g * g > 0 and d + f >= 0 and d + f < b1 and e + g >= 0 and e + g < b2 and u[a][d + f][e + g] == 0 and u[b][d + f][e + g] == 0 and not stopped:
                                    f1 = f
                                    g1 = g
                                    while d + f1 + f >= 0 and d + f1 + f < b1 and e + g1 + g >= 0 and e + g1 + g < b2 and u[a][d + f1 + f][e + g1 + g] == 0 and u[b][d + f1 + f][e + g1 + g] == 0:
                                        f1 += f
                                        g1 += g
                                    for h in range(3):
                                        p[h] = t[a][h]
                                    p[k] = d + f1 + b1 * (e + g1)
                                    h = s[p[0]][p[1]][p[2]]
                                    if c % 2 == 0:
                                        if x3[b][h] < c:
                                            x3[a][b] = c
                                        else:
                                            x3[a][b] = drawPosition
                                            stopped = True
                                    else:
                                        if x3[b][h] == c - 1:
                                            x3[a][b] = c
                                            stopped = True
                    if x3[a][b] == c:
                        j += 1
                        if j % 100000 == 0:
                            print("-", end = "")
                        for d in range(1, b5):
                            e = s[q[t[a][0]][d]][q[t[a][1]][d]][q[t[a][2]][d]]
                            f = s[q[t[b][0]][d]][q[t[b][1]][d]][q[t[b][2]][d]]
                            if x3[e][f] != c:
                                x3[e][f] = c
                                j += 1
                                if j % 100000 == 0:
                                    print("-", end = "")
    print(str(c) + "  " + str(j))
    c += 1
for a in range(b4):
    for b in range(b4):
        if x3[a][b] == drawPosition:
            j += 1
print("\nNumber of draws:", j)
print("\nDeepest position(s):")
for a in range(b4):
    if t[a][3] == 1:
        for b in range(b4):
            if x3[a][b] == c - 2:
                pos1 = "x -"
                for d in range(3):
                    pos1 += " " + letter[t[a][d] % b1] + str(1 + t[a][d] // b1)
                pos1 += "   o -"
                for d in range(3):
                    pos1 += " " + letter[t[b][d] % b1] + str(1 + t[b][d] // b1)
                print(pos1)
if (b1 == 5 or b1 == 7) and b2 == b1 and (b6 == 1 or b6 == 5):
    if b6 == 1:
        a = s[(b1 - 3) // 2][(b1 + 1) // 2][(b3 - 1) // 2 + b1]
        b = s[(b3 - 1) // 2 - b1][b3 - (b1 + 3) // 2][b3 - (b1 - 1) // 2]
    else:
        a = s[(b3 - 1) // 2 - 2 * b1][(b3 - 1) // 2 + b1 - 2][(b3 - 1) // 2 + b1 + 2]
        b = s[(b3 - 1) // 2 - b1 - 2][(b3 - 1) // 2 - b1 + 2][(b3 - 1) // 2 + 2 * b1]
else:
    print("\n(This may not be a suitable opening position)")
    a = s[0][2][b3 - 2]
    b = s[1][b3 - 3][b3 - 1]
for c in range(b1):
    for d in range(b2):
        w[c][d] = u[a][c][d] - u[b][c][d]
mv = Move()
stripe = "\n +"
for c in range(b1):
    stripe += "---+"
while x3[a][b] > 0:
    print(stripe)
    for d in range(b2):
        pos1 = str(b2 - d) + "|"
        for c in range(b1):
            pos1 += " " + piece[1 + w[c][b2 - 1 - d]] + " |"
        print(pos1 + stripe)
    pos1 = ""
    for c in range(b1):
        pos1 += "   " + letter[c]
    print(pos1 + "\n")
    j = 0
    if x3[a][b] == illegalPosition:
        print("Illegal position")
    else:
        for k in range(3):
            d = t[a][k] % b1
            e = t[a][k] // b1
            for f in range(-1, 2):
                for g in range(-1, 2):
                    if f * f + g * g > 0 and d + f >= 0 and d + f < b1 and e + g >= 0 and e + g < b2 and w[d + f][e + g] == 0:
                        f1 = f
                        g1 = g
                        while d + f1 + f >= 0 and d + f1 + f < b1 and e + g1 + g >= 0 and e + g1 + g < b2 and w[d + f1 + f][e + g1 + g] == 0:
                            f1 += f
                            g1 += g
                        for h in range(3):
                            p[h] = t[a][h]
                        p[k] = d + f1 + b1 * (e + g1)
                        h = s[p[0]][p[1]][p[2]]
                        j += 1
                        choice[j] = ". " + letter[d] + str(e + 1) + " -> " + letter[d + f1] + str(e + g1 + 1) + " : "
                        if x3[b][h] == drawPosition:
                            choice[j] += "Draw"
                        else:
                            if x3[b][h] % 2 == 0:
                                choice[j] += "Win"
                            else:
                                choice[j] += "Loss"
                            if x3[b][h] > 0:
                                choice[j] += " in " + str(x3[b][h] + 1) + " moves"
                        y3[j][0] = d
                        y3[j][1] = e
                        y3[j][2] = d + f1
                        y3[j][3] = e + g1
                        y3[j][4] = h
                        y3[j][5] = x3[b][h]
                        if y3[j][5] % 2 == 0:
                            y3[j][5] -= drawPosition
                        else:
                            y3[j][5] = drawPosition - y3[j][5]
    for c in range(1, j + 1):
        p[c] = c
    for c in range(1, j):
        for d in range(c + 1, j + 1):
            if y3[p[c]][5] > y3[p[d]][5]:
                e = p[c]
                p[c] = p[d]
                p[d] = e
    for c in range(1, j + 1):
        print(str(c) + choice[p[c]])
    if mv.prev != None:
        print("77. Retract last move")
    if (b1 == 5 or b1 == 7) and b2 == b1 and (b6 == 1 or b6 == 5):
        print("88. Back to start")
    print("99. Enter new position")
    d = 98
    while d != 99 and (d < 1 or d > j) and (d != 88 or (b1 != 5 and b1 != 7) or b2 != b1 or (b6 != 1 and b6 != 5)) and (d != 77 or mv.prev == None):
        d = readint("Enter alternative: ")
    if d == 77:
        b = a
        a = mv.z1
        for c in range(b1):
            for d in range(b2):
                w[c][d] = -w[c][d]
        piece[1] = piece[0]
        piece[0] = piece[2]
        piece[2] = piece[1]
        piece[1] = " "
        w[mv.x1][mv.y1] = 1
        w[mv.x2][mv.y2] = 0
        mv = mv.prev
    else:
        if d == 88:
            if b6 == 1:
                a = s[(b1 - 3) // 2][(b1 + 1) // 2][(b3 - 1) // 2 + b1]
                b = s[(b3 - 1) // 2 - b1][b3 - (b1 + 3) // 2][b3 - (b1 - 1) // 2]
            else:
                a = s[(b3 - 1) // 2 - 2 * b1][(b3 - 1) // 2 + b1 - 2][(b3 - 1) // 2 + b1 + 2]
                b = s[(b3 - 1) // 2 - b1 - 2][(b3 - 1) // 2 - b1 + 2][(b3 - 1) // 2 + 2 * b1]
            for c in range(b1):
                for d in range(b2):
                    w[c][d] = u[a][c][d] - u[b][c][d]
            piece[0] = "o"
            piece[1] = " "
            piece[2] = "x"
            mv = Move()
        else:
            if d == 99:
                h1 = 0
                h2 = 0
                h3 = 0
                while h1 != b3 - 6 or h2 != 3 or h3 != 3:
                    print("Enter one "+ str(b1) + "-digit number for each row")
                    print("0 = blank; 1 = 'x' (plays first); 2 = 'o'")
                    print("(The input is read as an integer, and starting zeros can be omitted)")
                    for e in range(b1):
                        for f in range(b2):
                            w[e][f] = 0
                    for e in range(b2):
                        f = readint("")
                        for g in range(b1):
                            w[b1 - 1 - g][b2 - 1 - e] = f % 10
                            f = f // 10
                        for f in range(b1):
                            if w[f][b2 - 1 - e] == 2:
                                w[f][b2 - 1 - e] = -1
                    h1 = 0
                    h2 = 0
                    h3 = 0
                    for e in range(b1):
                        for f in range(b2):
                            if w[e][f] == 0:
                                h1 += 1
                            if w[e][f] == 1:
                                h2 += 1
                            if w[e][f] == -1:
                                h3 += 1
                    if h1 != b3 - 6:
                        print("Error: " + str(h1) + " blanks (should be " + str(b3 - 6) + ")")
                    if h2 != 3:
                        print("Error: " + str(h2) + " x's (should be 3)")
                    if h3 != 3:
                        print("Error: " + str(h3) + " o's (should be 3)")
                h1 = 0
                while w[h1 % b1][h1 // b1] <= 0:
                    h1 += 1
                h2 = h1 + 1
                while w[h2 % b1][h2 // b1] <= 0:
                    h2 += 1
                h3 = h2 + 1
                while w[h3 % b1][h3 // b1] <= 0:
                    h3 += 1
                a = s[h1][h2][h3]
                h1 = 0
                while w[h1 % b1][h1 // b1] >= 0:
                    h1 += 1
                h2 = h1 + 1
                while w[h2 % b1][h2 // b1] >= 0:
                    h2 += 1
                h3 = h2 + 1
                while w[h3 % b1][h3 // b1] >= 0:
                    h3 += 1
                b = s[h1][h2][h3]
                piece[0] = "o"
                piece[1] = " "
                piece[2] = "x"
                mv = Move()
            else:
                c = p[d]
                mv2 = Move()
                mv2 = mv
                mv = Move()
                mv.prev = mv2
                mv.x1 = y3[c][0]
                mv.y1 = y3[c][1]
                mv.x2 = y3[c][2]
                mv.y2 = y3[c][3]
                mv.z1 = a
                a = b
                b = y3[c][4]
                w[y3[c][0]][y3[c][1]] = 0
                w[y3[c][2]][y3[c][3]] = 1
                for c in range(b1):
                    for d in range(b2):
                        w[c][d] = -w[c][d]
                piece[1] = piece[0]
                piece[0] = piece[2]
                piece[2] = piece[1]
                piece[1] = " "
print(stripe)
for d in range(b2):
    pos1 = str(b2 - d) + "|"
    for c in range(b1):
        pos1 += " " + piece[1 + w[c][b2 - 1 - d]] + " |"
    print(pos1 + stripe)
pos1 = ""
for c in range(b1):
    pos1 += "   " + letter[c]
print(pos1 + "\n\nGAME OVER\n")