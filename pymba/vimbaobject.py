# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import vimbastructure as structs
from .vimbaexception import VimbaException
from .vimbafeature import VimbaFeature
from .vimbadll import VimbaDLL
from ctypes import *


class VimbaObject(object):

    """
    A Vimba object has a handle and features associated with it.
    Objects include System,	Camera, Interface and AncillaryData.
    """

    @property
    def handle(self):
        return self._handle

    def __init__(self):
        # create own handle
        self._handle = c_void_p()

        # list of VimbaFeatureInfo objects
        # can't set yet as the object (e.g. a camera) won't be
        # opened yet, therefore no event for object opening
        # so will have it populate by user interaction
        # and blame them if the object is not opened then
        self._featureInfos = None

    # override getattr for undefined attributes
    def __getattr__(self, attr):

        # if a feature value requested (requires object (camera) open)
        if attr in self.getFeatureNames():
            return VimbaFeature(attr, self._handle).value

        # otherwise don't know about it
        raise AttributeError(''.join(["'VimbaObject' has no attribute '",
                                      attr,
                                      "'"]))

    # override setattr for undefined attributes
    def __setattr__(self, attr, val):

        # set privates as normal
        # check this first to allow all privates to set normally
        # and avoid recursion errors
        if attr.startswith('_'):
            super(VimbaObject, self).__setattr__(attr, val)

        # if it's an actual camera feature (requires camera open)
        elif attr in self.getFeatureNames():
            VimbaFeature(attr, self._handle).value = val

        # otherwise just set the attribute value as normal
        else:
            super(VimbaObject, self).__setattr__(attr, val)

    def _getFeatureInfos(self):
        """
        Gets feature info of all available features. Will
        cause error if object/camera is not opened.

        :returns: list -- feature info for available features.
        """
        # check it's populated as can't populate it in __init__
        if self._featureInfos is None:
            # args
            dummyFeatureInfo = structs.VimbaFeatureInfo()
            numFound = c_uint32(-1)

            # call once to get number of available features
            # Vimba DLL will return an error code
            errorCode = VimbaDLL.featuresList(self._handle,
                                              None,
                                              0,
                                              byref(numFound),
                                              sizeof(dummyFeatureInfo))
            if errorCode != 0:
                raise VimbaException(errorCode)

            # number of features specified by Vimba
            numFeatures = numFound.value

            # args
            featureInfoArray = (structs.VimbaFeatureInfo * numFeatures)()

            # call again to get the features
            # Vimba DLL will return an error code
            errorCode = VimbaDLL.featuresList(self._handle,
                                              featureInfoArray,
                                              numFeatures,
                                              byref(numFound),
                                              sizeof(dummyFeatureInfo))
            if errorCode != 0:
                raise VimbaException(errorCode)

            self._featureInfos = list(
                featInfo for featInfo in featureInfoArray)
        return self._featureInfos

    def getFeatureNames(self):
        """
        Get names of all available features.

        :returns: list -- feature names for available features.
        """
        return list(featInfo.name.decode() for featInfo in self._getFeatureInfos())

    def getFeatureInfo(self, featureName):
        """
        Gets feature info object of specified feature.

        :param featureName: the name of the feature.

        :returns: VimbaFeatureInfo object -- the feature info object specified.
        """
        # don't do this live as we already have this info
        # return info object, if it exists
        for featInfo in self._getFeatureInfos():
            if featInfo.name.decode() == featureName:
                return featInfo
        # otherwise raise error
        raise VimbaException(-53)

    # don't think we ever need to return a feature object...
    # def getFeature(self, featureName):

    def getFeatureRange(self, featureName):
        """
        Get valid range of feature values.

        :param featureName: name of the feature to query.

        :returns: tuple -- range as (feature min value, feature max value).
        """
        # can't cache this, need to look it up live
        return VimbaFeature(featureName.encode(), self._handle).range

    def runFeatureCommand(self, featureName):
        """
        Run a feature command.

        :param featureName: the name of the feature.
        """
        # run a command
        errorCode = VimbaDLL.featureCommandRun(self._handle,
                                               featureName.encode())
        if errorCode != 0:
            raise VimbaException(errorCode)

    def featureCommandIsDone(self, featureName):
        isDone = c_bool()
        errorCode = VimbaDLL.featureCommandIsDone(self._handle,
                                                  featureName.encode(),
                                                  byref(isDone))

        if errorCode != 0:
            raise VimbaException(errorCode)

        return isDone.value


    def readRegister(self, address):
        # note that the underlying Vimba function allows reading of an array
        # of registers, but only one address/value at a time is implemented
        # here
        """
        Read from a register of the module (camera).

        :param address: the address of the register to read.

        :returns: int -- value of register.
        """
        readCount = 1

        # check address validity
        try:
            regAddress = c_uint64(int(address, 16))
        except:
            raise VimbaException(-52)

        regData = c_uint64()
        numCompleteReads = c_uint32()

        errorCode = VimbaDLL.registersRead(self.handle,
                                           readCount,
                                           byref(regAddress),
                                           byref(regData),
                                           byref(numCompleteReads))

        if errorCode != 0:
            raise VimbaException(errorCode)

        return regData.value

    def writeRegister(self, address, value):
        # note that the underlying Vimba function allows writing of an array
        # of registers, but only one address/value at a time is implemented
        # here
        """
        Read from a register of the module (camera).

        :param address: the address of the register to read.
        :param value: the value to set in hex.
        """
        writeCount = 1

        # check address validity
        try:
            regAddress = c_uint64(int(address, 16))
        except:
            raise VimbaException(-52)

        # check value validity
        try:
            regData = c_uint64(int(value, 16))
        except:
            raise VimbaException(-52)

        numCompleteWrites = c_uint32()

        errorCode = VimbaDLL.registersWrite(self.handle,
                                            writeCount,
                                            byref(regAddress),
                                            byref(regData),
                                            byref(numCompleteWrites))
        if errorCode != 0:
            raise VimbaException(errorCode)
