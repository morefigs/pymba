# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import vimbastructure as structs
from .vimbaexception import VimbaException
from .vimbadll import VimbaDLL
from .vimbadll import VimbaC_MemoryBlock
from ctypes import *
import warnings
try:
    import numpy as np
except ImportError:
    warnings.warn('numpy not found, some VimbaFrame methods will not be available')


"""
Map pixel formats to bytes per pixel.
    The packed formats marked with "?" have not been tested.
"""
PIXEL_FORMATS = {
    "Mono8": 1,
    "Mono12": 2,
    "Mono12Packed": 1.5,  # ?
    "Mono14": 2,
    "Mono16": 2,
    "RGB8Packed": 3,
    "BGR8Packed": 3,
    "RGBA8Packed": 4,
    "BGRA8Packed": 4,
    "YUV411Packed": 4/3.0,  # ?
    "YUV422Packed": 2,
    "YUV444Packed": 3,
    "BayerRG8": 1,
    "BayerRG12": 2,
    "BayerGR8": 1,
    "BayerGR12": 2,
    "BayerGR12Packed": 1.5,  # ?
}


class VimbaFrame(object):
    """
    A Vimba frame.
    """
    def __init__(self, camera):
        self._camera = camera
        self._handle = camera.handle

        # get frame sizes
        self.payloadSize = self._camera.PayloadSize
        self.width = self._camera.Width
        self.height = self._camera.Height
        self.pixel_bytes = PIXEL_FORMATS[self._camera.PixelFormat]

        # frame structure
        self._frame = structs.VimbaFrame()

    def announceFrame(self):
        """
        Announce frames to the API that may be queued for frame capturing later.

        Runs VmbFrameAnnounce

        Should be called after the frame is created.  Call startCapture
        after this method.
        """
        # size of expected frame
        sizeOfFrame = self.payloadSize

        # keep this reference to keep block alive for life of frame
        self._cMem = VimbaC_MemoryBlock(sizeOfFrame)
        # set buffer to have length of expected payload size
        self._frame.buffer = self._cMem.block

        # set buffer size to expected payload size
        self._frame.bufferSize = sizeOfFrame

        errorCode = VimbaDLL.frameAnnounce(self._handle,
                                           byref(self._frame),
                                           sizeof(self._frame))

        if errorCode != 0:
            raise VimbaException(errorCode)

    def revokeFrame(self):
        """
        Revoke a frame from the API.
        """
        errorCode = VimbaDLL.frameRevoke(self._handle,
                                         byref(self._frame))

        if errorCode != 0:
            raise VimbaException(errorCode)

    def queueFrameCapture(self, frameCallback = None):
        """
        Queue frames that may be ﬁlled during frame capturing.
        Runs VmbCaptureFrameQueue

        Call after announceFrame and startCapture

        Callback must accept argument of type frame. Remember to requeue the
        frame by calling frame.queueFrameCapture(frameCallback) at the end of
        your callback function.
        """
        # remember the given callback function
        self._frameCallback = frameCallback

        # define a callback wrapper here so it doesn't bind self
        def frameCallbackWrapper(cam_handle, p_frame):
            # call the user's callback with the self bound outside the wrapper
            # ignore the frame pointer since we already know the callback
            # refers to this frame
            self._frameCallback(self)

        if self._frameCallback is None:
            self._frameCallbackWrapper_C = None
        else:
            # keep a reference to prevent gc issues
            self._frameCallbackWrapper_C = VimbaDLL.frameDoneCallback(frameCallbackWrapper)

        errorCode = VimbaDLL.captureFrameQueue(self._handle,
                                               byref(self._frame),
                                               self._frameCallbackWrapper_C)
        if errorCode != 0:
            raise VimbaException(errorCode)

    def waitFrameCapture(self, timeout=2000):
        """
        Wait for a queued frame to be ﬁlled (or dequeued).  Returns Errorcode
        upon completion.
        Runs VmbCaptureFrameWait

        timeout - int, milliseconds default(timeout, 2000)

        Call after an acquisition command
        """
        errorCode = VimbaDLL.captureFrameWait(self._handle,
                                              byref(self._frame),
                                              timeout)

        # errorCode to be processed by the end user for this function.
        # Prevents system for breaking for example on a hardware trigger
        # timeout
        #if errorCode != 0:
            #raise VimbaException(errorCode)
        return errorCode

    # custom method for simplified usage
    def getBufferByteData(self):
        """
        Retrieve buffer data in a useful format.

        :returns: array -- buffer data.
        """

        # cast frame buffer memory contents to a usable type
        data = cast(self._frame.buffer,
                    POINTER(c_ubyte * self.payloadSize))

        # make array of c_ubytes from buffer
        array = (c_ubyte * int(self.height*self.pixel_bytes) *
                 int(self.width*self.pixel_bytes)).from_address(addressof(
                                                                data.contents))

        return array

    def getImage(self):
        cframe = self._frame
        data = cast(cframe.buffer, POINTER(c_ubyte * cframe.imageSize))
        try:
            return np.ndarray(buffer=data.contents, dtype=np.uint8, shape=(cframe.height, cframe.width))
        except NameError as e:
            print('install numpy to use this method or use getBufferByteData instead')
            raise e
