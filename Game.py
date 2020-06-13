import copy

from Board import Board
from HumanPlayer import HumanPlayer
from AiPlayer import AiPlayer
from collections import defaultdict
from Singleton import singleton



class Game:

    def __init__(self,algorithm,playerColor,dificulty):

        self.humanPlayer = HumanPlayer(playerColor)
        self.aiPlayer = AiPlayer(playerColor)
        if playerColor == "white":
            print("You are white")
            print("Enemy player is black")
            self.humanPlayer.lastRow = 7
            self.aiPlayer.lastRow = 0
        elif playerColor == "black":
            print("You are black")
            print("Enemy player is white")
            self.humanPlayer.lastRow = 0
            self.aiPlayer.lastRow = 7
        if dificulty == "low":
            self.depth = 2
        elif dificulty == "medium":
            self.depth = 4
        elif dificulty == "hard":
            self.depth = 6

        self.board = Board()
        self.gameWinner = None
        for counter in self.aiPlayer.currentCounters:
            self.board.PutCounterOnBoardInPosition(counter.positions[0], counter.positions[1], counter.character)
        for counter in self.humanPlayer.currentCounters:
            self.board.PutCounterOnBoardInPosition(counter.positions[0],counter.positions[1],counter.character)
        self._restart = False

    def StartGame(self):
        print("The game starts")
        while self.gameWinner == None:
            self.board.DrawBoard()
            playerValidMove = False
            while playerValidMove == False:
                try:
                    oldPositionX,oldPositionY,positionX,positionY = self.humanPlayer.Move()
                    playerValidMove = self.CheckValidMove(oldPositionX,oldPositionY,positionX,positionY,self.humanPlayer)
                    if playerValidMove == True:
                        self.board.ChangeCounterPosition(oldPositionX,oldPositionY,positionX,positionY,self.humanPlayer.GetCounterFromPosition(oldPositionX,oldPositionY).character)
                        self.humanPlayer.GetCounterFromPosition(oldPositionX, oldPositionY).positions = (positionX,positionY)
                        self.board.DrawBoard()
                    else:
                        raise Exception()
                except:
                    print("\nNu poti sa faci o astfel de mutare! \n")
                    playerValidMove = False
            for counter in self.humanPlayer.currentCounters:
                if counter.positions[0] == self.humanPlayer.lastRow:
                    counter.isKing = True
            if self.CheckWinner():
                print(self.gameWinner)
                break
            self = copy.deepcopy(self.aiPlayer.Move(self))
            for counter in self.aiPlayer.currentCounters:
                if counter.positions[0] == self.aiPlayer.lastRow:
                    counter.isKing = True
            self.board.DrawBoard()
            if self.CheckWinner():
                print(self.gameWinner)
                break

        self._Restart()
    def CheckWinner(self):
        if self.aiPlayer.currentCounters == 0:
            self.gameWinner = "Human won"
            return True
        elif self.humanPlayer.currentCounters == 0:
            self.gameWinner == "Ai won"
            return True
        return False
    def _Restart(self):
        restart = input("Do you want to restart the game [yes/no]?")
        if restart.lower() == "yes":
            self._restart = True
            self.gameWinner = None
        elif restart.lower() == "no":
            self._restart = False

    def GetValidMoves(self,oldPositionX,oldPositionY,takeEnemyCounter,currentPlayerCounter,whoMove,enemy):
        try:
            validPositions = self.ValidPositions(oldPositionX,oldPositionY,currentPlayerCounter,whoMove)
            listOfRemoveFromValidPositions = []
            for posX,posY in validPositions:
                if posX < 0 or posX > 7 or posY < 0 or posY > 7:
                    listOfRemoveFromValidPositions.append((posX,posY))
                    continue
                if whoMove.HaveCounterOnPosition(posX,posY):
                    listOfRemoveFromValidPositions.append((posX, posY))
                    continue
                enemyHaveCounterOnPosition = enemy.HaveCounterOnPosition(posX,posY)
                if enemyHaveCounterOnPosition == True:
                    potentialPosition = self.CheckPotentialPositions(posX,posY,oldPositionX,oldPositionY,currentPlayerCounter,whoMove)
                    if enemy.HaveCounterOnPosition(potentialPosition[0],potentialPosition[1]) == False:
                        validPositions.append(potentialPosition)
                        takeEnemyCounter[potentialPosition].append(enemy.GetCounterFromPosition(posX,posY))
                        oldPotentialPosX = potentialPosition[0]
                        oldPotentialPosY = potentialPosition[1]
                        self.CheckMoreMoves(oldPotentialPosX,oldPotentialPosY,currentPlayerCounter,validPositions,takeEnemyCounter,whoMove,enemy)
                        #potentialMoreMove.append(potentialPosition) #aici tin positiile in care capturez si pot sa am posibilitatea sa capturez mai multe
                    listOfRemoveFromValidPositions.append((posX,posY))
                    continue

            for position in listOfRemoveFromValidPositions:
                validPositions.remove(position)

            #print(len(validPositions))
            #for posX,posY in validPositions:
             #   try:
              #      print(posX,posY,takeEnemyCounter[(posX,posY)][0].character)
               #     print("-----------------")
               # except:
                #    print(posX,posY)
                 #   print("-----------------")
            return validPositions
        except:
            return None
    def CheckValidMove(self,oldPositionX,oldPositionY,positionX,positionY,whoMove):
        playerCounter = whoMove.GetCounterFromPosition(oldPositionX, oldPositionY)
        if whoMove == self.humanPlayer:
            enemy = self.aiPlayer
        elif whoMove == self.aiPlayer:
            enemy = self.humanPlayer
        if playerCounter.isDead == True:
            return False
        if positionX == oldPositionX and positionY == oldPositionY:
            return False
        takeEnemyCounter = defaultdict(list)
        validPositions = self.GetValidMoves(oldPositionX,oldPositionY,takeEnemyCounter,playerCounter,whoMove,enemy)
        print(validPositions)
        if validPositions != None:
            for posX, posY in validPositions:  # verific daca positia aleasa este o pozitie valida
                if positionX == posX and positionY == posY:
                    try:
                        for elim in takeEnemyCounter[(posX, posY)]:
                            self.board.ElimFromBoard(elim.positions[0], elim.positions[1])
                            enemy.currentCounters.remove(elim)
                    except:
                        pass
                    return True
        return False
    def CheckMoreMoves(self,oldPotentialPosX,oldPotentialPosY,playerCounter,validPositions,takeEnemyCounter,whoMove,enemy):
        newValidPositions = self.ValidPositions(oldPotentialPosX, oldPotentialPosY, playerCounter,whoMove)
        for pX, pY in newValidPositions:
            aiHCOnPos = enemy.HaveCounterOnPosition(pX, pY) #enemy Have counter on position
            if aiHCOnPos == True:
                potentialPositionsOfPotentialPositions = self.CheckPotentialPositions(pX, pY, oldPotentialPosX,
                                                                                          oldPotentialPosY,
                                                                                          playerCounter,whoMove)
                if enemy.HaveCounterOnPosition(potentialPositionsOfPotentialPositions[0],
                                                           potentialPositionsOfPotentialPositions[1]) == False \
                        and potentialPositionsOfPotentialPositions[0] >= 0 and potentialPositionsOfPotentialPositions[0] <= 7\
                        and potentialPositionsOfPotentialPositions[1] >= 0 and potentialPositionsOfPotentialPositions[1] <= 7:
                    posList = []
                    posList.append(potentialPositionsOfPotentialPositions)
                    validPositions.append(potentialPositionsOfPotentialPositions)
                    enemyTake = []
                    enemyTake.append(enemy.GetCounterFromPosition(pX, pY))
                    for enemyc in takeEnemyCounter[(oldPotentialPosX, oldPotentialPosY)]:
                        enemyTake.append(enemyc)
                    for enemyc in enemyTake:
                        takeEnemyCounter[potentialPositionsOfPotentialPositions].append(enemyc)
                        #takeEnemyCounter[potentialPositionsOfPotentialPositions].append(enemy)
                    return self.CheckMoreMoves(potentialPositionsOfPotentialPositions[0],potentialPositionsOfPotentialPositions[1],playerCounter,validPositions,takeEnemyCounter,whoMove,enemy)


    def ValidPositions(self,oldPositionX,oldPositionY,playerCounter,whoMove):
        validPositions = []
        if playerCounter.isKing == True:
            validPositions = [(oldPositionX + 1, oldPositionY + 1), (oldPositionX + 1, oldPositionY - 1),
                              (oldPositionX - 1, oldPositionY + 1), (oldPositionX - 1, oldPositionY - 1)]
        else:
            if whoMove.color == "white":
                validPositions = [(oldPositionX + 1, oldPositionY + 1), (oldPositionX + 1, oldPositionY - 1)]
            elif whoMove.color == "black":
                validPositions = [(oldPositionX - 1, oldPositionY + 1), (oldPositionX - 1, oldPositionY - 1)]
        return validPositions
    def CheckPotentialPositions(self,posX,posY,oldPositionX,oldPositionY,playerCounter,whoMove):
        if playerCounter.isKing == True:  # verific daca pot sa capturez un jeton
            if posX > oldPositionX:
                if posY > oldPositionY:
                    potentialPosition = (posX + 1,
                                         posY + 1)  # daca tinde sa se mute pe o pozitie in care creste x ul si y ul atunci e posibil sa se mute pe acea diagonala
                elif posY < oldPositionY:
                    potentialPosition = (posX + 1, posY - 1)
            elif posX < oldPositionX:
                if posY > oldPositionY:
                    potentialPosition = (posX - 1, posY + 1)
                elif posY < oldPositionY:
                    potentialPosition = (posX - 1, posY - 1)
        else:
            if whoMove.color == "white":
                if posY > oldPositionY:
                    potentialPosition = (posX + 1, posY + 1)
                elif posY < oldPositionY:
                    potentialPosition = (posX + 1, posY - 1)
            elif whoMove.color == "black":
                if posY > oldPositionY:
                    potentialPosition = (posX - 1, posY + 1)
                elif posY < oldPositionY:
                    potentialPosition = (posX - 1, posY - 1)
        return potentialPosition

