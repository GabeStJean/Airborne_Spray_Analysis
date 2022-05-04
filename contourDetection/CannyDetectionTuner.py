import cv2
import sys
sys.path.append('..')
from Airborne_Spray_Analysis.CannyEdgeDetection import CannyEdgeDetection

# This program adds a trackbar to find the optimal parameters for the Canny Contour detection
# algorithm. In particular, the minValue, maxValue, and threshold parameters. Once these
# parameters are fine-tuned for a desired image, they can be used as hard coded values
# in the driver program.

imgPath = "C:/Users/jeans/Documents/photos/teststand1.jpg"
dilateAndErodeImage = False
showImgMeasurement = True
showPieViewer = True
showContourLen = True
showDebugOutput = False

class CannyDetectionTuner(CannyEdgeDetection):

    # Function: Constructor of the program
    def __init__(self):
        self.modifyPieViewerDimensions(3,3)
        CannyEdgeDetection.__init__(self, dilateAndErodeImage, showImgMeasurement, showPieViewer,
                                    showContourLen, showDebugOutput)
        self.createContourMap(cv2.imread(imgPath))
        self.findContours()

    # Function: Updates the minvalue parameter in the Canny Contour detection algorithm.
    # Precondition: Function is used as a callback function in a trackbar function.
    #
    # @param value The current value of the trackbar.
    def updateMinValue(self, value):
        self.minValue = value

    # Function: Updates the max value parameter in the Canny Contour detection algorithm.
    # Precondition: Function is used as a callback function in a trackbar function.
    #
    # @param value The current value of the trackbar.
    def updateMaxValue(self, value):
        self.maxValue = value

    # Function: Updates the sigma value for the Gaussian blur to be either 3x3 or 5x5.
    # Precondition: Function is used as a callback function in a trackbar function.
    #
    # @param value The current value of the trackbar.
    def updateSigma(self, value):
        if value == 1:
            self.sigma = 5
        else:
            self.sigma = 3

    # Function: Updates the sigma value for the Gaussain blur to be either 3x3 or 5x5
    # Precondition: Function is used as a callback function in a trackbar function
    #
    # @param value The current value of the trackbar
    def updateIterationNum(self, value):
        self.iterationNum = value

    # Function: Creates a track bar with sliders that serve to fine tune the parameters for the canny detection
    #           Algorithm.
    # Complexity: O(N)
    def cannyTrackbar(self):
        # Creating the trackbar
        cv2.namedWindow("Canny Edge Detection Tuner")  # Binds the trackbar and image window
        cv2.createTrackbar('minval', "Canny Edge Detection Tuner", self.minValue, 400, self.updateMinValue)
        cv2.createTrackbar('maxval', "Canny Edge Detection Tuner", self.maxValue, 400, self.updateMaxValue)
        cv2.createTrackbar('sigma', "Canny Edge Detection Tuner", 0, 1, self.updateSigma)
        if (self.dilateAndErodeImage == True):
            cv2.createTrackbar('iterations', "Canny Edge Detection Tuner", self.iterationNum, 7, self.updateIterationNum)
        # Execute until the exit key is pressed
        while (1):
            imgStack = self.imageFormatter.stackImages(1, ([self.img, self.imgBoundingBox, self.imgContourMap]))
            cv2.imshow("Canny Edge Detection Tuner", imgStack)
            k = cv2.waitKey(1) & 0xFF  # window refresh rate of trackbar in seconds
            if k == 27:  # If the escape key is pressed, end loop
                break
            self.createContourMap(cv2.imread(imgPath))
            self.findContours()
            self.areaList.clear()

## Entry point into the program ##
cannyDetectionTuner = CannyDetectionTuner()
cannyDetectionTuner.cannyTrackbar()
cv2.destroyAllWindows()