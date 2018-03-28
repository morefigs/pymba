# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import vimbastructure as structs
from .vimbaobject import VimbaObject
from .vimbaexception import VimbaException
from .vimbaframe import VimbaFrame
from .vimbadll import VimbaDLL
from ctypes import *

# camera features are automatically readable as object attributes.


class VimbaCamera(VimbaObject):

    """
    A Vimba camera object. This class provides the minimal access
    to Vimba functions required to control the camera.
    """

    @property
    def cameraIdString(self):
        return self._cameraIdString.decode()

    # own handle is inherited as self._handle
    def __init__(self, cameraIdString):

        # call super constructor
        super(VimbaCamera, self).__init__()

        # set ID
        self._cameraIdString = cameraIdString.encode()

        # set own info
        self._info = self._getInfo()

    def getInfo(self):
        """
        Get info of the camera. Does not require
        the camera to be opened.

        :returns: VimbaCameraInfo object -- camera information.
        """
        return self._info

    def _getInfo(self):
        """
        Get info of the camera. Does not require
        the camera to be opened.

        :returns: VimbaCameraInfo object -- camera information.
        """
        # args for Vimba call
        cameraInfo = structs.VimbaCameraInfo()

        # Vimba DLL will return an error code
        errorCode = VimbaDLL.cameraInfoQuery(self._cameraIdString,
                                             byref(cameraInfo),
                                             sizeof(cameraInfo))
        if errorCode != 0:
            raise VimbaException(errorCode)

        return cameraInfo

    def openCamera(self, cameraAccessMode=1):
        """
        Open the camera with requested access mode
        Available access modes:
           0 : VmbAccessModeNone 	
           1 : VmbAccessModeFull 	
           2 : VmbAccessModeRead 	
           3 : VmbAccessModeConfig 	
           4 : VmbAccessModeLite 
        """
        # args for Vimba call
        errorCode = VimbaDLL.cameraOpen(self._cameraIdString,
                                        cameraAccessMode,
                                        byref(self._handle))
        if errorCode != 0:
            raise VimbaException(errorCode)

    def closeCamera(self):
        """
        Close the camera.
        """
        errorCode = VimbaDLL.cameraClose(self._handle)
        if errorCode != 0:
            raise VimbaException(errorCode)

    def revokeAllFrames(self):
        """
        Revoke all frames assigned to the camera.
        """
        errorCode = VimbaDLL.frameRevokeAll(self._handle)
        if errorCode != 0:
            raise VimbaException(errorCode)

    def startCapture(self):
        """
        Prepare the API for incoming frames.
        """
        errorCode = VimbaDLL.captureStart(self._handle)
        if errorCode != 0:
            raise VimbaException(errorCode)

    def endCapture(self):
        """
        Stop the API from being able to receive frames.
        """
        errorCode = VimbaDLL.captureEnd(self._handle)
        if errorCode != 0:
            raise VimbaException(errorCode)

    def flushCaptureQueue(self):
        """
        Flush the capture queue.
        """
        errorCode = VimbaDLL.captureQueueFlush(self._handle)
        if errorCode != 0:
            raise VimbaException(errorCode)

    # method for easy frame creation
    def getFrame(self):
        """
        Creates and returns a new frame object. Multiple frames
        per camera can therefore be returned.

        :returns: VimbaFrame object -- the new frame.
        """
        return VimbaFrame(self)
