import numpy as np
import cv2
from ImageFormater import ImageFormater
from PieViewer import PieViewer
from ExtractSprayQuality import ExtractSprayQuality
import time

# This program adds a trackbar to find the optimal parameters for the Canny Contour detection
# algorithim.

# Program Parameters
dilateAndErodeImage = False
showImgMeasurement = True
showPieViewer = True
showContourLen = True
showDebugOutput = False

# Opening File
photoPath = "C:/Users/jeans/Documents/photos/"
# teststand6 - Reference object
# teststand1 - best quality
img = cv2.imread(photoPath + "/teststand2.jpg")

# Resizing
dimension = (int(img.shape[1] * 7 / 100), int(img.shape[0] * 7 / 100)) # (width, height)
img = cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)

# Conversion
US_QUARTER = .71 # in inches
IN_TO_MICRON = 25400
pixelsPerIn = -1

# Thresholding parameters
minValue = 70
maxValue = 122
sigma = 5 # can be only 5 or 3

# Other
iteration = 1
pieViewer = PieViewer()
extractSprayQuality = ExtractSprayQuality()
areaList = [] # Contains the micron measurement of contours that fit a criteria

# Function: Updates the minvalue parameter in the Canny Contour dectection algorithim.
# Precondition: Function is used as a callback function in a trackbar function
#
# @param value The current value of the trackbar
def updateMinValue(value):
    global minValue
    minValue = value

# Function: Updates the max value parameter in the Canny Contour dectection algorithim.
# Precondition: Function is used as a callback function in a trackbar function
#
# @param value The current value of the trackbar
def updateMaxValue(value):
    global maxValue
    maxValue = value

# Function: Updates the sigma value for the Gaussain blur to be either 3x3 or 5x5
# Precondition: Function is used as a callback function in a trackbar function
#
#@param value The current value of the trackbar
def updateSigma(value):
    global sigma
    if value == 1:
        sigma = 5
    else:
        sigma = 3

# Function: Updates a Piechart containing the area of  detected contours
# Precondition: The boolean class variable `showPieViewer` is enabled
def viewPieChart():
    global areaList

    formatedString = extractSprayQuality.getFormatedString(areaList)
    pieViewer.displayFormatedList(formatedString, 3, 3)

# Function: Finds detected contours defined by a criteria.
# Precondition: The contour map of the variable `img` is generated in `imgContourMap`.
# Postcondition: A contour map of an image used to produce a new image containing bounding
#                boxes around contours in `imgBoundingBox` and outlines of the contours
#                in `imgContourDraw`. The `areaList` variable is updated to contain the micron
#                measurement of contours that fit a criteria.
def findContours():
    global pixelsPerIn
    global imgBoundingBox
    global imgContourDraw
    global areaList

    imgBoundingBox = img.copy()
    imgContourDraw = img.copy()
    # Obtain an array of pixel coordinates that defines each contour in the map
    (contours, _) = cv2.findContours(imgContourMap, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Make the largest area (the US quarter) located at the first index
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Calibration: Obtain the area of the quarter in pixels
    if (pixelsPerIn == -1):
        pixelsPerIn = cv2.contourArea(contours[0])/US_QUARTER

    # To show the area of the coin, make i = 0 and remove upper bound
    for i in range(0, len(contours)):
        # Measures the area of the contour
        pixelArea = cv2.contourArea(contours[i])

        # Identifying shape of a contour
        arcLength = cv2.arcLength(contours[i], True)
        # Approximates contour shape (since shapes can be irregular)
        cornerPoints = cv2.approxPolyDP(contours[i], .01 * arcLength, True)
        objectCorners = len(cornerPoints)

        # upper bound is 1016 microns and the lower bound is 27 microns to remove noise
        upperBound = .04 * pixelsPerIn   # .04 inches = 1016 microns
        lowerBound = .0011 * pixelsPerIn # .0011 inches = 27 microns

        areaString = "{area: .2f} um"  # formating
        areaStringIn = "{area: .2f} in"  # formating

        # Filter out shapes that are not a circle and other noise
        if (pixelArea > lowerBound and pixelArea < upperBound and objectCorners > 4):
            transferFunction = pixelArea / pixelsPerIn * IN_TO_MICRON # Convert from pixel area into inches
            areaList.append(transferFunction)
            if (showDebugOutput == True):
                print("i=" + str(i) + ", Pixel area : " + str(pixelArea) +
                    ", Area in inches: " + areaStringIn.format(area = transferFunction / IN_TO_MICRON) +
                    ", Area in microns: " + areaString.format(area = transferFunction) +
                    ", corner points: " + str(objectCorners))

            # Draw bounding boxes with the area of each object
            x, y, w, h = cv2.boundingRect(cornerPoints) # x cord, y, cord, width, and height
            cv2.rectangle(imgBoundingBox, (x,y), (x+w, y+h), (0, 255, 0), 2)
            if (showImgMeasurement == True):
                cv2.putText(imgBoundingBox, areaString.format(area = transferFunction),
                    ( int(x + (w / 2) - 10), int(y + (h / 2) - 19)), cv2.FONT_HERSHEY_COMPLEX,
                    0.5, (0, 0, 0), 0)

    if (showPieViewer == True):
        viewPieChart()

    if (showContourLen == True):
        cv2.putText(imgContourMap, "Contours: " + str(len(contours)),
                    (int(imgContourMap.shape[0] - imgContourMap.shape[0] / 1.05),
                     int(imgContourMap.shape[1] - imgContourMap.shape[1] / 2.7)),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 100), 0)
        cv2.putText(imgBoundingBox, "Contours: " + str(len(areaList)),
                    (int(imgContourMap.shape[0] - imgContourMap.shape[0] / 1.05),
                     int(imgContourMap.shape[1] - imgContourMap.shape[1] / 2.7)),
                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 100), 0)

    cv2.drawContours(imgContourDraw, contours, -1, (255, 0, 0), 4) # Draw all contours

