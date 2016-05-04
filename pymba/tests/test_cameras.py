#!/usr/bin/python
from __future__ import absolute_import, print_function, division
from pymba import *
import time


def test_cameras():
    # start Vimba
    with Vimba() as vimba:
        # get system object
        system = vimba.getSystem()

        # list available cameras (after enabling discovery for GigE cameras)
        if system.GeVTLIsPresent:
            system.runFeatureCommand("GeVDiscoveryAllOnce")
            time.sleep(0.2)

        cameraIds = vimba.getCameraIds()
        for cameraId in cameraIds:
            print('Camera ID:', cameraId)

        # get and open a camera
        camera0 = vimba.getCamera(cameraIds[0])
        camera0.openCamera()

        # list camera features
        cameraFeatureNames = camera0.getFeatureNames()
        for name in cameraFeatureNames:
            print('Camera feature:', name)

        # get the value of a feature
        print(camera0.AcquisitionMode)

        # set the value of a feature
        camera0.AcquisitionMode = 'SingleFrame'

        # create new frames for the camera
        frame0 = camera0.getFrame()  # creates a frame
        frame1 = camera0.getFrame()  # creates a second frame

        # announce frame
        frame0.announceFrame()

        # capture a camera image
        camera0.startCapture()
        frame0.queueFrameCapture()
        camera0.runFeatureCommand('AcquisitionStart')
        camera0.runFeatureCommand('AcquisitionStop')
        frame0.waitFrameCapture()

        # get image data...
        imgData = frame0.getBufferByteData()

        # ...or use NumPy for fast image display (for use with OpenCV, etc)
        import numpy as np

        moreUsefulImgData = np.ndarray(buffer=frame0.getBufferByteData(),
                                       dtype=np.uint8,
                                       shape=(frame0.height,
                                              frame0.width,
                                              1))

        # clean up after capture
        camera0.endCapture()
        camera0.revokeAllFrames()

        # close camera
        camera0.closeCamera()


if __name__ == '__main__':
    test_cameras()