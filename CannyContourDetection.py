import numpy as np
import cv2
from ImageFormater import ImageFormater
import time
# This program adds a trackbar to find the optimal parameters for the binary
# image preprocessing for threshold based contour detection.

# Opening File
photoPath = "C:/Users/jeans/Documents/photos/"
img = cv2.imread(photoPath + "/teststand7.jpg")

# Resizing
dimension = (int(img.shape[1] * 9 / 100), int(img.shape[0] * 9 / 100))
img = cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)

# Conversion
US_QUARTER = .71 # in inches
IN_TO_MICRON = 25400
pixelsPerIn = -1

# Thresholding parameters
minValue = 100
maxValue = 255
sigma = 5 # can be only 5 or 3

# Other
iteration = 1

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

def findContoursCanny(imgToDrawOn, inputImage):
    global pixelsPerIn
    global iteration

    print("\niteration: " + str(iteration))
    (contours, _) = cv2.findContours(inputImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Make the largest area (the US quarter) located at the first index
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Calibration: Obtain the area of the quarter in pixels
    if (pixelsPerIn == -1):
        pixelsPerIn = cv2.contourArea(contours[0])/US_QUARTER

    for i in range(1, len(contours)):
        pixelArea = cv2.contourArea(contours[i])
        # upper bound is 762 microns and the lower bound is 40 microns to remove noise
        upperBound = .03 * pixelsPerIn
        lowerBound = .0011 * pixelsPerIn
        if (pixelArea > lowerBound and pixelArea < upperBound):
            transferFunction = pixelArea / pixelsPerIn # Convert from pixel area into inches
            #transferFunction = pixelArea / pixelsPerIn * IN_TO_MICRON
            print("i=" + str(i) + ", Pixel area : " + str(cv2.contourArea(contours[i])) +
                " Area in inches: " + str(transferFunction) +
                " Area in microns: " + str(transferFunction * IN_TO_MICRON))
    cv2.drawContours(imgToDrawOn, contours, -1, (255, 0, 0), 4)
    iteration += 1

def cannyTrackbar():
    global imgStackCanny
    global gray
    global imgCanny
    global imgContourDraw
    global imgContourDrawThre
    global sigma

    # Creating the trackbar
    cv2.namedWindow("Canny Detection")  # Binds the trackbar and image window
    cv2.createTrackbar('minval', "Canny Detection", minValue, 400, updateMinValue)
    cv2.createTrackbar('maxval', "Canny Detection", maxValue, 400, updateMaxValue)
    cv2.createTrackbar('sigma', "Canny Detection", 0, 1, updateSigma)
    while (1):
        imgStackCanny = imageFormater.stackImages(0.8, ([imgContourDraw, imgCanny]))
        cv2.imshow("Canny Detection", imgStackCanny)
        k = cv2.waitKey(1) & 0xFF  # window refresh rate in seconds
        if k == 27:  # If the escape key is pressed, end loop
            break
        GaussianBlur = cv2.GaussianBlur(gray, (sigma, sigma), 0)
        imgCanny = cv2.Canny(GaussianBlur, minValue, maxValue)
        imgContourDraw = img.copy()
        findContoursCanny(imgContourDraw, imgCanny)

## Entry point into the program
imageFormater = ImageFormater()

# Canny Edge Detection
gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)  # Needed to turn imag
GaussianBlur = cv2.GaussianBlur(gray, (sigma, sigma), 0) # To remove noise and imp
imgCanny = cv2.Canny(GaussianBlur, minValue, maxValue)

# Drawing contours
imgContourDraw = img.copy()
findContoursCanny(imgContourDraw, imgCanny)

# Drawing bounding Box
#imgBoundingBox = img.copy()
#drawBoundingBox()

imgStackCanny = imageFormater.stackImages(0.8, [imgContourDraw, imgCanny])
cannyTrackbar()
cv2.destroyAllWindows()