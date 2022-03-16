# Airborne-Spray-Analysis
This program utilizes the OpenVINO toolkit and the Intel Movidus Neural Compute stick 2 to perferm real-time analyis of pesticide practicles captured from a pi HQ camera.

## Setup
1. The Intel Movidus Neural Compute stick 2 must be inserted into the USB 3.0 slot of the slot  raspberry pi prior to program execution
2. A pi camera module must be attached to the CSCI port of the raspberry pi. This application utilizes the pi HQ camera with a 50  mm telephot lens.

## Calibrate Pi Camera Module
The `PiCamCalibrate.py` program in the [Calibrate](./Calibrate) folder is used to calibrate the camera module attached
to the raspberry pi so that the user can adjust camera settings by the use
of a camera preview.

## Create randomized Spray Dataset
The `GenerateSprayDataset.py` program location in the [dummyDataset](./dummyDataset) folder contains a program that generates random particle size distrubtions of a pesticide spray in a file named `sprayDataset`. These values are used as an input in `PieViewer.py` to debug the program.

## Real-time Spray Quality Analysis
The`PieViewer.py` program  parses through a file containing the distribution  of various particle types so that a real-time analysis of the changes in spray quality distribution can be visualized on a line-by-line basis.