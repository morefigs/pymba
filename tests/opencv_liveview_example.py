# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 14:59:03 2014

@author: derricw
"""

from __future__ import absolute_import, print_function, division
from pymba import *
import numpy as np
import cv2
import time

cv2.namedWindow("test")

with Vimba() as vimba:
    system = vimba.getSystem()

    system.runFeatureCommand("GeVDiscoveryAllOnce")
    time.sleep(0.2)

    camera_ids = vimba.getCameraIds()

    for cam_id in camera_ids:
        print("Camera found: ", cam_id)
        
    c0 = vimba.getCamera(camera_ids[0])
    c0.openCamera()

    try:
        #gigE camera
        print(c0.GevSCPSPacketSize)
        print(c0.StreamBytesPerSecond)
        c0.StreamBytesPerSecond = 100000000
    except:
        #not a gigE camera
        pass

    #set pixel format
    c0.PixelFormat="Mono8"
    #c0.ExposureTimeAbs=60000

    frame = c0.getFrame()
    frame.announceFrame()

    c0.startCapture()

    framecount = 0
    droppedframes = []

    while 1:
        try:
            frame.queueFrameCapture()
            success = True
        except:
            droppedframes.append(framecount)
            success = False
        c0.runFeatureCommand("AcquisitionStart")
        c0.runFeatureCommand("AcquisitionStop")
        frame.waitFrameCapture(1000)
        frame_data = frame.getBufferByteData()
        if success:
            img = np.ndarray(buffer=frame_data,
                             dtype=np.uint8,
                             shape=(frame.height,frame.width,1))
            cv2.imshow("test",img)
        framecount+=1
        k = cv2.waitKey(1)
        if k == 0x1b:
            cv2.destroyAllWindows()
            print("Frames displayed: %i"%framecount)
            print("Frames dropped: %s"%droppedframes)
            break


    c0.endCapture()
    c0.revokeAllFrames()

    c0.closeCamera()
