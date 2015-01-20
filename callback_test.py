from pymba import *
import time, Queue
import numpy as np

# start Vimba
vimba = Vimba()
vimba.startup()

# get system object
system = vimba.getSystem()

# list available cameras (after enabling discovery for GigE cameras)
if system.GeVTLIsPresent:
    system.runFeatureCommand("GeVDiscoveryAllOnce")
    time.sleep(0.2)
cameraIds = vimba.getCameraIds()

# get and open a camera
camera0 = vimba.getCamera(cameraIds[0])
camera0.openCamera()

# set the value of a feature
camera0.AcquisitionMode = 'Continuous'
camera0.BinningHorizontal = camera0.BinningVertical = 4
camera0.ExposureTimeAbs = 5000
fr = camera0.AcquisitionFrameRateAbs = camera0.AcquisitionFrameRateLimit

# get ready to capture
T = 10.0
camera0.startCapture()

# define a callback
frame_q = Queue.Queue()

def mycb(frame):
    img = np.ndarray(buffer=frame.getBufferByteData(),
                     dtype=np.uint8,
                     shape=(frame.height, frame.width))
    frame_q.put(img)
    frame.queueFrameCapture(mycb)

# create new frames for the camera
frames = [camera0.getFrame() for _ in xrange(5)]
for frame in frames:
    frame.announceFrame()
    frame.queueFrameCapture(frameCallback=mycb)

try:
    print "starting"
    camera0.runFeatureCommand('AcquisitionStart')
    time.sleep(T)
    camera0.runFeatureCommand('AcquisitionStop')
    print "done"
    time.sleep(0.5)

    # clean up after capture
    camera0.endCapture()
    camera0.revokeAllFrames()

except Exception as e:
    raise e

finally:
    # close camera
    camera0.closeCamera()

    # shutdown Vimba
    vimba.shutdown()

print "target frame rate: %2.2ffps" % fr
print "achieved frame rate: %2.2ffps" % (frame_q.qsize() / T, )

import matplotlib.pyplot as plt
plt.imshow(frame_q.get())
plt.show()
