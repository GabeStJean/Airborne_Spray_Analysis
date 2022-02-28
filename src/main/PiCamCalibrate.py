from time import sleep
from picamera import PiCamera

# This module is used for calibrating the focal length and apperature
# of the pi camera lens for a desired image quality during runtime.

camera = PiCamera()
camera.resolution = (2592, 1944) # (1024, 768)
camera.start_preview()

#camera.rotation = 180

sleep(2000)
try:
    camera.capture('../../images/foo.jpg') #Captures image and saves to path
finally:
    camera.close()
