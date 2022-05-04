import numpy as np
import cv2
from PieViewer import PieViewer
from ExtractSprayQuality import ExtractSprayQuality
from ImageFormatter import ImageFormatter

# This class uses the Canny Edge Detection map to identify water droplets in an image to produce a new image
# that contains bounding boxes or contours around them. Water droplets are then classified into spray particle
# types such as fine, medium, or coarse based on its area measurement. For the algorithm to work, a contour map
# of an image must first be created and then processed by the `findContours` function to filter out contours
# that are droplets to the best of the programs capabilities. Within the function, a droplet is identified
# as any object that has more than four corner points and has an area measurement within the spray quality
# range of the Spray Quality Monitor. The final output of the program creates bounding boxes around these droplets
# in the `imgBoundingBox` variable and the outlines of the contours onto the original in `imgContourDraw`.
#
# Within the program, the user has several customization options for how the program will be implemented:
#    1) dilateAndErodeImages - Performs dilation and erosion on the edge map to remove noise and to join
#                              disparate elements. Since droplets in this application are miniscule, this feature
#                              may cause noise in the application by clustering neighboring droplets as a single
#                              contour.
#    2) showImgMeasurement - Displays the area measurement of all droplets in microns.
#    3) showPieViewer - Serves as a visualization aid to monitor the spray quality of the application by outputting
#                       the particle size distribution and its VMD value. The feature utilizes the `PieViewer` class.
#    4) showContourLen - Displays the number of detected contours on the contour map and final output image
#    5) showDebugOutput - Displays the pixel area of a contour alongside its area in inches and microns on the
#                         console.
#
# For correct measurement functionality, ensure that a U.S. quarter is used as a reference object
# in the image. Verify that the transfer function is working properly by obtaining .71 inches for the coin
# in the console. To achieve this, remove the upper bound in `findContours`, set the range of the for
# loop in `findContours` from 1 to 0 in the lower bound section, and enable `showDebugOutput` in the
# child class. The coin should appear as i = 0 in the console.

# Conversion
US_QUARTER = .71 # in inches
IN_TO_MICRON = 25400

# Other
pieViewerWidth = 9
pieViewerHeight = 5

