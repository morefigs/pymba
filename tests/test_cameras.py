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
            system.run_feature_command("GeVDiscoveryAllOnce")
            time.sleep(0.2)

        cameraIds = vimba.getCameraIds()
        for cameraId in cameraIds:
            print('Camera ID:', cameraId)

        # get and open a camera
        camera0 = vimba.getCamera(cameraIds[0])
        camera0.open()

        # list camera features
        cameraFeatureNames = camera0.get_feature_names()
        for name in cameraFeatureNames:
            print('Camera feature:', name)

        # get the value of a feature
        print(camera0.AcquisitionMode)

        # set the value of a feature
        camera0.AcquisitionMode = 'SingleFrame'

        # create new frames for the camera
        frame0 = camera0.create_frame()  # creates a frame
        frame1 = camera0.create_frame()  # creates a second frame

        # announce frame
        frame0.announce()

        # capture a camera image
        camera0.start_capture()
        frame0.queue_capture()
        camera0.run_feature_command('AcquisitionStart')
        camera0.run_feature_command('AcquisitionStop')
        frame0.wait_capture()

        # get image data...
        imgData = frame0.get_buffer()

        # ...or use NumPy for fast image display (for use with OpenCV, etc)
        import numpy as np

        moreUsefulImgData = np.ndarray(buffer=frame0.get_buffer(),
                                       dtype=np.uint8,
                                       shape=(frame0.height,
                                              frame0.width,
                                              1))

        # clean up after capture
        camera0.end_capture()
        camera0.revoke_all_frames()

        # close camera
        camera0.close()


if __name__ == '__main__':
    test_cameras()