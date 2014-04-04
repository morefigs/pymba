from pymba import *
import numpy as np
import cv2
import time

#very crude example, assumes your camera is PixelMode = BAYERRG8

# start Vimba
vimba = Vimba()
vimba.startup()

# get system object
system = vimba.getSystem()

# list available cameras (after enabling discovery for GigE cameras)
if system.GeVTLIsPresent:
    print("GeVTLIsPresent")
    system.runFeatureCommand("GeVDiscoveryAllOnce")
    time.sleep(0.2)
else:
    print ("No GeVTL")
cameraIds = vimba.getCameraIds()
for cameraId in cameraIds:
    print 'Camera ID:', cameraId

# get and open a camera
camera0 = vimba.getCamera(cameraIds[0])
camera0.openCamera()

# list camera features
cameraFeatureNames = camera0.getFeatureNames()
for name in cameraFeatureNames:
    try:
    	print 'Camera feature:%s=%s' % (name, camera0.__getattr__(name))
	pass
    except VimbaException:
	print "%s Not yet implemented" % name
	pass

# read info of a camera feature
#featureInfo = camera0.getFeatureInfo('AcquisitionMode')
#for field in featInfo.getFieldNames():
#    print field, '--', getattr(featInfo, field)

# get the value of a feature
print "AcquisitionMode is"
print camera0.AcquisitionMode
print camera0.ExposureMode

# set the value of a feature
print "Setting acquisition mode"

#camera0.AcquisitionMode = 'Continuous'
camera0.__setattr__("AcquisitionModeCCC", 'SingleFrame')
try:
    camera0.AcquisitionModeJJJ = 'JJJ'
    print "Got in here"
except Exception:
    print "Failed to set JJJ"
print camera0.AcquisitionMode

# create new frames for the camera

frame0 = camera0.getFrame()    # creates a frame
frame1 = camera0.getFrame()    # creates a second frame

# announce frame
frame0.announceFrame()

# capture a camera image
count = 0
while count < 10:
    camera0.startCapture()
    camera0.runFeatureCommand('AcquisitionStart')

    frame0.queueFrameCapture()
    frame0.waitFrameCapture()

    camera0.runFeatureCommand('AcquisitionStop')

    # get image data...
    imgData = frame0.getBufferByteData()
    
    moreUsefulImgData = np.ndarray(buffer = frame0.getBufferByteData(),
                                   dtype = np.uint8,
                                   shape = (frame0.height,
                                            frame0.width,
                                            1))
    rgb = cv2.cvtColor(moreUsefulImgData, cv2.COLOR_BAYER_RG2RGB)
    cv2.imwrite('foo{}.png'.format(count), rgb)
    print "image {} saved".format(count)
    count += 1
    camera0.endCapture()
# clean up after capture
camera0.revokeAllFrames()

# close camera
camera0.closeCamera()

# shutdown Vimba
vimba.shutdown()