class CannyEdgeDetection:

    # Function: Constructor of the class
    def __init__(self, dilateAndErodeImage, showImgMeasurement, showPieViewer, showContourLen, showDebugOutput):
        self.dilateAndErodeImage = dilateAndErodeImage
        self.showImgMeasurement = showImgMeasurement
        self.showPieViewer = showPieViewer
        self.showContourLen = showContourLen
        self.showDebugOutput = showDebugOutput
        # Initializing images
        self.img = None
        self.imgContourMap = None  # Contains a map of contours of `img`
        self.imgBoundingBox = None  # Contains bounding boxes drawn around images
        self.imgContourDraw = None  # Contains contours drawn around images
        # Canny Edge Detection parameters
        self.minValue = 70
        self.maxValue = 122
        self.sigma = 5  # can be only 5 or 3
        self.iterationNum = 2
        # Other
        self.extractSprayQuality = ExtractSprayQuality()
        self.pieViewer = PieViewer()
        self.areaList = []  # Contains the micron measurement of contours that fit a criteria
        self.pixelsPerIn = -1
        self.imageFormatter = ImageFormatter()

    # Function: Modifies the dimensions of the pie chart window.
    #
    # @param width - The desired width of the pie chart window.
    # @param height - The desired height of the pie chart window.
    def modifyPieViewerDimensions(self, width, height):
        global pieViewerWidth
        global pieViewerHeight

        pieViewerWidth = width
        pieViewerHeight = height

    # Function: Creates a spray quality pie chart based on the values within `areaList`.
    # Precondition: The boolean class variable `showPieViewer` is enabled.
    def viewPieChart(self):
        global pieViewerWidth
        global pieViewerHeight

        formatedString = self.extractSprayQuality.getFormatedString(self.areaList)
        self.pieViewer.displayFormatedList(formatedString, pieViewerWidth, pieViewerHeight)

    # Function: Creates a contour map of an image using Canny edge detection
    # Postcondition: An image containing the contour map of the original is produced
    #
    # @param img - the image to obtain a contour map of.
    # @param windowWidthScaler - the scaled width of `img`.
    # @param windowHeightScaler - the scaled height of `img`.
    def createContourMap(self, img, windowWidthScaler=7, windowHeightScaler=7):
        self.img = img
        # Resizing image
        dimension = (int(self.img.shape[1] * windowWidthScaler/ 100),
                     int(self.img.shape[0] * windowHeightScaler/ 100))  # (width, height)
        self.img = cv2.resize(self.img, dimension, interpolation=cv2.INTER_AREA)
        grayScaleImg = cv2.cvtColor(self.img.copy(), cv2.COLOR_BGR2GRAY)
        GaussianBlur = cv2.GaussianBlur(grayScaleImg, (self.sigma, self.sigma), 0)  # Removes noise
        self.imgContourMap = cv2.Canny(GaussianBlur, self.minValue, self.maxValue)
        # Used to enhance the contour map by creating smoother lines
        if (self.dilateAndErodeImage == True):
            kernel = np.ones((3, 3))
            imgDial = cv2.dilate(self.imgContourMap, kernel, iterations=self.iterationNum)
            imgThre = cv2.dilate(imgDial, kernel, iterations=self.iterationNum)
            self.imgContourMap = imgThre.copy()

    # Function: Finds detected contours defined by a criteria.
    # Precondition: The contour map of the variable `img` is generated in `imgContourMap`.
    # Postcondition: A contour map of an image used to produce a new image containing bounding
    #                boxes around contours in `imgBoundingBox` and outlines of the contours
    #                in `imgContourDraw`. The `areaList` variable is updated to contain the micron
    #                measurement of contours that fit a criteria.
    #
    # Complexity: O(N)
    def findContours(self):
        self.imgBoundingBox = self.img.copy()
        self.imgContourDraw = self.img.copy()
        # Obtain an array of pixel coordinates that defines each contour in the map
        (contours, _) = cv2.findContours(self.imgContourMap, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Make the largest area (the US quarter) located at the first index
        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        # Calibration: Obtain the area of the quarter in pixels
        if (self.pixelsPerIn == -1):
            self.pixelsPerIn = cv2.contourArea(contours[0]) / US_QUARTER

        # To show the area of the coin, make i = 0 and remove the upper bound
        for i in range(1, len(contours)):
            # Measures the area of the contour
            pixelArea = cv2.contourArea(contours[i])

            # Identifying shape of a contour
            arcLength = cv2.arcLength(contours[i], True)
            # Approximates contour shape (since shapes can be irregular)
            cornerPoints = cv2.approxPolyDP(contours[i], .01 * arcLength, True)
            objectCorners = len(cornerPoints)

            # upper bound is 1016 microns and the lower bound is 27 microns to remove noise
            upperBound = .04 * self.pixelsPerIn  # .04 inches = 1016 microns
            lowerBound = .0011 * self.pixelsPerIn  # .0011 inches = 27 microns

            areaString = "{area: .2f} um"  # formating
            areaStringIn = "{area: .2f} in"  # formating

            # Filter out shapes that are not a circle and other noise
            if (pixelArea > lowerBound and pixelArea < upperBound and objectCorners > 4):
                transferFunction = pixelArea / self.pixelsPerIn * IN_TO_MICRON  # Convert from pixel area into inches
                self.areaList.append(transferFunction)
                if (self.showDebugOutput == True):
                    print("i=" + str(i) + ", Pixel area : " + str(pixelArea) +
                          ", Area in inches: " + areaStringIn.format(area=transferFunction / IN_TO_MICRON) +
                          ", Area in microns: " + areaString.format(area=transferFunction) +
                          ", corner points: " + str(objectCorners))

                # Draw bounding boxes with the area of each object
                x, y, w, h = cv2.boundingRect(cornerPoints)  # x cord, y, cord, width, and height
                cv2.rectangle(self.imgBoundingBox, (x, y), (x + w, y + h), (0, 255, 0), 2)
                if (self.showImgMeasurement == True):
                    cv2.putText(self.imgBoundingBox, areaString.format(area=transferFunction),
                                (int(x + (w / 2) - 10), int(y + (h / 2) - 19)), cv2.FONT_HERSHEY_COMPLEX,
                                0.5, (0, 0, 0), 0)

        if (self.showPieViewer == True):
            self.viewPieChart()

        if (self.showContourLen == True):
            cv2.putText(self.imgContourMap, "Contours: " + str(len(contours)),
                        (int(self.imgContourMap.shape[0] - self.imgContourMap.shape[0] / 1.05),
                         int(self.imgContourMap.shape[1] - self.imgContourMap.shape[1] / 2.7)),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 100), 0)
            cv2.putText(self.imgBoundingBox, "Contours: " + str(len(self.areaList)),
                        (int(self.imgContourMap.shape[0] - self.imgContourMap.shape[0] / 1.05),
                         int(self.imgContourMap.shape[1] - self.imgContourMap.shape[1] / 2.7)),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 100), 0)
            cv2.putText(self.imgContourDraw, "Contours: " + str(len(self.areaList)),
                        (int(self.imgContourMap.shape[0] - self.imgContourMap.shape[0] / 1.05),
                         int(self.imgContourMap.shape[1] - self.imgContourMap.shape[1] / 2.7)),
                        cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 100), 0)
        cv2.drawContours(self.imgContourDraw, contours, -1, (255, 0, 0), 4)  # Draw all contours
