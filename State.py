import copy


class State:

    def __init__(self,depth,game,parent = None, score = None):
        self.game = copy.deepcopy(game)
        self.depth = depth
        self.parent = parent
        self.score = score
    def MakeMove(self,oldPos,newPos,enemyTake,whoMove,whoStay):
        whoMove.GetCounterFromPosition(oldPos[0],oldPos[1]).positions = newPos
        for take in enemyTake:
            if whoStay.HaveCounterOnPosition(take.positions[0],take.positions[1]):
                whoStay.GetCounterFromPosition(take.positions[0],take.positions[1]).isDead = True
                self.game.board.ElimFromBoard(take.positions[0],take.positions[1])  # fac tot ceea ce s-ar face daca ar exista o astfel de miscare
                for counter in whoStay.currentCounters:
                    if counter.positions == take.positions:
                        whoStay.currentCounters.remove(counter)

        self.game.board.Clear()
        for counter in self.game.aiPlayer.currentCounters:
            self.game.board.PutCounterOnBoardInPosition(counter.positions[0],counter.positions[1],counter.character)
        for counter in self.game.humanPlayer.currentCounters:
            self.game.board.PutCounterOnBoardInPosition(counter.positions[0], counter.positions[1],
                                                            counter.character)

       # print(self.enemy.currentCounters)
