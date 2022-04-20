

class ExtractSprayQuality:

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
        self.file = open("sprayQualityDataset.txt", "w")

    def clearSprayDictionaryToDefault(self):
        self.sprayDictionary = {"ultra coarse": 0,
                                "extremely coarse": 0,
                                "very coarse": 0,
                                "coarse": 0,
                                "medium": 0,
                                "fine": 0,
                                "very fine": 0,
                                "extremely fine": 0}

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

    def findVMD(self):
        arrayLength = len(self.areaList)
        if arrayLength == 0:
            self.classifyVMD(0)
        elif (arrayLength % 2 == 2):
            self.classifyVMD(self.areaList[int(arrayLength/2)])
        else:
            self.classifyVMD(self.areaList[int(arrayLength/2) - 1])

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

