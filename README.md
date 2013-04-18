# pymba

pymba is a Python wrapper for the Allied Vision Technologies (AVT) Vimba C API. It wraps (and requires) the VimbaC.dll file included in the AVT Vimba installation. It currently supports most of the functionality provided by VimbaC.dll for 1394 cameras.

## Installation

Install the Vimba SDK from AVT to the default directory, and install at least:

	- AVT 1394 Transport Layer
	 └ Core components
	- AVT Vimba SDK
	 └ Core components
	 └ C API runtime components
	 └ Driver Installer

Run the AVTDriverInstaller tool and install the AVT Vimba SDK drivers.

Install pymba.

## Usage

### Typical usage

The following code gives a good example of basic pymba usage. For clarity exceptions are not dealt with.

	from vimba import *
	
	# start Vimba
	vimba = Vimba()
	vimba.startup()
	
	# show Vimba version
	print '\nVimba API version\n------'
	print vimba.getVersion()
	
	# list available camera IDs
	camIds = vimba.getCameraIds()
	print '\nAvailable cameras\n------'
	for cam in camIds:
		print cam
	
	# create and open a camera
	cam0 = vimba.getCamera(camIds[0])
	cam0.openCamera()
	
	# list features of a camera
	featNames = cam0.getFeatureNames()
	print '\nAvailable features for camera', cam0.cameraIdString, '\n------'
	for fn in featNames:
		print fn
	
	# read info of a camera feature
	featInfo = cam0.getFeatureInfo('AcquisitionMode')
	print '\nProperties for feature', featInfo.name, 'on camera', cam0.cameraIdString, '\n------'
	for field in featInfo.getFieldNames():
		print field, '--', getattr(featInfo, field)
	
	# get the value of a feature
	print '\nValue of feature', featInfo.name, 'on camera', cam0.cameraIdString, '\n------'
	print cam0.AcquisitionMode
	
	# set the value of a feature
	cam0.AcquisitionMode = 'SingleFrame'
	
	# create new frames for the camera
	frame0 = cam0.getFrame()	# creates a frame
	frame1 = cam0.getFrame()	# creates a second frame
	
	# announce frame
	frame0.announceFrame()
	
	# capture a camera image
	cam0.startCapture()
	frame0.queueFrameCapture()
	cam0.runFeatureCommand('AcquisitionStart')
	cam0.runFeatureCommand('AcquisitionStop')
	frame0.waitFrameCapture()
	
	# get image data
	imgData = frame0.getBufferByteData()
	
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

	from vimba import *

	try:
		vimba = Vimba()
		vimba.startup()
	except VimbaException as e:
		print e.message
