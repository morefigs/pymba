# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import vimbastructure as structs
from .vimbaexception import VimbaException
from .vimbadll import VimbaDLL
from ctypes import *

# class may extend a generic Vimba entity class one day...


class VimbaFeature(object):

    """
    A feature of a Vimba object.
    """

    @property
    def name(self):
        return self._name.decode()

    @property
    def handle(self):
        return self._handle

    # lookup relevant function for feature type and pass to that function
    @property
    def value(self):
        return self._getSetTypeFuncs[self._info.featureDataType][0]()

    @value.setter
    def value(self, val):
        self._getSetTypeFuncs[self._info.featureDataType][1](val)

    @property
    def range(self):
        return self._rangeQueryTypeFuncs[self._info.featureDataType]()

    def __init__(self, name, handle):

        # set name and handle
        self._name = name.encode()
        self._handle = handle

        # set own info
        self._info = self._getInfo()

        # type functions dict for looking up correct get/set function to use
        self._getSetTypeFuncs = {0: (self._notYetImplemented, self._notYetImplemented),		# todo
                                 1: (self._getIntFeature, self._setIntFeature),
                                 2: (self._getFloatFeature, self._setFloatFeature),
                                 3: (self._getEnumFeature, self._setEnumFeature),
                                 4: (self._getStringFeature, self._setStringFeature),
                                 5: (self._getBoolFeature, self._setBoolFeature),
                                 # todo
                                 6: (self._notYetImplemented, self._notYetImplemented),
                                 # todo
                                 7: (self._notYetImplemented, self._notYetImplemented),
                                 8: (self._notYetImplemented, self._notYetImplemented)}		# todo

        # type functions dict for looking up correct range function to use
        self._rangeQueryTypeFuncs = {0: self._unknownRange,
                                     1: self._rangeQueryIntFeature,
                                     2: self._rangeQueryFloatFeature,
                                     3: self._unknownRange,
                                     4: self._unknownRange,
                                     5: self._unknownRange,
                                     6: self._unknownRange,
                                     7: self._unknownRange,
                                     8: self._unknownRange}

    def getInfo(self):
        """
        Get info of the feature.

        :returns: VimbaFeatureInfo object -- feature information..
        """
        return self._info

    def _getInfo(self):
        """
        Get info of the feature.

        :returns: VimbaFeatureInfo object -- feature information..
        """
        # args for Vimba call
        featureInfo = structs.VimbaFeatureInfo()

        # Vimba DLL will return an error code
        errorCode = VimbaDLL.featureInfoQuery(self._handle,
                                              self._name,
                                              byref(featureInfo),
                                              sizeof(featureInfo))
        if errorCode != 0:
            raise VimbaException(errorCode)

        return featureInfo

    def _notYetImplemented(self, val=None):
        """
        Raises exception if feature value type is not yet defined.
        """
        raise VimbaException(-1001)

    def _getIntFeature(self):
        """
        Get the value of an integer feature.

        :returns: int -- value of the specified feature.
        """

        # create args
        valueToGet = c_int64()

        errorCode = VimbaDLL.featureIntGet(self._handle,
                                           self._name,
                                           byref(valueToGet))
        if errorCode != 0:
            raise VimbaException(errorCode)

        return valueToGet.value

    def _setIntFeature(self, valueToSet):
        """
        Set the value of an integer feature.

        :param valueToSet: the int value to set for the feature.
        """

        errorCode = VimbaDLL.featureIntSet(self._handle,
                                           self._name,
                                           valueToSet)
        if errorCode != 0:
            raise VimbaException(errorCode)

    def _getFloatFeature(self):
        """
        Get the value of a ﬂoat feature.

        :returns: float -- value of the specified feature.
        """

        # create args
        valueToGet = c_double()

        errorCode = VimbaDLL.featureFloatGet(self._handle,
                                             self._name,
                                             byref(valueToGet))
        if errorCode != 0:
            raise VimbaException(errorCode)

        return valueToGet.value

    def _setFloatFeature(self, valueToSet):
        """
        Set the value of a float feature.

        :param valueToSet: the float value to set for the feature.
        """

        errorCode = VimbaDLL.featureFloatSet(self._handle,
                                             self._name,
                                             valueToSet)
        if errorCode != 0:
            raise VimbaException(errorCode)

    def _getEnumFeature(self):
        """
        Get the value of an enum feature.

        :returns: enum -- value of the specified feature.
        """

        # create args
        valueToGet = c_char_p()

        errorCode = VimbaDLL.featureEnumGet(self._handle,
                                            self._name,
                                            byref(valueToGet))
        if errorCode != 0:
            raise VimbaException(errorCode)

        return valueToGet.value.decode()

    def _setEnumFeature(self, valueToSet):
        """
        Set the value of an enum feature.

        :param valueToSet: the enum value to set for the feature.
        """

        errorCode = VimbaDLL.featureEnumSet(self._handle,
                                            self._name,
                                            valueToSet.encode())
        if errorCode != 0:
            raise VimbaException(errorCode)

    def _getStringFeature(self):
        """
        Get the value of a string feature.

        :returns: string -- value of the specified feature.
        """

        # create args
        bufferSize = 256
        valueToGet = create_string_buffer('\000' * bufferSize)
        sizeFilled = c_uint32()

        errorCode = VimbaDLL.featureStringGet(self._handle,
                                              self._name,
                                              valueToGet,
                                              bufferSize,
                                              byref(sizeFilled))
        if errorCode != 0:
            raise VimbaException(errorCode)
        return valueToGet.value.decode()

    def _setStringFeature(self, valueToSet):
        """
        Set the value of a string feature.

        :param valueToSet: the string value to set for the feature.
        """

        errorCode = VimbaDLL.featureStringSet(self._handle,
                                              self._name,
                                              valueToSet.encode())
        if errorCode != 0:
            raise VimbaException(errorCode)

    def _getBoolFeature(self):
        """
        Get the value of a bool feature.

        :returns: bool -- value of the specified feature.
        """

        # create args
        valueToGet = c_bool()

        errorCode = VimbaDLL.featureBoolGet(self._handle,
                                            self._name,
                                            byref(valueToGet))
        if errorCode != 0:
            raise VimbaException(errorCode)

        return valueToGet.value

    def _setBoolFeature(self, valueToSet):
        """
        Set the value of a bool feature.

        :param valueToSet: the bool value to set for the feature.
        """

        errorCode = VimbaDLL.featureBoolSet(self._handle,
                                            self._name,
                                            valueToSet)
        if errorCode != 0:
            raise VimbaException(errorCode)

    def _unknownRange(self):
        """
        Returns empty for ranges that have not been implemented.
        """
        return ''

    def _rangeQueryIntFeature(self):
        """
        Get the range of an int feature.

        :returns: tuple -- min and max range.
        """

        # create args
        minToGet = c_int64()
        maxToGet = c_int64()

        errorCode = VimbaDLL.featureIntRangeQuery(self._handle,
                                                  self._name,
                                                  byref(minToGet),
                                                  byref(maxToGet))
        if errorCode != 0:
            raise VimbaException(errorCode)

        return (int(str(minToGet.value)), int(str(maxToGet.value)))

    def _rangeQueryFloatFeature(self):
        """
        Get the range of a float feature.

        :returns: tuple -- min and max range.
        """

        # create args
        minToGet = c_double()
        maxToGet = c_double()

        errorCode = VimbaDLL.featureFloatRangeQuery(self._handle,
                                                    self._name,
                                                    byref(minToGet),
                                                    byref(maxToGet))
        if errorCode != 0:
            raise VimbaException(errorCode)

        return (minToGet.value, maxToGet.value)

    # def _rangeQueryEnumFeature(self):
    #	"""
    #	Get the range of an enum feature.
    #
    #	:returns: tuple -- min and max range.
    #	"""
    #
    # create args
    #	minToGet = c_uint32()
    #	maxToGet = c_uint32()
    #
    #	errorCode = VimbaDLL.featureEnumRangeQuery(self._handle,
    #											   self._name,
    #											   byref(minToGet),
    #											   byref(maxToGet))
    #	if errorCode != 0:
    #		raise VimbaException(errorCode)
    #
    #	return (minToGet.value, maxToGet.value)
