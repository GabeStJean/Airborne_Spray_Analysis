
import cv2
import sys
from threading import Thread
from PieViewer import PieViewer
from ExtractSprayQuality import ExtractSprayQuality
import random

import time

pieViewer = PieViewer()
extractSprayQuality = ExtractSprayQuality()
areaList = [0]

def analyzePhoto():
    # Opening File
    photoPath = "C:/Users/jeans/Documents/photos/"
    img = cv2.imread(photoPath + "/DSC_9984.jpg")
    #/DSC_9984.jpg

    # Resizing
    dimension = (int(img.shape[1] * 10 / 100), int(img.shape[0] * 10 / 100))
    img = cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)

def updateValues():
    global areaList

    while True:
        for i in range(len(areaList)):
            randNum = random.randrange(25, 75)
            if (random.randrange(0, 1) == 0):
                randNum = -1 * randNum

            areaList[i] = areaList[i] + randNum
            time.sleep(1)

## Entry point into the program
pieViewerThread = Thread(target=updateValues, args=(), daemon=True)
pieViewerThread.start()

areaList = [100, 150, 210, 75, 500, 550, 330, 205, 400, 445, 100, 650, 700]
while True:
    formatedStr = extractSprayQuality.getFormatedString(areaList)
    pieViewer.displayFormatedList(formatedStr)

#while True:
   #print("Marcus")
    #time.sleep(2)

