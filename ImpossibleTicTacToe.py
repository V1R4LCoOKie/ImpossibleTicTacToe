import pygame, random

pygame.init()

NONE = -1
TIE = 0
P1 = 1
P2 = 2

X = 'X'
O = 'O'

assetDIR = "assets/"

Ximg = pygame.image.load(assetDIR + "X.png")
Xselectedimg = pygame.image.load(assetDIR + "Xselected.png")
Oimg = pygame.image.load(assetDIR + "O.png")
Oselectedimg = pygame.image.load(assetDIR + "Oselected.png")
Boardimg = pygame.image.load(assetDIR + "Board.png")
P1img = pygame.image.load(assetDIR + "P1deselected.png")
P1selectedimg = pygame.image.load(assetDIR + "P1selected.png")
P2img = pygame.image.load(assetDIR + "P2deselected.png")
P2selectedimg = pygame.image.load(assetDIR + "P2selected.png")
PlayButtonimg = pygame.image.load(assetDIR + "PlayButton.png")

ARIALFONT = pygame.font.SysFont("arial", 50)
SARIALFONT = pygame.font.SysFont("arial", 30)

EMPTY = 0

WAYSTOWIN = [[(0,0), (0,1), (0,2)], # ROW
             [(1,0), (1,1), (1,2)],
             [(2,0), (2,1), (2,2)],
             [(0,0), (1,0), (2,0)], # COLUMN
             [(0,1), (1,1), (2,1)],
             [(0,2), (1,2), (2,2)],
             [(0,0), (1,1), (2,2)], # DIAGONAL
             [(2,0), (1,1), (0,2)]]

SPECIALCASES1AVOID = [[[1,0,0], [0,2,0], [2,0,1]],
                      [[1,0,2], [0,2,0], [0,0,1]],
                      [[2,0,1], [0,2,0], [1,0,0]],
                      [[0,0,1], [0,2,0], [1,0,2]]]

SPECIALCASES2AVOID = [[[0,0,0], [0,1,0], [0,0,0]]]

SPECIALCASES2GET   = [[[1,0,0], [0,2,0], [0,0,1]],
                      [[0,0,1], [0,2,0], [1,0,0]]]

def main():

    winningOutcomes = generateOutcomes()
    
    numLosses = 0
    numDraws = 0

    window = pygame.display.set_mode((500,500))

    playerPref = (P1, Ximg, Oimg)

    while True:
        events = pygame.event.get()

        winText = SARIALFONT.render("WINS: 0", True, (255,255,255))
        loseText = SARIALFONT.render("LOSSES: " + str(numLosses), True, (255,255,255))
        drawText = SARIALFONT.render("TIES: " + str(numDraws), True, (255,255,255))

        window.fill((0,0,0))

        window.blit(winText, (10, 430))
        window.blit(loseText, (winText.get_width() + 20, 430))
        window.blit(drawText, (loseText.get_width() + winText.get_width() + 30, 430))
        pygame.display.update()

        playerPref = getPlayerPref(window, playerPref)

        window.fill((0,0,0))

        window.blit(winText, (10, 430))
        window.blit(loseText, (winText.get_width() + 20, 430))
        window.blit(drawText, (loseText.get_width() + winText.get_width() + 30, 430))
        pygame.display.update()

        result = playGame(window, winningOutcomes, playerPref[0], playerPref[1], playerPref[2])

        if result == TIE:
            numDraws += 1
        elif result == P1 or result == P2:
            numLosses += 1

        for e in events:
            if e.type == pygame.QUIT:
                return

def getPlayerPref(window, ogPref):

    text = ARIALFONT.render("Choose: ", True, (255,255,255))

    window.blit(text, (10,10))

    selectedPlayer = ogPref[0]
    selectedShape = ogPref[1]

    window.blit(P1selectedimg if selectedPlayer == P1 else P1img, (125,100))
    window.blit(P2selectedimg if selectedPlayer == P2 else P2img, (275,100))
    window.blit(Xselectedimg if selectedShape == Ximg else Ximg, (125,210))
    window.blit(Oselectedimg if selectedShape == Oimg else Oimg, (275,210))

    window.blit(PlayButtonimg, (175, 320))

    pygame.display.update()

    def within(pos, x, y, w, h):
        return pos[0] >= x and pos[0] < x + w and pos[1] >= y and pos[1] < y + h

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button != 1:
                    continue
                if within(e.pos, 175,320,150,70):
                    return (selectedPlayer, selectedShape, Ximg if selectedShape == Oimg else Oimg)
                elif within(e.pos, 125,100,100,100):
                    window.fill((0,0,0), rect=(125,100,250,100))
                    selectedPlayer = P1
                    window.blit(P1selectedimg, (125,100))
                    window.blit(P2img, (275,100))
                    pygame.display.update()
                elif within(e.pos, 275,100,100,100):
                    window.fill((0,0,0), rect=(125,100,250,100))
                    selectedPlayer = P2
                    window.blit(P1img, (125,100))
                    window.blit(P2selectedimg, (275,100))
                    pygame.display.update()
                elif within(e.pos, 125,210,100,100):
                    window.fill((0,0,0), rect=(125,210,250,100))
                    selectedShape = Ximg
                    window.blit(Xselectedimg, (125,210))
                    window.blit(Oimg, (275,210))
                    pygame.display.update()
                elif within(e.pos, 275,210,100,100):
                    window.fill((0,0,0), rect=(125,210,250,100))
                    selectedShape = Oimg
                    window.blit(Ximg, (125,210))
                    window.blit(Oselectedimg, (275,210))
                    pygame.display.update()



