import numpy as np
import cv2
from ImageFormater import ImageFormater
from PieViewer import PieViewer
from ExtractSprayQuality import ExtractSprayQuality
import time

# This program adds a trackbar to find the optimal parameters for the binary
# image preprocessing for threshold based contour detection.

# Program Parameters
dilateAndErodeImage = False
showImgMeasurement = True
showPieViewer = True

# Opening File
photoPath = "C:/Users/jeans/Documents/photos/"
img = cv2.imread(photoPath + "/teststand6.jpg")

# teststand6 - Reference object
# teststand1 - best quality

# Resizing
dimension = (int(img.shape[1] * 7 / 100), int(img.shape[0] * 7 / 100))
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
areaList = []

def updateMinValue(value):
    global minValue
    minValue = value

def updateMaxValue(value):
    global maxValue
    maxValue = value

def updateSigma(value):
    global sigma
    if value == 1:
        sigma = 5
    else:
        sigma = 3

def viewPieChart():
    global areaList

    formatedString = extractSprayQuality.getFormatedString(areaList)
    pieViewer.displayFormatedList(formatedString, 3, 3)
    areaList.clear()

def findContours(imgToDrawOn, inputImage):
    global pixelsPerIn
    global iteration
    global imgBoundingBox
    global imgContourDraw
    global areaList

    imgBoundingBox = imgToDrawOn.copy()
    (contours, _) = cv2.findContours(inputImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Make the largest area (the US quarter) located at the first index
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Calibration: Obtain the area of the quarter in pixels
    if (pixelsPerIn == -1):
        pixelsPerIn = cv2.contourArea(contours[0])/US_QUARTER

    # To show the area of the coin, make i = 0 and remove upper bound
    for i in range(1, len(contours)):
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
            #print("i=" + str(i) + ", Pixel area : " + str(pixelArea) +
            #    ", Area in inches: " + areaStringIn.format(area = transferFunction / IN_TO_MICRON) +
            #    ", Area in microns: " + areaString.format(area = transferFunction) +
            #    ", corner points: " + str(objectCorners))

            # Draw bounding boxes with the area of each object
            x, y, w, h = cv2.boundingRect(cornerPoints) # x cord, y, cord, width, and height
            cv2.rectangle(imgBoundingBox, (x,y), (x+w, y+h), (0, 255, 0), 2)
            if (showImgMeasurement == True):
                cv2.putText(imgBoundingBox, areaString.format(area = transferFunction),
                    ( int(x + (w / 2) - 10), int(y + (h / 2) - 19)), cv2.FONT_HERSHEY_COMPLEX,
                    0.5, (0, 0, 0), 0)

    if (showPieViewer == True):
        viewPieChart()
    cv2.drawContours(imgToDrawOn, contours, -1, (255, 0, 0), 4) # Draw all contours
    imgContourDraw = imgToDrawOn.copy()
    iteration += 1

def createContourMap():
    global gray
    global sigma
    global imgContourMap
    global minValue
    global maxValue

    GaussianBlur = cv2.GaussianBlur(gray, (sigma, sigma), 0)
    imgContourMap = cv2.Canny(GaussianBlur, minValue, maxValue)

    if (dilateAndErodeImage == True):
        kernel = np.ones((5, 5))
        imgDial = cv2.dilate(imgContourMap.copy(), kernel, iterations=2)
        imgThre = cv2.dilate(imgDial, kernel, iterations=2)
        imgContourMap = imgThre.copy()

def cannyTrackbar():
    global imgStackCanny
    global img
    global imgContourMap
    global imgContourDraw
    global imgBoundingBox
    global minValue
    global maxValue
    global sigma

    # Creating the trackbar
    cv2.namedWindow("Canny Detection")  # Binds the trackbar and image window
    cv2.createTrackbar('minval', "Canny Detection", minValue, 400, updateMinValue)
    cv2.createTrackbar('maxval', "Canny Detection", maxValue, 400, updateMaxValue)
    cv2.createTrackbar('sigma', "Canny Detection", 0, 1, updateSigma)
    while (1):
        imgStackCanny = imageFormater.stackImages(1, ([img, imgBoundingBox, imgContourMap]))
        cv2.imshow("Canny Detection", imgStackCanny)
        k = cv2.waitKey(1) & 0xFF  # window refresh rate in seconds
        if k == 27:  # If the escape key is pressed, end loop
            break
        createContourMap()
        imgContourDraw = img.copy()
        findContours(imgContourDraw, imgContourMap)

## Entry point into the program
imageFormater = ImageFormater()

# Canny Edge Detection
gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)  # Needed to turn imag

createContourMap()

# Drawing contours
imgContourDraw = img.copy()
imgBoundingBox = None
findContours(imgContourDraw, imgContourMap)

cannyTrackbar()
cv2.destroyAllWindows()
