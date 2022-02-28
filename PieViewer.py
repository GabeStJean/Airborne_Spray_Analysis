import matplotlib.pyplot as plt
import numpy as np
import random

# This class serves as a proof of concept for the visual component of the design

class PieViewer:

    def __init__(self, initial):
        self.moleculeDictionary = {"ultra coarse" : self.randomIncrement(initial),
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

    def randomUpdateDictionary(self):
        pass

    def getDictionary(self):
        return self.moleculeDictionary


## Entry point into the program ##
pieViewer = PieViewer(30)

moleculeDictionary = pieViewer.getDictionary()

pieLabels = ["Ultra coarse","Extremely coarse",
             "Very coarse","Coarse",
             "Medium","Fine","Very fine",
             "Extremely fine"]

pieColors = ["pink","blue","red","purple",
            "green","orange","gray","yellow"]

#sliceExlpode = (0,0,0.07,0,0,0,0,0)

# Display pie chart of changes in molecule distribution continuously
for i in range(15):
    for key in moleculeDictionary:
        keyValue = moleculeDictionary.get(key)
        randomIncValue = pieViewer.randomIncrement(keyValue)
        moleculeDictionary.update({key : randomIncValue})

    moleculeDataset = np.array([moleculeDictionary.get("ultra coarse"),
                               moleculeDictionary.get("extremely coarse"),
                               moleculeDictionary.get("very coarse"),
                               moleculeDictionary.get("coarse"),
                               moleculeDictionary.get("medium"),
                               moleculeDictionary.get("fine"),
                               moleculeDictionary.get("very fine"),
                               moleculeDictionary.get("medium")])
    print(moleculeDictionary)

    plt.title("Spray Quality")
    plt.pie(moleculeDataset, labels = pieLabels, shadow = True, startangle = 90,
            colors = pieColors, autopct='%.0f%%')
    plt.legend(bbox_to_anchor=(1.05, 1.05), title = "Legend", fontsize = 'xx-small',
               shadow = True)
    plt.show(block=False)     # Allow for piechart window to be closed
    plt.pause(.05)            # Update rate
    plt.clf()                 # Refresh pichart
