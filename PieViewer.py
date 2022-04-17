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

        self.pieExplode = [0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0]
        self.vmdValue = ""

    def getDictionary(self):
        return self.sprayDictionary

    def getLength(self):
        return len(self.sprayDictionary)


    def updateSprayDictionary(self, formatedStringList):
        self.sprayDictionary.update({"ultra coarse": int(formatedStringList[0])})
        self.sprayDictionary.update({"extremely coarse": int(formatedStringList[1])})
        self.sprayDictionary.update({"very coarse": int(formatedStringList[2])})
        self.sprayDictionary.update({"coarse": int(formatedStringList[3])})
        self.sprayDictionary.update({"medium": int(formatedStringList[4])})
        self.sprayDictionary.update({"fine": int(formatedStringList[5])})
        self.sprayDictionary.update({"very fine": int(formatedStringList[6])})
        self.sprayDictionary.update({"extremely fine": int(formatedStringList[7])})
        try:
            self.vmdValue = formatedStringList[8].lower().strip()
        except:
            self.vmdValue = ""

    def updateExplodeList(self, vmd):
        if vmd == "ultra coarse":  # In microns
            self.pieExplode = [0.12, 0.0, 0.0, 0.0,
                               0.0, 0.0, 0.0, 0.0]
        elif vmd == "extremely coarse":
            self.pieExplode = [0.0, 0.12, 0.0, 0.0,
                               0.0, 0.0, 0.0, 0.0]
        elif vmd == "very coarse":
            self.pieExplode = [0.0, 0.0, 0.12, 0.0,
                               0.0, 0.0, 0.0, 0.0]
        elif vmd == "coarse":
            self.pieExplode = [0.0, 0.0, 0.0, 0.12,
                               0.0, 0.0, 0.0, 0.0]
        elif vmd == "medium":
            self.pieExplode = [0.0, 0.0, 0.0, 0.0,
                               0.12, 0.0, 0.0, 0.0]
        elif vmd == "fine":
            self.pieExplode = [0.0, 0.0, 0.0, 0.0,
                               0.0, 0.12, 0.0, 0.0]
        elif vmd == "very fine":
            self.pieExplode = [0.0, 0.0, 0.0, 0.0,
                               0.0, 0.0, 0.12, 0.0]
        else:  # Extremely Fine
            self.pieExplode = [0.0, 0.0, 0.0, 0.0,
                               0.0, 0.0, 0.0, 0.12]
        return self.pieExplode

    def updatePieChart(self):
        sprayDataset = np.array([self.sprayDictionary.get("ultra coarse"),
                                 self.sprayDictionary.get("extremely coarse"),
                                 self.sprayDictionary.get("very coarse"),
                                 self.sprayDictionary.get("coarse"),
                                 self.sprayDictionary.get("medium"),
                                 self.sprayDictionary.get("fine"),
                                 self.sprayDictionary.get("very fine"),
                                 self.sprayDictionary.get("extremely fine")])
        plt.rcParams["figure.figsize"] = (10, 5)
        plt.title("$\\bf{Spray Quality}$")
        self.updateExplodeList(self.vmdValue)
        plt.pie(sprayDataset, labels=self.pieLabels, shadow=True, startangle=90,
                colors=self.pieColors, autopct='%.0f%%', explode=self.pieExplode)
        plt.legend(bbox_to_anchor=(1.05, 1.05), title="$\\bf{Legend}$", fontsize='medium',
                   shadow=True)

        plt.show(block=False)  # Allow for piechart window to be closed
        plt.pause(.1)  # Update rate
        plt.clf()  # Refresh pichart

    # Function: Display the spray quality from a properly formated file
    def readFile(self, filePath):
        file = open(filePath)
        fileLine = file.readline()
        while fileLine:
            #print(fileLine, end='')
            formatedStringList = fileLine.split(" ")
            self.updateSprayDictionary(formatedStringList)
            print(self.sprayDictionary)
            # Update the values read by the pie chart
            self.updatePieChart()
            fileLine = file.readline() # Obtain the next line to read
        file.close

    # Function: Display the spray quality from a properly formated string
    def displayFormatedList(self, formatedString):
            formatedString.split(" ")
            self.updateSprayDictionary(formatedString.split(" "))
            self.updatePieChart()
