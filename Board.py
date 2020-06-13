class Board:

    def __init__(self):
        self.dimension = 8 # width and height
        self.emptySpace = "_"
        self.board = []
        for i in range(self.dimension):
            row = []
            for j in range(self.dimension):
                row.append(self.emptySpace)
            self.board.append(row)
    def Clear(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.board[i][j] = self.emptySpace
    def PutCounterOnBoardInPosition(self,positionX,positionY,character):
        self.board[positionX][positionY] = character
    def ChangeCounterPosition(self,oldPositionX,oldPositionY,newPositionX,newPositionY,character):
        self.board[oldPositionX][oldPositionY] = self.emptySpace
        self.board[newPositionX][newPositionY] = character
    def ElimFromBoard(self,positionX,positionY):
        self.board[positionX][positionY] = self.emptySpace
    def DrawBoard(self):
        print("\n")
        nr = 0
        for row in self.board:
            if nr == 0:
                list = [" "]
                for i in range(len(row)):
                    list.append(i)
                    list.append(" ")
                print(*list, sep = ', ')
            print(nr,row)
            nr = nr + 1
        print("\n")
