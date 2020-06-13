from Player import Player

class HumanPlayer(Player):

    def __init__(self,color):
        self.color = color
        super().__init__(color)

    def Move(self):
        print("\n What coutner do you want to move? \n")
        oldPositionX = input("Type position on row")
        oldPositionY = input("Type position on column")
        print("\n Where do you want to move? \n")
        positionX = input("Type position on row")
        positionY = input("Type position on column")
        return  int(oldPositionX),int(oldPositionY),int(positionX),int(positionY)
