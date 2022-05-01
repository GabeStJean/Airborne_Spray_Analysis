import matplotlib.pyplot as plt
import numpy as np
import random

# This class creates a pie chart that will be used to visualize the spray quality of a pesticide
# spray application. The spray quality for this application contains the ratio of droplet size
# classification for measured particles and the Volume Metric Median Diameter (VMD) value of the
# dataset. The VMD value of the dataset is represented as an exploded pie piece on the chart.
#
# The program contains a function to display a correctly formatted string  containing the spray
# quality, and a function to interpret a file containing values pertaining to spray quality.
# A exploding pie piece within the chart will be used to denote the VMD value of the application.
#
# A correctly formatted string for this program is as follows:
# "UltraCoarse ExtremelyCoarse VeryCoarse Medium Fine VeryFine ExtremelyFine VMD"
#
# Within the correctly formatted string, the VMD value is optional and no pie piece will be exploded
# if ommitted.

class PieViewer:

    # Function: The constructor of the class.
    def __init__(self):
        self.debugMode = False
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

    # Function: Retrieves the spray dictionary.
    def getDictionary(self):
        return self.sprayDictionary

    # Function: Returns the length of the spray dictionary.
    def getLength(self):
        return len(self.sprayDictionary)

    # Function: Updates the `sprayDictionary` variable from a properly formatted string.
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

    # Function: Denotes the VMD value of the spray quality as an explodeded pie piece.
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
        elif vmd == "extremely fine":
            self.pieExplode = [0.0, 0.0, 0.0, 0.0,
                               0.0, 0.0, 0.0, 0.12]
        else:
            [0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0]
        return self.pieExplode

    # Function: Updates the piechart with the values obtained from `sprayDictionary`.
    # Postcondition: A piechart is updated for the user on the screen.
    def updatePieChart(self, windowWidth = 9, windowLength = 5):
        sprayDataset = np.array([self.sprayDictionary.get("ultra coarse"),
                                 self.sprayDictionary.get("extremely coarse"),
                                 self.sprayDictionary.get("very coarse"),
                                 self.sprayDictionary.get("coarse"),
                                 self.sprayDictionary.get("medium"),
                                 self.sprayDictionary.get("fine"),
                                 self.sprayDictionary.get("very fine"),
                                 self.sprayDictionary.get("extremely fine")])

        plt.rcParams["figure.figsize"] = (windowWidth, windowLength)
        plt.title("$\\bf{Spray Quality}$")
        self.updateExplodeList(self.vmdValue)
        plt.pie(sprayDataset, labels=self.pieLabels, shadow=True, startangle=90,
                colors=self.pieColors, autopct='%.0f%%', explode=self.pieExplode)
        plt.legend(bbox_to_anchor=(1.05, 1.05), title="$\\bf{Legend}$", fontsize='medium',
                   shadow=True)

        plt.show(block=False)  # Allow for piechart window to be closed
        plt.pause(.1)  # Update rate
        plt.clf()  # Refresh pichart

    # Function: Displays the spray quality from a properly formatted file
    # Precondition: The file path exists.
    # Postcondition: A pie chart that changes in realtime from values parsed through a file
    #                is outputted to the screen.
    def readFile(self, filePath):
        file = open(filePath)
        fileLine = file.readline()
        while fileLine:
            if (self.debugMode == True):
                print(fileLine, end='')
            if (fileLine == "\n" or fileLine.split()[0] == "#"):
                fileLine = file.readline()  # Obtain the next line to be read
            else:
                formatedStringList = fileLine.split(" ")
                self.updateSprayDictionary(formatedStringList)
                # Update the values read by the pie chart
                self.updatePieChart()
            fileLine = file.readline() # Obtain the next line to be read
        file.close

    # Function: Display the spray quality from a properly formatted string
    #
    # @param formatted String contains the number of particle types and the VMD classification
    def displayFormatedList(self, formatedString, windowWidth = 9, windowLength = 5):
            formatedString.split(" ")
            self.updateSprayDictionary(formatedString.split(" "))
            self.updatePieChart(windowWidth, windowLength)
