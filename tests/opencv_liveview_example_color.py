# -*- coding: utf-8 -*-
"""
Created on Mon Jul 07 14:59:03 2014

@author: derricw

Same as the other liveview example, but displays in color.

Obviously you want to use a camera that has a color mode like BGR8Packed

OpenCV is expecting color images to be in BGR8Packed by default.  It can work
    with other formats as well as convert one to the other, but this example
    just uses its default behavior.

"""
from __future__ import absolute_import, print_function, division
from pymba import *
import numpy as np
import cv2
import time
import sys

cv2.namedWindow("test")

with Vimba() as vimba:
    system = vimba.getSystem()

    system.run_feature_command("GeVDiscoveryAllOnce")
    time.sleep(0.2)

    camera_ids = vimba.getCameraIds()

    for cam_id in camera_ids:
        print("Camera found: ", cam_id)

    c0 = vimba.getCamera(camera_ids[0])
    c0.open()

    try:
        #gigE camera
        print("Packet size:", c0.GevSCPSPacketSize)
        c0.StreamBytesPerSecond = 100000000
        print("BPS:", c0.StreamBytesPerSecond)
    except:
        #not a gigE camera
        pass

    #set pixel format
    c0.PixelFormat = "BGR8Packed"  # OPENCV DEFAULT
    time.sleep(0.2)

    frame = c0.create_frame()
    frame.announce()

    c0.start_capture()

    framecount = 0
    droppedframes = []

    while 1:
        try:
            frame.queue_capture()
            success = True
        except:
            droppedframes.append(framecount)
            success = False
        c0.run_feature_command("AcquisitionStart")
        c0.run_feature_command("AcquisitionStop")
        frame.wait_capture(1000)
        frame_data = frame.get_buffer()
        if success:
            img = np.ndarray(buffer=frame_data,
                             dtype=np.uint8,
                             shape=(frame.height, frame.width, frame.pixel_bytes))
            cv2.imshow("test", img)
        framecount += 1
        k = cv2.waitKey(1)
        if k == 0x1b:
            cv2.destroyAllWindows()
            print("Frames displayed: %i" % framecount)
            print("Frames dropped: %s" % droppedframes)
            break


    c0.end_capture()
    c0.revoke_all_frames()

    c0.close()

