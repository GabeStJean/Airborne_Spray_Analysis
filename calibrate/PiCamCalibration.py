from time import sleep
from picamera import PiCamera
import atexit
from fractions import Fraction
import datetime
import time

# This program is utilzed to calibrate a pi camera module attached to the CSCI port of the
# microcontroller.

camera = PiCamera()
camera.resolution = (1024, 768) # (1024, 768) (2592, 1944)
# 6000000 microseconds is thes slowest shutter speed
# 1 unit = 1 microseconds
camera.shutter_speed = 1000
camera.flash_mode = 'on'
camera.exposure_mode="sports"
camera.iso = 200
camera.start_preview()

#camera.rotation = 180
input("Press any key to take photo ...")

try:
    #Captures image and saves to path
    camera.capture('../images/foo.jpg', format='jpeg', use_video_port=True)
finally:
    camera.close()