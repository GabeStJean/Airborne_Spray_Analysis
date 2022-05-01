import cv2

import time
from CannyEdgeDetection import CannyEdgeDetection

# This is the driver program for the Spray Quality monitor for informed pesticide decisions. This program will
# analyze a series of photos with the canny edge detection algorithm to identify droplets and display
# the spray quality in the form of a pie chart.
#
# Original Author: Gabriel St. Jean
# Email: gjustinst.jean@gmail.com
# Date: 5/1/22

folderPath = "C:/Users/jeans/Documents/photos/"
dilateAndErodeImage = False
showImgMeasurement = False
showPieViewer = True
showContourLen = False
showDebugOutput = False

class SprayQualityDriver(CannyEdgeDetection):

    # Function: Constructor of the program
    def __init__(self):
        CannyEdgeDetection.__init__(self, dilateAndErodeImage, showImgMeasurement, showPieViewer,
                                    showContourLen, showDebugOutput)
        self.minValue = 37
        self.maxValue = 41

    # Function: Performs canny contour detection to identify spray droplets on a series of pre captured images and displays
    #           the spray quality in the form of a piechart
    # Postcondition: The spray quality is shown to the user in the form of a pie chart while
    def analyzePhoto(self):
        count = 1
        while True:
            if (count > 10):
                count = 1
            imgPath = folderPath + "teststand{}.jpg".format(count)
            self.createContourMap(cv2.imread(imgPath))
            self.findContours()
            cv2.imshow("Canny Detection", self.imgBoundingBox)
            k = cv2.waitKey(1) & 0xFF  # window refresh rate in seconds
            if k == 27:  # If the escape key is pressed, end loop
                break
            count += 1
            self.pixelsPerIn = -1
            self.areaList.clear()
            time.sleep(.3)
        cv2.destroyAllWindows()

## Entry point into the program ##
sprayQualityDriver = SprayQualityDriver()
sprayQualityDriver.analyzePhoto()
cv2.destroyAllWindows()
