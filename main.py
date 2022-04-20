
import cv2
from PieViewer import PieViewer
from ExtractSprayQuality import ExtractSprayQuality
import time
from ImageFormater import ImageFormater

# Conversion
US_QUARTER = .71 # in inches
IN_TO_MICRON = 25400
pixelsPerIn = -1

# Reference to draw water droplet contours on
imgDropletDraw = None

# Other
imageFormater = ImageFormater()
pieViewer = PieViewer()
extractSprayQuality = ExtractSprayQuality()
finishedAreaListFlag = False
areaList = []

def analyzePhoto():
    global areaList
    global imgDropletDraw

    photoPath = "C:/Users/jeans/Documents/photos/"

    for i in range(1, 10):
        filePath = photoPath + "teststand{}.jpg".format(i)
        img = cv2.imread(filePath)
        dimension = (int(img.shape[1] * 9 / 100), int(img.shape[0] * 9 / 100))
        img = cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)
        print(filePath)

        # Canny Edge Detection
        gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)  # Needed to turn imag
        GaussianBlur = cv2.GaussianBlur(gray, (5, 5), 0)  # To remove noise and imp
        imgCanny = cv2.Canny(GaussianBlur, 63, 69)

        # Drawing contours
        imgDropletDraw = img.copy()
        findContoursCanny(imgDropletDraw, imgCanny)
        if len(areaList) == 0:
            continue
        cv2.imshow("Canny Detection", imgDropletDraw)
        formatedStr = extractSprayQuality.getFormatedString(areaList)
        pieViewer.displayFormatedList(formatedStr)
        time.sleep(4.5)
        areaList.clear()

def findContoursCanny(imgToDrawOn, inputImage):
    global pixelsPerIn
    global imgDropletDraw
    global areaList

    (contours, _) = cv2.findContours(inputImage, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Make the largest area (the US quarter) located at the first index
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Calibration: Obtain the area of the quarter in pixels
    if (pixelsPerIn == -1):
        pixelsPerIn = cv2.contourArea(contours[0])/US_QUARTER

    # Shape Identification
    for i in range(1, len(contours)):
        pixelArea = cv2.contourArea(contours[i])
        # Identifying shape of a contour
        arcLength = cv2.arcLength(contours[i], True)
        # Approximates contour shape (since shapes can be irregular)
        cornerPoints = cv2.approxPolyDP(contours[i], .01 * arcLength, True)
        objectCorners = len(cornerPoints)

        # upper bound is 762 microns and the lower bound is 40 microns to remove noise
        upperBound = .03 * pixelsPerIn
        lowerBound = .0011 * pixelsPerIn

        # Filter out shapes that are not a circle and other noise
        if (pixelArea > lowerBound and pixelArea < upperBound and objectCorners > 4):
            # Finding the area of each contour
            transferFunction = pixelArea / pixelsPerIn * IN_TO_MICRON # Convert from pixel area into inches
            areaList.append(transferFunction)
            # Draw bounding boxes with the area of each object
            x, y, w, h = cv2.boundingRect(cornerPoints) # x cord, y, cord, width, and height
            cv2.rectangle(imgDropletDraw, (x,y), (x+w, y+h), (0, 255, 0), 2)
            areaString = "{area: .2f} um"
            cv2.putText(imgDropletDraw, areaString.format(area = transferFunction),
                    (int(x + (w / 2) - 10), int(y + (h / 2) - 19)),
                    cv2.FONT_HERSHEY_COMPLEX,0.5, (0, 0, 0), 0)

## Entry point into the program
analyzePhoto()
