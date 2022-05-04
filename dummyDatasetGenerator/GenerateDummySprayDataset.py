import random
from datetime import date
import time

# This program generates a dummy dataset of the amount of the distribution of the various
# types of pesticide spray particles.
#
# A correctly formatted string for this program is as follows:
# "UltraCoarse ExtremelyCoarse VeryCoarse Medium Fine VeryFine ExtremelyFine VMD"
#
# Within the correctly formatted string, the VMD value is optional and no pie piece will be exploded
# if omitted.

class GenerateSprayDataset:

    # Function: Constructor of the program.
    def __init__(self, initial):
        self.sprayDictionary = {"ultra coarse" : self.randomIncrement(initial),
                                   "extremely coarse" : self.randomIncrement(initial),
                                   "very coarse" : self.randomIncrement(initial),
                                   "coarse" : self.randomIncrement(initial),
                                   "medium" : self.randomIncrement(initial),
                                   "fine" : self.randomIncrement(initial),
                                   "very fine" : self.randomIncrement(initial),
                                   "extremely fine" : self.randomIncrement(initial)}

    # Function: Adds a random number to increment/decrement the current value of
    #           a pesticide spray distribution.
    def randomIncrement(self, start):
        randNumPos = random.randint(0, 10)
        randNumNeg = random.randint(0, 10)
        if (start <= randNumNeg):          # Prevent a negative number
            return start + randNumPos
        elif (1 == random.randint(0,1)):
            return start + randNumPos
        else:
            return start - randNumNeg

    # Function: Updates all values in the pesticide dataset by arbitrary increments.
    def randomUpdateDictionary(self):
        for key in self.sprayDictionary:
            keyValue = self.sprayDictionary.get(key)
            randomIncValue = self.randomIncrement(keyValue)
            self.sprayDictionary.update({key : randomIncValue})

    def getDictionary(self):
        return self.sprayDictionary

    def getStrRep(self):
        keyValueStr = ""
        for key in self.sprayDictionary:
            keyValueStr += str(self.sprayDictionary.get(key)) + " "
        return keyValueStr.strip()

    def __repr__(self):
        return self.getStrRep()

## Entry point into the program ##
generateSprayDataset = GenerateSprayDataset(30)
t = time.localtime()
currentTime = time.strftime("%H:%M:%S", t)
file = open("../sprayDataset.txt", "w")
file.write("# File format: \"UltraCoarse ExtremelyCoarse VeryCoarse Medium Fine VeryFine ExtremelyFine VMD\".\n"
           + "# VMD is optional.\n# File produced on " + str(date.today()) + " @ " + str(currentTime) + " by GenerateDummySprayDataset.py."+ "\n\n")
for i in range(30):
    generateSprayDataset.randomUpdateDictionary()
    file.write(generateSprayDataset.getStrRep() + "\n")

file.close()
