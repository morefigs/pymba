# -*- coding: utf-8 -*-
import vimbastructure as structs
from vimbaexception import VimbaException
from vimbadll import VimbaDLL
from vimbadll import VimbaC_MemoryBlock
from ctypes import *

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

		# frame structure
		self._frame = structs.VimbaFrame()
		
	def announceFrame(self):
		"""
		Announce frames to the API that may be queued for frame capturing later.
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
	
	def queueFrameCapture(self):
		"""
		Queue frames that may be ﬁlled during frame capturing.
		"""
		errorCode = VimbaDLL.captureFrameQueue(self._handle,
											   byref(self._frame),
											   None)	# callback not implemented, callback example in pico?
		if errorCode != 0:
			raise VimbaException(errorCode)
	
	def waitFrameCapture(self, timeout = 2000):
		"""
		Wait for a queued frame to be ﬁlled (or dequeued).
		"""
		errorCode = VimbaDLL.captureFrameWait(self._handle,
											  byref(self._frame),
											  timeout)
		if errorCode != 0:
			raise VimbaException(errorCode)	

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
		array = (c_ubyte * self.height * self.width).from_address(addressof(data.contents))
		
		return array
