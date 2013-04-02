# pymba

pymba is a Python wrapper for the Allied Vision Technologies (AVT) Vimba C API. It wraps (and requires) the VimbaC.dll file included in the AVT Vimba installation.  

## Usage

### Typical usage

The following code gives a good example of basic pymba usage. For clarity exceptions are not dealt with.

	from pymba.Vimba import Vimba
	from pymba.VimbaFrame import VimbaFrame
	from pymba.VimbaCamera import VimbaCamera
	
	# start Vimba
	vimba = Vimba()
	vimba.startup()
	
	# show Vimba version
	print '\nVimba API version:'
	print '  ', vimba.getVersion()
	
	# list available camera IDs
	camIds = vimba.listCameras()
	print '\nAvailable cameras:'
	for cam in camIds:
		print '  ', cam
	
	# open a camera
	cam0 = VimbaCamera(camIds[0])
	cam0.openCamera()
	
	# list features of a camera
	featNames = cam0.listFeatures()
	print '\nAvailable features for camera', cam0.cameraIdString
	for feat in featNames:
		print '  ', feat
	
	# query a camera feature
	featName = 'Gain'
	gainFeature = cam0.queryFeature(featName)
	print '\nInformation for feature', featName, 'on camera', cam0.cameraIdString
	for k, v in gainFeature.iteritems():
		print '  ', k, '---', v
	
	# read the value of a feature
	print '\nValue of feature', featName, 'on camera', cam0.cameraIdString
	print '  ', cam0.Gain
	
	# set the value of a feature
	#cam0.Gain = 999
	
	# create a frame for a camera
	cam0.frame0 = VimbaFrame(cam0)
	cam0.frame0.announceFrame()
	
	# grab a camera image
	cam0.startCapture()
	cam0.frame0.queueFrameCapture()
	cam0.runFeatureCommand('AcquisitionStart')
	cam0.runFeatureCommand('AcquisitionStop')
	cam0.frame0.waitFrameCapture()
	imgData = cam0.frame0.getBufferByteData()
	# can use NumPy and OpenCV for faster image display
	#import numpy as np
	#import cv2
	#moreUsefulImgData = np.ndarray(buffer = cam0.frame0.getBufferByteData(),
	#							   dtype = np.uint8,
	#							   shape = (cam0.frame0.height,
	#										cam0.frame0.width,
	#										1))
	
	# clean up after capture
	cam0.endCapture()
	cam0.revokeAllFrames()
	
	# close camera
	cam0.closeCamera()
	
	# shutdown Vimba	
	vimba.shutdown()
	

### Handling Vimba exceptions

Handling exceptions can be done as shown below.

	from pymba.Vimba import Vimba
	from pymba.VimbaException import VimbaException

	try:
		vimba = Vimba()
		vimba.startup()
	except VimbaException as e:
		print e.message
