import cv2
from ImageFormater import ImageFormater
import time

# This program adds a trackbar to find the optimal parameters for the binary
# image preprocessing for threshold based contour detection.

# Reading Image
photoPath = "C:/Users/jeans/Documents/photos/"
img = cv2.imread(photoPath + "/teststand1.jpg")

# Resizing
dimension = (int(img.shape[1] * 10 / 100), int(img.shape[0] * 10 / 100))
img = cv2.resize(img, dimension, interpolation=cv2.INTER_AREA)

# Default thresholding contour detection values for an image
thresh = 41
maxval = 255
contoursThresh = ("")

# Function: Updates the thresh value for threshold contour detection
# Precondition: The thresh slider is modified when thresholdTrackbar() is invoked
def updateThresh(value):
    global thresh
    thresh = value

# Function: Updates the thresh value when the corresponding slider is used in thresholdTrackbar()
# Precondition: The maxval slider is modified when thresholdTrackbar() is invoked
def updateMaxValue(value):
    global maxval
    maxval = value

# Function: Draws contours on the original image
# Postcondition: The imgThreshContourDraw variable stores image with contour drawing.
def findContoursThreshold():
    global imgBinary
    global imgThreshContourDraw

    imgThreshContourDraw = img.copy()
    #cv2.RETR_LIST
    (contoursBinary, hiearchy) = cv2.findContours(imgBinary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(len(contoursBinary)) # Make sure contours are accurate
    cv2.drawContours(imgThreshContourDraw, contoursBinary, -1, (0, 0, 255), 2)

# Function: Allows the user to find optimal thresh and maxval parameters by the use of a
#           trackbar.
def thresholdTrackbar():
    global imgStackThresh
    global imgThreshContourDraw
    global imgBinary
    global thresh
    global maxval

    # Creating the trackbar
    cv2.namedWindow("Binary Image Threshold")  # Binds the trackbar and image window
    cv2.createTrackbar('thresh', "Binary Image Threshold", thresh, 255, updateThresh)
    cv2.createTrackbar('maxval', "Binary Image Threshold", maxval, 255, updateMaxValue)
    while (1):
        imgStackThresh = imageFormater.stackImages(0.8, ([imgThreshContourDraw, imgBinary]))
        cv2.imshow("Binary Image Threshold", imgStackThresh)
        k = cv2.waitKey(1) & 0xFF  # window refresh rate in seconds
        if k == 27:  # If the escape key is pressed, end loop
            break
        _, imgBinary = cv2.threshold(grayInverted, thresh, maxval, cv2.THRESH_BINARY)
        findContoursThreshold()
        time.sleep(.5)


# Thresholding based contour detection
gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)     # converting to gray scale
grayInverted = cv2.bitwise_not(gray)                    # Invert colors for contours to be drawn on outlines

# Create a binary image
_, imgBinary = cv2.threshold(grayInverted, thresh, maxval, cv2.THRESH_BINARY)

# finding contours
imgThreshContourDraw = img.copy()
findContoursThreshold()
imageFormater = ImageFormater()
imgStackThresh = imageFormater.stackImages(0.8, ([imgThreshContourDraw, imgBinary]))
thresholdTrackbar()
cv2.destroyAllWindows()
