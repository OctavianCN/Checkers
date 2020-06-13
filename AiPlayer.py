import copy

from Player import Player
from math import inf as infinity
from collections import defaultdict
from State import State
class AiPlayer(Player):

    def __init__(self, color):
        if color == "white":
            color = "black"
        elif color == "black":
            color = "white"
        self.color = color
        super().__init__(color)

    def Move(self,game):
        i = 1
        turn = 'ai'
        stateList = []
        toIterate = []
        while i < game.depth:
            newStates = []
            if toIterate:
                for state in toIterate:
                    self.CreateStates(state.game,newStates,i,turn)
                    for newState in newStates:
                        newState.parent = state
            else:
                self.CreateStates(game,newStates,i,turn)
            if newStates:
                toIterate.clear()
                for state in newStates:
                    toIterate.append(state)
                    stateList.append(state)
            i = i + 1
            if turn == 'ai':
                turn = 'human'
            elif turn == 'human':
                turn = 'ai'
        for state in stateList:
            if state.depth == state.game.depth - 1:
                self.CalculateScore1(state)
                turn = "min"
                self.minimax(state,turn)
        maxState = None
        for state in stateList:
            if state.parent and state.score != None:
                newSt = state
                while newSt.parent:
                    newSt = copy.deepcopy(newSt.parent)
                if maxState != None:
                    if newSt.score > maxState.score:
                        maxState = copy.deepcopy(newSt)
                else:
                    maxState = copy.deepcopy(newSt)
        maxState.game.board.DrawBoard()
        return maxState.game

    def minimax(self,state,turn):
        if turn == "min":
            turn = "max"
        elif turn == "max":
            turn = "min"
        if state.parent:
            if turn == "max":
                if state.parent.score == None:
                    state.parent.score = -infinity
                if state.parent.score < state.score:
                    state.parent.score = state.score
            elif turn == "min":
                if state.parent.score == None:
                    state.parent.score = infinity
                if state.parent.score > state.score:
                    state.parent.score = state.score
            self.minimax(state.parent,turn)


    def CreateStates(self,game,stateList,i,turn):
        if turn == 'ai':
            whoMove = game.aiPlayer
            whoStay = game.humanPlayer
        elif turn == 'human':
            whoMove = game.humanPlayer
            whoStay = game.aiPlayer

        allPossibleMoves = defaultdict(list)
        takeEnemyCounter = defaultdict(list)
        for counter in whoMove.currentCounters:
            allPossibleMoves[counter].append(
                game.GetValidMoves(counter.positions[0], counter.positions[1], takeEnemyCounter, counter, whoMove,
                                   whoStay))

        for counter in whoMove.currentCounters:
            for possibleMoves in allPossibleMoves[counter]:
                for move in possibleMoves:
                    if move:
                        state = State(i, game)
                        if turn == 'ai':
                            stateWhoMove = state.game.aiPlayer
                            stateWhoStay = state.game.humanPlayer
                        elif turn == 'human':
                            stateWhoMove = state.game.humanPlayer
                            stateWhoStay = state.game.aiPlayer
                        state.MakeMove(counter.positions, move, takeEnemyCounter[move],stateWhoMove,stateWhoStay)
                        stateList.append(state)

    def CalculateScore(self,state):
        state.score = len(state.game.aiPlayer.currentCounters) - len(state.game.humanPlayer.currentCounters)
    def CalculateScore1(self,state):
        score = 0
        for counter in state.game.aiPlayer.currentCounters:
            if counter.isKing == True:
                score = score + 2
            else:
                score = score + 1
        for counter in state.game.aiPlayer.currentCounters:
            if counter.isKing == True:
                score = score - 2
            else:
                score = score - 1
        state.score = score

