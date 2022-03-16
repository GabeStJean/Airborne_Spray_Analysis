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
        self.pieLabels = ["Ultra coarse","Extremely coarse",
             "Very coarse","Coarse",
             "Medium","Fine","Very fine",
             "Extremely fine"]

        self.pieColors = ["skyblue","pink","mediumpurple","darkorange",
            "forestgreen","yellow","darkviolet","royalblue"]


    def getDictionary(self):
        return self.sprayDictionary

    def getLength(self):
        return len(self.sprayDictionary)

    def readFile(self, filePath):
        self.sprayDictionary
        file = open(filePath)
        fileLine = file.readline()
        while fileLine:
            #print(fileLine, end='')
            splitString = fileLine.split(" ")
            self.sprayDictionary.update({"ultra coarse": int(splitString[0])})
            self.sprayDictionary.update({"extremely coarse": int(splitString[1])})
            self.sprayDictionary.update({"very coarse": int(splitString[2])})
            self.sprayDictionary.update({"coarse": int(splitString[3])})
            self.sprayDictionary.update({"medium": int(splitString[4])})
            self.sprayDictionary.update({"fine": int(splitString[5])})
            self.sprayDictionary.update({"very fine": int(splitString[6])})
            self.sprayDictionary.update({"extremely fine": int(splitString[7])})
            print(self.sprayDictionary)
            sprayDataset = np.array([self.sprayDictionary.get("ultra coarse"),
                                     self.sprayDictionary.get("extremely coarse"),
                                     self.sprayDictionary.get("very coarse"),
                                     self.sprayDictionary.get("coarse"),
                                     self.sprayDictionary.get("medium"),
                                     self.sprayDictionary.get("fine"),
                                     self.sprayDictionary.get("very fine"),
                                     self.sprayDictionary.get("extremely fine")])
            fileLine = file.readline()
            plt.title("Spray Quality")
            plt.pie(sprayDataset, labels = self.pieLabels, shadow = True, startangle = 90,
                    colors = self.pieColors, autopct='%.0f%%')
            plt.legend(bbox_to_anchor=(1.05, 1.05), title = "Legend", fontsize = 'xx-small',
                       shadow = True)
            plt.show(block=False)     # Allow for piechart window to be closed
            plt.pause(.01)            # Update rate
            plt.clf()                 # Refresh pichart
        file.close



## Entry point into the program ##
pieViewer = PieViewer()
pieViewer.readFile("/home/pi/Airborne-Spray-Analysis/dummyDataset/sprayDataset.txt")
