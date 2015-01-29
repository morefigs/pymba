=======
pymba
=======

pymba is a Python wrapper for the Allied Vision Technologies (AVT) Vimba C API. It wraps the VimbaC.dll file included in the AVT Vimba installation to provide a simple Python interface for AVT cameras. It currently supports most of the functionality provided by VimbaC.dll.

Installation
============

* Install the Vimba SDK from AVT to the default directory.

* Run the AVTDriverInstaller tool and install the AVT Vimba SDK drivers.

* Install pymba.

Usage
=====

Testing installation
--------------------

If Vimba SDK and pymba are installed correctly, then the following code should give the installed Vimba version. No camera is needed.

	from pymba import *
	
	with Vimba() as vimba:
	    print vimba.getVersion()
	
Interacting with cameras
------------------------

Discover, open, manipulate, and capture frames from a camera.
    
    from pymba import *
    import time
    
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
            print 'Camera ID:', cameraId
        
        # get and open a camera
        camera0 = vimba.getCamera(cameraIds[0])
        camera0.openCamera()
        
        # list camera features
        cameraFeatureNames = camera0.getFeatureNames()
        for name in cameraFeatureNames:
            print 'Camera feature:', name
        
        # get the value of a feature
        print camera0.AcquisitionMode
        
        # set the value of a feature
        camera0.AcquisitionMode = 'SingleFrame'
        
        # create new frames for the camera
        frame0 = camera0.getFrame()    # creates a frame
        frame1 = camera0.getFrame()    # creates a second frame
        
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
        moreUsefulImgData = np.ndarray(buffer = frame0.getBufferByteData(),
                                       dtype = np.uint8,
                                       shape = (frame0.height,
                                                frame0.width,
                                                1))
        
        # clean up after capture
        camera0.endCapture()
        camera0.revokeAllFrames()
        
        # close camera
	
Interacting with the Vimba system
---------------------------------
    
Get a reference to the Vimba system object and list available system features.
    
    from pymba import *
    
    with Vimba() as vimba:
        # get system object
        system = vimba.getSystem()
        
        # list system features
        for featureName in system.getFeatureNames():
            print 'System feature:', featureName
        

Interacting with transport layer interfaces
-------------------------------------------
    
Get a reference to an interface object and list available interface features.
    
    from pymba import *
    
    with Vimba() as vimba:
        # get list of available interfaces
        interfaceIds = vimba.getInterfaceIds()
        for interfaceId in interfaceIds:
            print 'Interface ID:', interfaceId
        
        # get interface object and open it
        interface0 = vimba.getInterface(interfaceIds[0])
        interface0.openInterface()
        
        # list interface features
        interfaceFeatureNames = interface0.getFeatureNames()
        for name in interfaceFeatureNames:
            print 'Interface feature:', name
        
        # close interface
        interface0.closeInterface()

Handling Vimba exceptions
-------------------------

	from pymba import *

	try:
	    with Vimba() as vimba:
	except VimbaException as e:
	    print e.message

Known issues
============

* Not all API functions are wrapped (most are). For full list see vimbadll.py.
* Only 32-bit VimbaC.dll (version 1.2.1) under Windows has been tested.
* Colour cameras and GigE cameras have not been tested.
* The VimbaC.dll file location has been hardcoded in vimbadll.py. It should be easy to change if needed.

