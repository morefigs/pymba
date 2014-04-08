# -*- coding: utf-8 -*-
from ctypes import *

	
class VimbaVersion(Structure):
	_fields_ = [('major', c_uint32),
				('minor', c_uint32),
				('patch', c_uint32)]


class VimbaInterfaceInfo(Structure):
	_fields_ = [('interfaceIdString', c_char_p),	# Unique identifier for each interface
				('interfaceType', c_uint32),		# Interface type, see VmbInterfaceType
				('interfaceName', c_char_p),		# Interface name, given by the transport layer
				('serialString', c_char_p),			# Serial number
				('permittedAccess', c_uint32)]		# Used access mode, see VmbAccessModeType
	
	def getFieldNames(self):
		"""
		Get field names.
		"""
		return [field[0] for field in self._fields_]


class VimbaCameraInfo(Structure):
	_fields_ = [('cameraIdString', c_char_p),		# Unique identifier for each camera
				('cameraName', c_char_p),			# Name of the camera
				('modelName', c_char_p),			# Model name
				('serialString', c_char_p),			# Serial number
				('permittedAccess', c_uint32),		# Used access mode, see VmbAccessModeType
				('interfaceIdString', c_char_p)]	# Unique value for each interface or bus
	
	def getFieldNames(self):
		"""
		Get field names.
		"""
		return [field[0] for field in self._fields_]
	

class VimbaFeatureInfo(Structure):

	_fields_ = [('name', c_char_p),
				('featureDataType', c_uint32),
				('featureFlags', c_uint32),
				('category', c_char_p),
				('displayName', c_char_p),
				('pollingTime', c_uint32),
				('unit', c_char_p),
				('representation', c_char_p),
				('visibility', c_uint32),
				('tooltip', c_char_p),
				('description', c_char_p),
				('sfncNamespace', c_char_p),
				('isStreamable', c_bool),
				('hasAffectedFeatures', c_bool),
				('hasSelectedFeatures', c_bool)]

	def getFieldNames(self):
		"""
		Get field names.
		"""
		return [field[0] for field in self._fields_]


class VimbaFrame(Structure):
				
				# IN
	_fields_ = [('buffer', c_void_p),				# Comprises image and ancillary data
				('bufferSize', c_uint32),			# Size of the data buffer
				
				('context', c_void_p * 4),			# User context filled during queuing
				
				# OUT
				('receiveStatus', c_int32),  		# Resulting status of the receive operation
				('receiveFlags', c_uint32),			# Resulting flags of the receive operation
				
				('imageSize', c_uint32),			# Size of the image data inside the data buffer
				('ancillarySize', c_uint32),		# Size of the ancillary data inside the data buffer
				
				('pixelFormat', c_uint32),			# Pixel format of the image
				
				('width', c_uint32),				# Width of an image
				('height', c_uint32),				# Height of an image
				('offsetX', c_uint32),				# Horizontal offset of an image
				('offsetY', c_uint32),				# Vertical offset of an image
				
				('frameID', c_uint64),				# Unique ID of this frame in this stream
				('timestamp', c_uint64)]			# Timestamp of the data transfer
	
	def getFieldNames(self):
		"""
		Get field names.
		"""
		return [field[0] for field in self._fields_]



	
	
