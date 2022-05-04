# This class is used to obtain a correctly formatted string containing the spray quality
# of a dataset of droplet measurements. This is accomplished by classifying the value of each
# measured particle value in the dataset and then creates a formatted string that contains
# the number of each classified droplet. The program also classifies the Volume Metric Median
# Diameter (VMD) of the dataset and appends it to the string.
#
# Droplet classification is based on the classification used to identify droplets in pesticide
# spray applications which are fine, medium, coarse, and etc.
#
# A correctly formatted string for this program is as follows:
# "UltraCoarse ExtremelyCoarse VeryCoarse Medium Fine VeryFine ExtremelyFine VMD"

class ExtractSprayQuality:

    # Function: The constructor of the class.
    def __init__(self):
        self.areaList = [0]
        self.sprayDictionary = {"ultra coarse": 0,
                                "extremely coarse": 0,
                                "very coarse": 0,
                                "coarse": 0,
                                "medium": 0,
                                "fine": 0,
                                "very fine": 0,
                                "extremely fine": 0}
        self.VMDvalue = ""

    # Function: Clears the spray dictionary to default values.
    def clearSprayDictionaryToDefault(self):
        self.sprayDictionary = {"ultra coarse": 0,
                                "extremely coarse": 0,
                                "very coarse": 0,
                                "coarse": 0,
                                "medium": 0,
                                "fine": 0,
                                "very fine": 0,
                                "extremely fine": 0}

    # Function: Populates a dictionary containing the number of droplet types based on
    #           the values within `areaList`.
    # Precondition: The values within `areaList` are in microns.
    # Postcondition: The sprayDictionary` variable contains the number of droplets present
    #                within `areaList`.
    #
    # Complexity: O(N)
    def updateSprayDictionary(self):
        self.clearSprayDictionaryToDefault()
        for area in self.areaList:
            if area > 650:  # In microns
                keyValue = self.sprayDictionary.get("ultra coarse")
                self.sprayDictionary.update({"ultra coarse": keyValue + 1})
            elif area > 500:
                keyValue = self.sprayDictionary.get("extremely coarse")
                self.sprayDictionary.update({"extremely coarse": keyValue + 1})
            elif area > 400:
                keyValue = self.sprayDictionary.get("very coarse")
                self.sprayDictionary.update({"very coarse": keyValue + 1})
            elif area > 325:
                keyValue = self.sprayDictionary.get("coarse")
                self.sprayDictionary.update({"coarse": keyValue + 1})
            elif area > 225:
                keyValue = self.sprayDictionary.get("medium")
                self.sprayDictionary.update({"medium": keyValue + 1})
            elif area > 145:
                keyValue = self.sprayDictionary.get("fine")
                self.sprayDictionary.update({"fine": keyValue + 1})
            elif area > 60:
                keyValue = self.sprayDictionary.get("very fine")
                self.sprayDictionary.update({"very fine": keyValue + 1})
            else:
                keyValue = self.sprayDictionary.get("extremely fine")
                self.sprayDictionary.update({"extremely fine": keyValue + 1})

    # Function: Obtains the median value of a list of numbers.
    # Precondtion: The list is sorted.
    # Postcondition: The VMD value of the list is found.
    def findVMD(self):
        arrayLength = len(self.areaList)
        if arrayLength == 0:
            self.classifyVMD(0)
        elif (arrayLength % 2 == 2):
            self.classifyVMD(self.areaList[int(arrayLength/2)])
        else:
            self.classifyVMD(self.areaList[int(arrayLength/2) - 1])

    # Function: Obtains the VMD classification based on a micron measurement.
    def classifyVMD(self, area):
            if area > 650: # In microns
                self.VMDvalue = "ultra coarse"
            elif area > 500:
                self.VMDvalue = "extremely coarse"
            elif area > 400:
                self.VMDvalue = "very coarse"
            elif area > 325:
                self.VMDvalue = "coarse"
            elif area > 225:
                self.VMDvalue = "medium"
            elif area > 145:
                self.VMDvalue = "fine"
            elif area > 60:
                self.VMDvalue = "very fine"
            else:
                self.VMDvalue = "extremely fine"

    # Function: Produces a formatted string containing the spray quality of a list of
    #           the area of spray droplets.
    # Precondition: Values in the area list are in microns.
    #
    # @param areaList - a list containing the micron measurement of spray particles.
    def getFormatedString(self, areaList):
        self.areaList = areaList.copy()  # For finding VMD
        self.areaList.sort()
        self.findVMD()
        self.updateSprayDictionary()
        keyValueStr = ""
        for key in self.sprayDictionary:
            keyValueStr += str(self.sprayDictionary.get(key)) + " "
        keyValueStr += self.VMDvalue
        return keyValueStr.strip()
