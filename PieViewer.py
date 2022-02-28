import matplotlib.pyplot as plt
import numpy as np
import random

# This class serves as a proof of concept for the visual component of the design

class PieViewer:

    def __init__(self):
        self.sprayDictionary = {"ultra coarse" : 0,
                                "extremely coarse" : 0,
                                "very coarse" : 0,
                                "coarse" : 0,
                                "medium" : 0,
                                "fine" : 0,
                                "very fine" : 0,
                                "extremely fine" : 0}



    def getDictionary(self):
        return self.sprayDictionary

    def getLength(self):
        return len(self.sprayDictionary)


## Entry point into the program ##
pieViewer = PieViewer()
sprayDictionary = pieViewer.getDictionary()

file = open("sprayDataset.txt", "r")
fileLine = file.readline()


pieLabels = ["Ultra coarse","Extremely coarse",
             "Very coarse","Coarse",
             "Medium","Fine","Very fine",
             "Extremely fine"]

pieColors = ["skyblue","pink","mediumpurple","forestgreen",
            "firebrick","darkorange","slategray","royalblue"]

while fileLine:
    print(fileLine, end='')
    splitString = fileLine.split(" ")
    sprayDictionary.update({"ultra coarse": int(splitString[0])})
    sprayDictionary.update({"extremely coarse": int(splitString[1])})
    sprayDictionary.update({"very coarse": int(splitString[2])})
    sprayDictionary.update({"coarse": int(splitString[3])})
    sprayDictionary.update({"medium": int(splitString[4])})
    sprayDictionary.update({"fine": int(splitString[5])})
    sprayDictionary.update({"very fine": int(splitString[6])})
    sprayDictionary.update({"extremely fine": int(splitString[7])})

    sprayDataset = np.array([sprayDictionary.get("ultra coarse"),
                              sprayDictionary.get("extremely coarse"),
                                sprayDictionary.get("very coarse"),
                                sprayDictionary.get("coarse"),
                                sprayDictionary.get("medium"),
                                sprayDictionary.get("fine"),
                               sprayDictionary.get("very fine"),
                                sprayDictionary.get("extremely fine")])
    fileLine = file.readline()

    plt.title("Spray Quality")
    plt.pie(sprayDataset, labels = pieLabels, shadow = True, startangle = 90,
            colors = pieColors, autopct='%.0f%%')
    plt.legend(bbox_to_anchor=(1.05, 1.05), title = "Legend", fontsize = 'xx-small',
               shadow = True)
    plt.show(block=False)     # Allow for piechart window to be closed
    plt.pause(.01)            # Update rate
    plt.clf()                 # Refresh pichart

file.close
