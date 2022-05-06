import cv2
import time
from CannyEdgeDetection import CannyEdgeDetection
import os

# This is the driver program for the Spray Quality monitor for informed pesticide applications. This program
# will analyze a series of photos with the canny edge detection algorithm to identify droplets and display
# the spray quality in the form of a pie chart.
#
# Original Author: Gabriel St. Jean
# Email: gjustinst.jean@gmail.com
# Date: 5/1/22

pictureFolderPath = "C:/Users/jeans/Documents/photos/"
videoPath = "C:/Users/jeans/Documents/Videos/manPunching.mp4"

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
    #           the spray quality in the form of a pie chart.
    # Precondition: The class variable `showPieViewer` is set to true.
    def analyzePhotos(self):
        count = 1
        while True:
            if (count > 10):
                count = 1
            imgPath = pictureFolderPath + "teststand{}.jpg".format(count)
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

    # Function: Performs canny contour detection to identify spray droplets on each frame of a video file and displays
    #           the spray quality in the form of a pie chart.
    # Precondition: The class variable `showPieViewer` is set to true.
    def analyzeVideo(self):
        videoStream = cv2.VideoCapture(videoPath)
        currentFrame = 0
        success = True
        # 1000/ delayTime = FPS. Does not account for the delay caused from computations in the program.
        delayTime = 11

        # Location to save image frames
        if not os.path.exists("resources/videoCanny"):
            os.makedirs("resources/videoCanny")

        while (True):
            try:
                success, frame = videoStream.read()
                self.createContourMap(frame, 50, 50)
                self.findContours()
                imgStack = self.imageFormatter.stackImages(1, ([self.imgBoundingBox, self.imgContourMap]))
                cv2.imshow("Canny Detection", imgStack)
                # Store image frame as an image in a file
                #cv2.imwrite("./resources/VideoCanny" + str(currentFrame) + ".jpg", imgStack)
                currentFrame += 1
                k = cv2.waitKey(delayTime) & 0xFF
                if (k == 27):  # If the escape key is pressed, end loop
                    break
                self.pixelsPerIn = -1
                self.areaList.clear()
            except:
               videoStream = cv2.VideoCapture(videoPath)


## Entry point into the program ##
sprayQualityDriver = SprayQualityDriver()
#sprayQualityDriver.analyzeVideo()
sprayQualityDriver.analyzePhotos()
cv2.destroyAllWindows()
