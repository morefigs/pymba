# pymba

pymba is a Python wrapper for the Allied Vision Technologies (AVT) Vimba C API. It wraps the VimbaC.dll file included in the AVT Vimba installation to provide a simple Python interface for AVT cameras. It currently supports most of the functionality provided by VimbaC.dll for 1394 cameras.

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

### Testing installation 

If Vimba and pymba are installed correctly, then the following code should give the installed Vimba version. No camera is needed.

	from vimba import *
	
	vimba = Vimba()
	vimba.getVersion()
	
### Basic usage

The following code gives an example of basic usage. For clarity exceptions are not dealt with here.

	from vimba import *
	
	#### start Vimba
	vimba = Vimba()
	vimba.startup()
	
	#### show Vimba version
	print vimba.getVersion()
	
	#### list available camera IDs
	camIds = vimba.getCameraIds()
	for cam in camIds:
		print cam
	
	#### create and open a camera
	cam0 = vimba.getCamera(camIds[0])
	cam0.openCamera()
	
	#### list features of a camera
	featNames = cam0.getFeatureNames()
	for fn in featNames:
		print fn
	
	#### read info of a camera feature
	featInfo = cam0.getFeatureInfo('AcquisitionMode')
	for field in featInfo.getFieldNames():
		print field, '--', getattr(featInfo, field)
	
	#### get the value of a feature
	print cam0.AcquisitionMode
	
	#### set the value of a feature
	cam0.AcquisitionMode = 'SingleFrame'
	
	#### create new frames for the camera
	frame0 = cam0.getFrame()	# creates a frame
	frame1 = cam0.getFrame()	# creates a second frame
	
	#### announce frame
	frame0.announceFrame()
	
	#### capture a camera image
	cam0.startCapture()
	frame0.queueFrameCapture()
	cam0.runFeatureCommand('AcquisitionStart')
	cam0.runFeatureCommand('AcquisitionStop')
	frame0.waitFrameCapture()
	
	#### get image data...
	imgData = frame0.getBufferByteData()
	
	#### ...or use NumPy for fast image display (for use with OpenCV, etc)
	import numpy as np
	moreUsefulImgData = np.ndarray(buffer = cam0.frame0.getBufferByteData(),
								   dtype = np.uint8,
								   shape = (cam0.frame0.height,
											cam0.frame0.width,
											1))
	
	#### clean up after capture
	cam0.endCapture()
	cam0.revokeAllFrames()
	
	#### close camera
	cam0.closeCamera()
	
	#### shutdown Vimba	
	vimba.shutdown()
	
	
	


	

### Handling Vimba exceptions

Handling exceptions can be done as shown below.

	from vimba import *

	try:
		vimba = Vimba()
		vimba.startup()
	except VimbaException as e:
		print e.message



## Known issues

* Not all SDK functions are wrapped (most are). For full list see vimbadll.py.
* Colour cameras have not been tested. B&W 1394 cameras have been tested under Windows with Vimba version 1.2.1.
* The VimbaC.dll file location has been hardcoded in vimbadll.py. It should be easy to change if needed.

