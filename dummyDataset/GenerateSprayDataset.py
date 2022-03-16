import random

# This program generates a dummy dataset of the amount of the distribution of the various
# types of pesticide spray particles.

class GenerateSprayDataset:
    def __init__(self, initial):
        self.sprayDictionary = {"ultra coarse" : self.randomIncrement(initial),
                                   "extremely coarse" : self.randomIncrement(initial),
                                   "very coarse" : self.randomIncrement(initial),
                                   "coarse" : self.randomIncrement(initial),
                                   "medium" : self.randomIncrement(initial),
                                   "fine" : self.randomIncrement(initial),
                                   "very fine" : self.randomIncrement(initial),
                                   "extremely fine" : self.randomIncrement(initial)}

    # Function: adds a random number to increment/decrement the current value of
    #           a pesticide spray distribution
    def randomIncrement(self, start):
        randNumPos = random.randint(0, 10)
        randNumNeg = random.randint(0, 10)
        if (start <= randNumNeg):          # Prevent a negative number
            return start + randNumPos
        elif (1 == random.randint(0,1)):
            return start + randNumPos
        else:
            return start - randNumNeg

    # Function: Updates all values in the pesticide dataset by arbitray increments
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

file = open("sprayDataset.txt", "w")

for i in range(30):
    generateSprayDataset.randomUpdateDictionary()
    file.write(generateSprayDataset.getStrRep() + "\n")

file.close()
