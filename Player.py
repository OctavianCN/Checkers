from Counter import Counter
class Player:

    def __init__(self,counterColor):
        self.defaultNumberOfCounters = 12
        self.currentCounters = []
        self.whiteCountersDefaultPositions = [(0,1),(0,3),(0,5),(0,7),(1,0),(1,2),(1,4),(1,6),(2,1),(2,3),(2,5),(2,7)]
        self.blackCountersDefaultPositions = [(5,0),(5,2),(5,4),(5,6),(6,1),(6,3),(6,5),(6,7),(7,0),(7,2),(7,4),(7,6)]
        self.lastRow = None
        for i in range(self.defaultNumberOfCounters):
            counter = Counter()
            self.currentCounters.append(counter)

        for i in range(self.defaultNumberOfCounters):
            if counterColor == "white":
                self.currentCounters[i].positions = self.whiteCountersDefaultPositions[i]
                self.currentCounters[i].character = "a"
                self.currentCounters[i].kingCharacter = "ak"
            if counterColor == "black":
                self.currentCounters[i].positions = self.blackCountersDefaultPositions[i]
                self.currentCounters[i].character = "b"
                self.currentCounters[i].kingCharacter = "bk"

    def HaveCounterOnPosition(self,posX,posY):
        for counter in self.currentCounters:
            if counter.positions[0] == posX and counter.positions[1] == posY:
               return True
        return False


    def GetCounterFromPosition(self,posX,posY):
        try:
            for counter in self.currentCounters:
                if counter.positions == (posX,posY):
                    return counter
        except:
            print("Counter not found")

    def Move(self):
        pass