# Function: Creates a contour map of an image using Canny edge detection
# Postcondition: An image containing the contour map of the original is produced
#
# @param grayScaleImg The gray scale image to be converted into a contour map.
# @param minValue The min value parameter for canny edge detection.
# @param maxValue the max value parameter for canny edge decetion.
def createContourMap(grayScaleImg, minValue, maxValue):
    global sigma
    global imgContourMap

    GaussianBlur = cv2.GaussianBlur(grayScaleImg, (sigma, sigma), 0) # Removes noise
    imgContourMap = cv2.Canny(GaussianBlur, minValue, maxValue)
    # Used to enhance the contour map by creating smoother lines
    if (dilateAndErodeImage == True):
        kernel = np.ones((5, 5))
        imgDial = cv2.dilate(imgContourMap, kernel, iterations=2)
        imgThre = cv2.dilate(imgDial, kernel, iterations=2)
        imgContourMap = imgThre.copy()

# Function: Creates a track bar with sliders that will adjust the parametrs
def cannyTrackbar():
    global grayScaleImg
    global imgStackCanny
    global imgContourMap
    global imgContourDraw
    global imgBoundingBox
    global minValue
    global maxValue
    global sigma
    global areaList

    # Creating the trackbar
    cv2.namedWindow("Canny Edge Detection Tuner")  # Binds the trackbar and image window
    cv2.createTrackbar('minval', "Canny Edge Detection Tuner", minValue, 400, updateMinValue)
    cv2.createTrackbar('maxval', "Canny Edge Detection Tuner", maxValue, 400, updateMaxValue)
    cv2.createTrackbar('sigma', "Canny Edge Detection Tuner", 0, 1, updateSigma)
    # Execute until the exit key is pressed
    while (1):
        imgStackCanny = imageFormater.stackImages(1, ([img, imgBoundingBox, imgContourMap]))
        cv2.imshow("Canny Edge Detection Tuner", imgStackCanny)
        k = cv2.waitKey(1) & 0xFF  # window refresh rate of trackbar in seconds
        if k == 27:  # If the escape key is pressed, end loop
            break
        createContourMap(grayScaleImg.copy(), minValue, maxValue)
        findContours()
        areaList.clear()
        time.sleep(.5)



## Entry point into the program
imageFormater = ImageFormater() # Used to display multiple images at once

# Canny Edge Detection Preprocessing
grayScaleImg = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)  # Needed to turn imag

createContourMap(grayScaleImg, minValue, maxValue)

# Drawing contours
imgContourDraw = img.copy() # Draws the contour map onto the original image
imgBoundingBox = img.copy() # Draws bounding boxes around contours onto the original image
findContours()
cannyTrackbar()
cv2.destroyAllWindows()
