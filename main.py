import cv2
from PieViewer import PieViewer
from ExtractSprayQuality import ExtractSprayQuality
from ImageFormater import ImageFormater
import time

# This is the driver program for the Spray Quality monitor for informed pesticide decisions. This program will
# analyze a series of photos with the canny edge detection algorithm to identify droplets and display
# their distribution in the form of a pie chart.

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
areaList = []

# Function: Performs canny contour detection to identify spray droplets on aseries of pre captured images and displays
#           the spray quality alongside the images
# Postcondition: The spray quality is shown to the user in the form of a pie chart while
def analyzePhoto():
    global areaList
    global imgDropletDraw
    global pixelsPerIn

    photoPath = "C:/Users/jeans/Documents/photos/"

    count = 1
    while True:
        if (count > 10):
            count = 1

        filePath = photoPath + "teststand{}.jpg".format(count)
        img = cv2.imread(filePath)
        dimension = (int(img.shape[1] * 9 / 100), int(img.shape[0] * 9 / 100))
        img = cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)
        print(filePath)

        # Canny Edge Detection
        gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)  # Needed to turn image gray
        GaussianBlur = cv2.GaussianBlur(gray, (5, 5), 0)  # To remove noise and imp
        imgCanny = cv2.Canny(GaussianBlur, 42, 40)

        # Drawing contours
        imgDropletDraw = img.copy()
        findContoursCanny(imgCanny)
        cv2.imshow("Canny Detection", imgDropletDraw)
        formatedStr = extractSprayQuality.getFormatedString(areaList)
        pieViewer.displayFormatedList(formatedStr)
        k = cv2.waitKey(1) & 0xFF  # window refresh rate in seconds
        if k == 27:  # If the escape key is pressed, end loop
            break
        count += 1
        pixelsPerIn = -1
        areaList.clear()
        time.sleep(1)

def findContoursCanny(inputImage):
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
    for i in range(1, len(contours)): # For each contour
        pixelArea = cv2.contourArea(contours[i]) # Green's algorithim
        # Identifying shape of a contour
        arcLength = cv2.arcLength(contours[i], True)
        # Approximates contour shape (since shapes can be irregular)
        cornerPoints = cv2.approxPolyDP(contours[i], .01 * arcLength, True)
        objectCorners = len(cornerPoints)

        # upper bound is 1016 microns and the lower bound is 27 microns for droplet spectra
        upperBound = .04 * pixelsPerIn   # .04 inches = 1016 microns
        lowerBound = .0011 * pixelsPerIn # .0011 inches = 27 microns

        # Filter out shapes that are not a circle and other noise
        if (pixelArea > lowerBound and pixelArea < upperBound and objectCorners > 4):
            # Finding the area of each contour
            transferFunction = pixelArea / pixelsPerIn * IN_TO_MICRON # Convert from pixel area into inches
            areaList.append(transferFunction)
            # Draw bounding boxes with the area of each object
            x, y, w, h = cv2.boundingRect(cornerPoints) # x cord, y, cord, width, and height
            cv2.rectangle(imgDropletDraw, (x,y), (x+w, y+h), (0, 255, 0), 2)
            areaString = "{area: .2f} um"
            #cv2.putText(imgDropletDraw, areaString.format(area = transferFunction),
            #       (int(x + (w / 2) - 10), int(y + (h / 2) - 19)),
            #       cv2.FONT_HERSHEY_COMPLEX,0.5, (0, 0, 0), 0)

## Entry point into the program
analyzePhoto()
