# -*- coding: utf-8 -*-
import vimbastructure as structs
from vimbaexception import VimbaException
from sys import platform
import os
from ctypes import *

if platform == "win32":
	from ctypes.util import find_msvcrt
	_cruntime = cdll.LoadLibrary(find_msvcrt())
	vimbaC_path = r'C:\Program Files\Allied Vision Technologies\AVTVimba_1.2\VimbaC\Bin\Win32\VimbaC.dll'
	dll_loader = windll
else:
	_cruntime = CDLL("libc.so.6")
	dll_loader = cdll
	assert os.environ.get("GENICAM_GENTL64_PATH"), "you need your GENICAM_GENTL64_PATH environment set.  Make sure you have Vimba installed, and you have loaded the /etc/profile.d/ scripts"
	vimba_dir = "/".join(os.environ.get("GENICAM_GENTL64_PATH").split("/")[1:-3])
	vimbaC_path = "/" + vimba_dir + "/VimbaC/DynamicLib/x86_64bit/libVimbaC.so"

with open(vimbaC_path) as thefile:
	pass #NJO i think this is kind of like an os.exists ?


class VimbaDLL(object):
	"""
	ctypes directives to make the wrapper class work cleanly, 
	talks to VimbaC.dll
	"""
	# a full list of Vimba API methods
	# (only double dashed methods have been implemented so far)
	#
	# -- VmbVersionQuery()
	#
	# -- VmbStartup()
	# -- VmbShutdown()
	#
	# -- VmbCamerasList()
	# -- VmbCameraInfoQuery()
	# -- VmbCameraOpen()
	# -- VmbCameraClose()
	#
	# -- VmbFeaturesList()
	# -- VmbFeatureInfoQuery()
	# VmbFeatureListAffected()
	# VmbFeatureListSelected()
	# VmbFeatureAccessQuery()
	#
	# -- VmbFeatureIntGet()
	# -- VmbFeatureIntSet()
	# -- VmbFeatureIntRangeQuery()
	# VmbFeatureIntIncrementQuery()
	#
	# -- VmbFeatureFloatGet()
	# -- VmbFeatureFloatSet()
	# -- VmbFeatureFloatRangeQuery()
	#
	# -- VmbFeatureEnumGet()
	# -- VmbFeatureEnumSet()
	# VmbFeatureEnumRangeQuery()
	# VmbFeatureEnumIsAvailable()
	# VmbFeatureEnumAsInt()
	# VmbFeatureEnumAsString()
	# VmbFeatureEnumEntryGet()
	#
	# -- VmbFeatureStringGet()
	# -- VmbFeatureStringSet()
	# VmbFeatureStringMaxlengthQuery()
	#
	# -- VmbFeatureBoolGet()
	# -- VmbFeatureBoolSet()
	#
	# -- VmbFeatureCommandRun()
	# VmbFeatureCommandIsDone()
	#
	# VmbFeatureRawGet()
	# VmbFeatureRawSet()
	# VmbFeatureRawLengthQuery()
	#
	# VmbFeatureInvalidationRegister()
	# VmbFeatureInvalidationUnregister()
	#
	# -- VmbFrameAnnounce()
	# -- VmbFrameRevoke()
	# -- VmbFrameRevokeAll()
	# -- VmbCaptureStart()
	# -- VmbCaptureEnd()
	# -- VmbCaptureFrameQueue()
	# -- VmbCaptureFrameWait()
	# -- VmbCaptureQueueFlush()
	#
	# -- VmbInterfacesList()
	# -- VmbInterfaceOpen()
	# -- VmbInterfaceClose()
	#
	# VmbAncillaryDataOpen()
	# VmbAncillaryDataClose()
	#
	# VmbMemoryRead()
	# VmbMemoryWrite()
	# -- VmbRegistersRead()
	# -- VmbRegistersWrite()
	
	# Vimba C API DLL

	_vimbaDLL = dll_loader.LoadLibrary(vimbaC_path)
	
	# version query
	versionQuery = _vimbaDLL.VmbVersionQuery
	versionQuery.restype = c_int32									# returned error code
	versionQuery.argtypes = (POINTER(structs.VimbaVersion),			# pointer to version structure
							c_uint32)								# version structure size
	
	# startup
	startup = _vimbaDLL.VmbStartup
	startup.restype = c_int32										# returned error code
	
	# shutdown
	shutdown = _vimbaDLL.VmbShutdown
		
	# list cameras
	camerasList = _vimbaDLL.VmbCamerasList
	camerasList.restype = c_int32									# returned error code
	camerasList.argtypes = (POINTER(structs.VimbaCameraInfo),		# pointer to camera info structure
							c_uint32,								# length of list
							POINTER(c_uint32),						# pointer to number of cameras
							c_uint32)								# camera info structure size
	
	# camera info query
	cameraInfoQuery = _vimbaDLL.VmbCameraInfoQuery
	cameraInfoQuery.restype = c_int32
	cameraInfoQuery.argtypes = (c_char_p,							# camera unique id
								POINTER(structs.VimbaCameraInfo),	# pointer to camera info structure
								c_uint32)							# size of structure
	
	# camera open
	cameraOpen = _vimbaDLL.VmbCameraOpen
	cameraOpen.restype = c_int32									# returned error code
	cameraOpen.argtypes = (c_char_p,								# camera unique id
						   c_uint32,								# access mode
						   c_void_p)								# camera handle, pointer to a pointer
	
	# camera close
	cameraClose = _vimbaDLL.VmbCameraClose
	cameraClose.restype = c_int32									# returned error code
	cameraClose.argtypes = (c_void_p,)								# camera handle
	
	# list features
	featuresList = _vimbaDLL.VmbFeaturesList
	featuresList.restype = c_int32
	featuresList.argtypes = (c_void_p,								# handle, in this case camera handle
							 POINTER(structs.VimbaFeatureInfo),		# pointer to feature info structure
							 c_uint32,								# list length
							 POINTER(c_uint32),						# pointer to num features found
							 c_uint32)								# feature info size
	
	# feature info query
	featureInfoQuery = _vimbaDLL.VmbFeatureInfoQuery
	featureInfoQuery.restype = c_int32
	featureInfoQuery.argtypes = (c_void_p,							# handle, in this case camera handle
								 c_char_p,							# name of feature
								 POINTER(structs.VimbaFeatureInfo),	# pointer to feature info structure
								 c_uint32)							# size of structure
	
	# get the int value of a feature
	featureIntGet = _vimbaDLL.VmbFeatureIntGet
	featureIntGet.restype = c_int32
	featureIntGet.argtypes = (c_void_p,								# handle, in this case camera handle
							  c_char_p,								# name of the feature
							  POINTER(c_int64))						# value to get

	# set the int value of a feature
	featureIntSet = _vimbaDLL.VmbFeatureIntSet
	featureIntSet.restype = c_int32
	featureIntSet.argtypes = (c_void_p,								# handle, in this case camera handle
							  c_char_p,								# name of the feature
							  c_int64)								# value to set	# get the value of an integer feature
		
	# query the range of values of the feature
	featureIntRangeQuery = _vimbaDLL.VmbFeatureIntRangeQuery
	featureIntRangeQuery.restype = c_int32
	featureIntRangeQuery.argtypes = (c_void_p,						# handle
									 c_char_p,						# name of the feature
									 POINTER(c_int64),				# min range
									 POINTER(c_int64))				# max range
	
	# get the float value of a feature
	featureFloatGet = _vimbaDLL.VmbFeatureFloatGet
	featureFloatGet.restype = c_int32
	featureFloatGet.argtypes = (c_void_p,							# handle, in this case camera handle
								c_char_p,							# name of the feature
								POINTER(c_double))					# value to get

	# set the float value of a feature
	featureFloatSet = _vimbaDLL.VmbFeatureFloatSet
	featureFloatSet.restype = c_int32
	featureFloatSet.argtypes = (c_void_p,							# handle, in this case camera handle
								c_char_p,							# name of the feature
								c_double)							# value to set

	# query the range of values of the feature
	featureFloatRangeQuery = _vimbaDLL.VmbFeatureFloatRangeQuery
	featureFloatRangeQuery.restype = c_int32
	featureFloatRangeQuery.argtypes = (c_void_p,					# handle
									   c_char_p,					# name of the feature
									   POINTER(c_double),			# min range
									   POINTER(c_double))			# max range

	# get the enum value of a feature
	featureEnumGet = _vimbaDLL.VmbFeatureEnumGet
	featureEnumGet.restype = c_int32
	featureEnumGet.argtypes = (c_void_p,							# handle, in this case camera handle
							   c_char_p,							# name of the feature
							   POINTER(c_char_p))					# value to get

	# set the enum value of a feature
	featureEnumSet = _vimbaDLL.VmbFeatureEnumSet
	featureEnumSet.restype = c_int32
	featureEnumSet.argtypes = (c_void_p,							# handle, in this case camera handle
							   c_char_p,							# name of the feature
							   c_char_p)							# value to set

	# get the string value of a feature
	featureStringGet = _vimbaDLL.VmbFeatureStringGet
	featureStringGet.restype = c_int32
	featureStringGet.argtypes = (c_void_p,							# handle, in this case camera handle
								 c_char_p,							# name of the feature
								 c_char_p,							# string buffer to fill
								 c_uint32,							# size of the input buffer
								 POINTER(c_uint32))					# string buffer to fill

	# set the string value of a feature
	featureStringSet = _vimbaDLL.VmbFeatureStringSet
	featureStringSet.restype = c_int32
	featureStringSet.argtypes = (c_void_p,							# handle, in this case camera handle
								 c_char_p,							# name of the feature
								 c_char_p)							# value to set

	# get the boolean value of a feature
	featureBoolGet = _vimbaDLL.VmbFeatureBoolGet
	featureBoolGet.restype = c_int32
	featureBoolGet.argtypes = (c_void_p,							# handle, in this case camera handle
							   c_char_p,							# name of the feature
							   POINTER(c_bool))						# value to get

	# set the boolean value of a feature
	featureBoolSet = _vimbaDLL.VmbFeatureBoolSet
	featureBoolSet.restype = c_int32
	featureBoolSet.argtypes = (c_void_p,							# handle, in this case camera handle
							   c_char_p,							# name of the feature
							   c_bool)								# value to set

	# run a feature command
	featureCommandRun = _vimbaDLL.VmbFeatureCommandRun
	featureCommandRun.restype = c_int32
	featureCommandRun.argtypes = (c_void_p,							# handle for a module that exposes features
								  c_char_p)							# name of the command feature

	# announce frames to the API that may be queued for frame capturing later
	frameAnnounce = _vimbaDLL.VmbFrameAnnounce
	frameAnnounce.restype = c_int32
	frameAnnounce.argtypes = (c_void_p,								# camera handle
							  POINTER(structs.VimbaFrame),			# pointer to frame
							  c_uint32)								# size of frame
	
	# revoke a frame from the API
	frameRevoke = _vimbaDLL.VmbFrameRevoke
	frameRevoke.restype = c_int32
	frameRevoke.argtypes = (c_void_p,								# camera handle
							POINTER(structs.VimbaFrame))			# pointer to frame
	
	# revoke all frames assigned to a certain camera
	frameRevokeAll = _vimbaDLL.VmbFrameRevokeAll
	frameRevokeAll.restype = c_int32
	frameRevokeAll.argtypes = (c_void_p,)							# camera handle
	
	# prepare the API for incoming frames
	captureStart = _vimbaDLL.VmbCaptureStart
	captureStart.restype = c_int32
	captureStart.argtypes = (c_void_p,)								# camera handle
	
	# stop the API from being able to receive frames
	captureEnd = _vimbaDLL.VmbCaptureEnd
	captureEnd.restype = c_int32
	captureEnd.argtypes = (c_void_p,)								# camera handle
	
	# queue frames that may be filled during frame capturing
	captureFrameQueue = _vimbaDLL.VmbCaptureFrameQueue
	captureFrameQueue.restype = c_int32
	captureFrameQueue.argtypes = (c_void_p,
								  POINTER(structs.VimbaFrame),
								  c_void_p)							# callback
	
	# wait for a queued frame to be filled (or dequeued)
	captureFrameWait = _vimbaDLL.VmbCaptureFrameWait
	captureFrameWait.restype = c_int32
	captureFrameWait.argtypes = (c_void_p,							# camera handle
								 POINTER(structs.VimbaFrame),
								 c_uint32)							# timeout
		
	# flush the capture queue
	captureQueueFlush = _vimbaDLL.VmbCaptureQueueFlush
	captureQueueFlush.restype = c_int32
	captureQueueFlush.argtypes = (c_void_p,)						# camera handle
	
	# list interfaces
	interfacesList = _vimbaDLL.VmbInterfacesList
	interfacesList.restype = c_int32
	interfacesList.argtypes = (POINTER(structs.VimbaInterfaceInfo),		# pointer to interface info structure
							   c_uint32,								# length of list
							   POINTER(c_uint32),						# pointer to number of interfaces
							   c_uint32)	
	
	# open interface
	interfaceOpen = _vimbaDLL.VmbInterfaceOpen
	interfaceOpen.restype = c_int32
	interfaceOpen.argtypes = (c_char_p,								# unique id
							  c_void_p)								# handle
	
	# close interface
	interfaceClose = _vimbaDLL.VmbInterfaceClose
	interfaceClose.restype = c_int32
	interfaceClose.argtypes = (c_void_p,)							# handle
	
	# read from register
	registersRead = _vimbaDLL.VmbRegistersRead
	registersRead.restype = c_int32
	registersRead.argtypes = (c_void_p,								# handle
							  c_uint32,								# read count
							  POINTER(c_uint64),					# pointer to address array
							  POINTER(c_uint64),					# pointer to data array
							  POINTER(c_uint32))					# pointer to num complete reads
	
	# write to register
	registersWrite = _vimbaDLL.VmbRegistersWrite
	registersWrite.restype = c_int32
	registersWrite.argtypes = (c_void_p,							# handle
							   c_uint32,							# write count
							   POINTER(c_uint64),					# pointer to address array
							   POINTER(c_uint64),					# pointer to data array
							   POINTER(c_uint32))					# pointer to num complete write
	
	
class VimbaC_MemoryBlock(object):
	"""
	Just a memory block object for dealing
	neatly with C memory allocations.
	"""
	
	# C runtime DLL
	_crtDLL = _cruntime
	
	@property
	def block(self):
		return self._block
		
	def __init__(self, blockSize):

		# assign memory block		
		malloc = self._crtDLL.malloc
		malloc.argtypes = (c_size_t,)
		malloc.restype = c_void_p
		self._block = malloc(blockSize)		# todo check for NULL on failure
		
		# this seems to be None if too much memory is requested
		if self._block is None:
			raise VimbaException(-51)

	def __del__(self):
		
		# free memory block
		free = self._crtDLL.free
		free.argtypes = (c_void_p,)
		free.restype = None
		free(self._block)

	
	
	
	
	
	
	
	
	
	
	
	
