from Game import Game
from Singleton import singleton
@singleton
class Menu:
    def __init__(self):

        self.menuQuestions = {}
        self.menuQuestions["What type of algorithm do you want MiniMax or Alpha-Beta Pruning?\n"] = ["minimax", "alpha-beta pruning"]
        self.menuQuestions["What color of counters do you want Black or White(Black have the first move)?\n"] = ["white", "black"]
        self.menuQuestions["What dificulty do you want(Low,Medium,Hard)?\n"] = ["low", "medium", "hard"]
        self.playerAnswers = []
        self.__askQuestions()
        self.Game = Game(self.playerAnswers[0],self.playerAnswers[1],self.playerAnswers[2])
        self.Game.StartGame()
        if self.Game._restart == True:
            self.__init__()

    def __askQuestions(self):
        gotAnswer = False
        for question in self.menuQuestions:
            while gotAnswer == False:
                playerAnswer = input (question)
                for answers in self.menuQuestions[question]:
                    if answers == playerAnswer.lower():
                        gotAnswer = True
                        self.playerAnswers.append(answers)
                        break
            gotAnswer = False