def playGame(window, winningOutcomes, playerNumber, playerimg, computerimg):
    
    window.blit(Boardimg, (95,100))

    playerTurn = True if playerNumber == P1 else False

    while True:
        if winningOutcomes.winner != NONE:
            break
        if playerTurn:
            pygame.draw.rect(window, (0,0,0), (0,0,500,100))
            text = ARIALFONT.render("It's your turn! Click a spot!", True, (255,255,255))
            window.blit(text, ((window.get_width() - text.get_width()) // 2, 20))
            pygame.display.update()

            while True:
                flag = False
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        quit()
                    elif e.type == pygame.MOUSEBUTTONDOWN:
                        if e.button == 1:
                            x = y = 0
                            if e.pos[0] >= 95 and e.pos[0] < 195:
                                x = 95
                            elif e.pos[0] >= 200 and e.pos[0] < 300:
                                x = 200
                            elif e.pos[0] >= 305 and e.pos[0] < 405:
                                x = 305
                            else:
                                continue

                            if e.pos[1] >= 100 and e.pos[1] < 200:
                                y = 100
                            elif e.pos[1] >= 205 and e.pos[1] < 305:
                                y = 205
                            elif e.pos[1] >= 310 and e.pos[1] < 410:
                                y = 310
                            else:
                                continue

                            if winningOutcomes.board[(x - 95) // 105][(y - 95) // 105] != EMPTY:
                                continue

                            window.blit(playerimg, (x, y))
                            for child in winningOutcomes.children:
                                if child.board[(x - 95) // 105][(y - 95) // 105] == playerNumber:
                                    winningOutcomes = child
                                    break
                            flag = True
                            break
                if flag:
                    playerTurn = False
                    break
        else:
            pygame.draw.rect(window, (0,0,0), (0,0,500,100))
            text = ARIALFONT.render("Thinking!", True, (255,255,255))
            window.blit(text, ((window.get_width() - text.get_width()) // 2, 20))
            pygame.display.update()
            pygame.time.delay(1500)

            defLose = []
            if playerNumber == P1:
                for child in winningOutcomes.children:
                    flag = False
                    for specialCase in SPECIALCASES1AVOID:
                        if child.board == specialCase:
                            flag = True
                            break
                    for child2 in child.children:
                        if child2.winner == P1:
                            flag = True
                            break
                    if flag:
                        defLose.append(child)
            elif playerNumber == P2:
                for child in winningOutcomes.children:
                    flag = False
                    for specialCase in SPECIALCASES2AVOID:
                        if child.board == specialCase:
                            flag = True
                            break
                    for child2 in child.children:
                        if child2.winner == P2:
                            flag = True
                            break
                    if flag:
                        defLose.append(child)

            minLoseChildren = []
            minLose = 0
            if playerNumber == P1:
                minLose = 1
                for child in winningOutcomes.children:
                    if child in defLose:
                        continue
                    if child.pathP1Wins / child.pathOutcomes == minLose:
                        minLoseChildren.append(child)
                    elif child.pathP1Wins / child.pathOutcomes < minLose:
                        minLose = child.pathP1Wins / child.pathOutcomes
                        minLoseChildren = [child]
            elif playerNumber == P2:
                minLose = 1
                for child in winningOutcomes.children:
                    if child in defLose:
                        continue
                    if child.pathP2Wins / child.pathOutcomes == minLose:
                        minLoseChildren.append(child)
                    elif child.pathP2Wins / child.pathOutcomes < minLose:
                        minLose = child.pathP2Wins / child.pathOutcomes
                        minLoseChildren = [child]

            newWinningOutcome = minLoseChildren[random.randint(0, len(minLoseChildren) - 1)]

            defWins = []
            if playerNumber == P1:
                for child in winningOutcomes.children:
                    flag = True
                    for child2 in child.children:
                        flag2 = False
                        for child3 in child2.children:
                            if child3.winner == P2:
                                flag2 = True
                                break
                        if not flag2:
                            flag = False
                            break
                    if flag:
                        defWins.append(child)
            elif playerNumber == P2:
                for child in winningOutcomes.children:
                    for specialCase in SPECIALCASES2GET:
                        if specialCase == child.board:
                            defWins.append(child)
                for child in winningOutcomes.children:
                    if len(defWins) > 0:
                        break
                    flag = True
                    for child2 in child.children:
                        flag2 = False
                        for child3 in child2.children:
                            if child3.winner == P1:
                                flag2 = True
                                break
                        if not flag2:
                            flag = False
                            break
                    if flag:
                        defWins.append(child)

            if len(defWins) > 0:
                newWinningOutcome = defWins[random.randint(0, len(defWins) - 1)]

            for x in range(3):
                for y in range(3):
                    if newWinningOutcome.board[x][y] != winningOutcomes.board[x][y]:
                        window.blit(computerimg, ((x * 105) + 95, (y * 105) + 95))
                        winningOutcomes = newWinningOutcome
                        break

            playerTurn = True

    pygame.draw.rect(window, (0,0,0), (0,0,500,100))
    text = ARIALFONT.render("You lose!" if winningOutcomes.winner != TIE else "A tie!", True, (255,255,255))
    window.blit(text, ((window.get_width() - text.get_width()) // 2, 20))

    pygame.display.update()
    pygame.time.delay(1500)

    return winningOutcomes.winner

def printBoard(board):
    for x in range(3):
        for y in range(3):
            if y != 2:
                print(" {} |".format(X if board[x][y] == P1 else O if board[x][y] == P2 else ' '), end="")
            else:
                print(" {}".format(X if board[x][y] == P1 else O if board[x][y] == P2 else ' '))
        if x != 2:
            print("___|___|___")

def generateOutcomes():

    class outcome:

        def __init__(self, board, numEmpty):
            self.winner = NONE
            self.board = [[board[x][y] for y in range(3)] for x in range(3)]
            self.numEmpty = numEmpty
            self.children = []
            self.pathOutcomes = 0
            self.pathP1Wins = 0
            self.pathP2Wins = 0
            self.pathTies = 0

        def checkWinner(self):
            for winPositions in WAYSTOWIN:
                x = winPositions[0]
                x = self.board[x[0]][x[1]]
                if x == EMPTY:
                    continue
                y = winPositions[1]
                y = self.board[y[0]][y[1]]
                if y != x:
                    continue
                z = winPositions[2]
                z = self.board[z[0]][z[1]]
                if z != x:
                    continue
                self.winner = x
                return x
            if self.numEmpty == 0:
                self.winner = TIE
                return TIE
            return NONE

    def generateOutcomesR(curOutcome, currentPlayer):
        w = curOutcome.checkWinner()
        if w != NONE:
            curOutcome.pathOutcomes = 1
            if w == P1:
                curOutcome.pathP1Wins = 1
            elif w == P2:
                curOutcome.pathP2Wins = 1
            else:
                curOutcome.pathTies = 1
            return curOutcome
        for x in range(3):
            for y in range(3):
                if curOutcome.board[x][y] != EMPTY:
                    continue
                newBoard = [[b for b in curOutcome.board[a]] for a in range(3)]
                newBoard[x][y] = currentPlayer
                curOutcome.children.append(generateOutcomesR(outcome(newBoard, curOutcome.numEmpty - 1), P1 if currentPlayer == P2 else P2))
        for o in curOutcome.children:
            curOutcome.pathOutcomes += o.pathOutcomes
            curOutcome.pathP1Wins += o.pathP1Wins
            curOutcome.pathP2Wins += o.pathP2Wins
            curOutcome.pathTies += o.pathTies
        return curOutcome

    print("Loading AI...")

    startingOutcome = outcome([[EMPTY for _ in range(3)] for _ in range(3)], 9)

    startingOutcome = generateOutcomesR(startingOutcome, P1)

    #print("POSSIBLE GAMES: " + str(startingOutcome.pathP1Wins+startingOutcome.pathP2Wins+startingOutcome.pathTies))
    #print("P1 WINS:        " + str(startingOutcome.pathP1Wins))
    #print("P2 WINS:        " + str(startingOutcome.pathP2Wins))
    #print("TIES:           " + str(startingOutcome.pathTies))
    return startingOutcome

main()