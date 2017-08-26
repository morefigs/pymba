# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import vimbastructure as structs
from .vimbadll import VimbaDLL
from .vimbaexception import VimbaException
from .vimbasystem import VimbaSystem
from .vimbacamera import VimbaCamera
from .vimbainterface import VimbaInterface
from ctypes import *


class Vimba(object):

    """
    An Allied Vision Technology Vimba API.
    This API provides access to AVT cameras.
    """

    # todo - assign camera info and feature info as own object proeprties

    def __init__(self):

        # create own system singleton object
        self._system = VimbaSystem()

        # lists of VimbaCameraInfo and VimbaInterfaceInfo objects
        # can't be called before startup() so populate later
        self._interfaceInfos = None

        # dict of {camera ID : VimbaCamera object} as we don't want to forget
        # them
        self._cameras = {}

        # dict of {interface ID : VimbaInterface object} as we don't want to
        # forget them
        self._interfaces = {}

    def __enter__(self):
        """
        Define vimba context for safe execution.

        The vimba object should be used like this:
            # start Vimba
            with Vimba() as vimba:
                system = vimba.getSystem()
                # ...
        """
        self.startup()
        return self

    def __exit__(self, type, value, traceback):
        """
        Shutdown Vimba when the with context is left. This allows cleanup
        when an error occurs in the main program. The system will not hang
        on a kernel call after an exception.
        """
        self.shutdown()

    def _getInterfaceInfos(self):
        """
        Gets interface info of all available interfaces.

        :returns: list -- interface info for available interfaces.
        """
        if self._interfaceInfos is None:
            # args
            numFound = c_uint32(-1)

            # call once just to get the number of interfaces
            # Vimba DLL will return an error code
            errorCode = VimbaDLL.interfacesList(None,
                                                0,
                                                byref(numFound),
                                                sizeof(structs.VimbaInterfaceInfo))
            if errorCode != 0:
                raise VimbaException(errorCode)

            numInterfaces = numFound.value

            # args
            interfaceInfoArray = (structs.VimbaInterfaceInfo * numInterfaces)()

            # call again to get the features
            # Vimba DLL will return an error code
            errorCode = VimbaDLL.interfacesList(interfaceInfoArray,
                                                numInterfaces,
                                                byref(numFound),
                                                sizeof(structs.VimbaInterfaceInfo))
            if errorCode != 0:
                raise VimbaException(errorCode)
            self._interfaceInfos = list(
                interfaceInfo for interfaceInfo in interfaceInfoArray)
        return self._interfaceInfos

    def _getCameraInfos(self):
        """
        Gets camera info of all attached cameras.

        :returns: list -- camera info for available cameras.
        """
        # args
        dummyCameraInfo = structs.VimbaCameraInfo()
        numFound = c_uint32(-1)

        # call once just to get the number of cameras
        # Vimba DLL will return an error code
        errorCode = VimbaDLL.camerasList(byref(dummyCameraInfo),
                                         0,
                                         byref(numFound),
                                         sizeof(dummyCameraInfo))
        if errorCode != 0 and errorCode != -9:
            raise VimbaException(errorCode)

        numCameras = numFound.value

        # args
        cameraInfoArray = (structs.VimbaCameraInfo * numCameras)()

        # call again to get the features
        # Vimba DLL will return an error code
        errorCode = VimbaDLL.camerasList(cameraInfoArray,
                                         numCameras,
                                         byref(numFound),
                                         sizeof(dummyCameraInfo))
        if errorCode != 0:
            raise VimbaException(errorCode)
        return list(camInfo for camInfo in cameraInfoArray)

    def getSystem(self):
        """
        Gets system singleton object.

        :returns: VimbaSystem object -- the system singleton object.
        """
        return self._system

    def getInterfaceIds(self):
        """
        Gets IDs of all available interfaces.

        :returns: list -- interface IDs for available interfaces.
        """
        return list(interfaceInfo.interfaceIdString for interfaceInfo in self._getInterfaceInfos())

    def getCameraIds(self):
        """
        Gets IDs of all available cameras.

        :returns: list -- camera IDs for available cameras.
        """
        return list(camInfo.cameraIdString.decode() for camInfo in self._getCameraInfos())

    def getInterfaceInfo(self, interfaceId):
        """
        Gets interface info object of specified interface.

        :param interfaceId: the ID of the interface object to get.

        :returns: VimbaInterfaceInfo object -- the interface info object specified.
        """
        # don't do this live as we already have this info
        # return info object if it exists
        for interfaceInfo in self._getInterfaceInfos():
            if interfaceInfo.interfaceIdString == interfaceId:
                return interfaceInfo
        # otherwise raise error
        raise VimbaException(-54)

    def getCameraInfo(self, cameraId):
        """
        Gets camera info object of specified camera.

        :param cameraId: the ID of the camera object to get.
                         This might not only be a cameraId as returned by getCameraIds() 
                         but also e.g. a serial number. Check the Vimba documentation for 
                         other possible values.

        :returns: VimbaCameraInfo object -- the camera info object specified.
        """
        cameraInfo = structs.VimbaCameraInfo()
        errorCode = VimbaDLL.cameraInfoQuery(cameraId.encode(),
                                             cameraInfo,
                                             sizeof(cameraInfo))
        if errorCode == 0:
            return cameraInfo

        # otherwise raise error
        raise VimbaException(-50)

    def getInterface(self, interfaceId):
        """
        Gets interface object based on interface ID string. Will not recreate
        interface object if it already exists.

        :param interfaceId: the ID of the interface.

        :returns: VimbaInterface object -- the interface object specified.
        """
        # check ID is valid
        if interfaceId in self.getInterfaceIds():
            # create it if it doesn't exist
            if interfaceId not in self._interfaces:
                self._interfaces[interfaceId] = VimbaInterface(interfaceId)
            return self._interfaces[interfaceId]
        raise VimbaException(-54)

    def getCamera(self, cameraId):
        """
        Gets camera object based on camera ID string. Will not recreate
        camera object if it already exists.

        :param cameraId: the ID of the camera object to get. 
                         This might not only be a cameraId as returned by getCameraIds() 
                         but also e.g. a serial number. Check the Vimba documentation for 
                         other possible values.

        :returns: VimbaCamera object -- the camera object specified.
        """
        # check ID is valid
        if cameraId in self.getCameraIds():
            # create it if it doesn't exist
            if cameraId not in self._cameras:
                self._cameras[cameraId] = VimbaCamera(cameraId)
            return self._cameras[cameraId]
        else:
            # the given string might not be a camera ID -> check for other IDs
            cameraInfo = structs.VimbaCameraInfo()
            errorCode = VimbaDLL.cameraInfoQuery(cameraId.encode(),
                                                 cameraInfo,
                                                 sizeof(cameraInfo))
            if errorCode != 0:
                raise VimbaException(-50)   # camera not found
            
            cameraIdString = cameraInfo.cameraIdString.decode()
            if cameraIdString not in self._cameras:
                self._cameras[cameraIdString] = VimbaCamera(cameraIdString)
            return self._cameras[cameraIdString]
            

    def getVersion(self):
        """
        Retrieve the version number of VimbaC.

        :returns: string - Vimba API version info.
        """
        # args
        versionInfo = structs.VimbaVersion()

        # Vimba DLL will return an error code
        errorCode = VimbaDLL.versionQuery(versionInfo,
                                          sizeof(versionInfo))
        if errorCode != 0:
            raise VimbaException(errorCode)

        versionStr = '.'.join([str(versionInfo.major),
                               str(versionInfo.minor),
                               str(versionInfo.patch)])
        return versionStr

    def startup(self):
        """
        Initialize the VimbaC API.
        """
        # Vimba DLL will return an error code
        errorCode = VimbaDLL.startup()
        if errorCode != 0:
            raise VimbaException(errorCode)

    def shutdown(self):
        """
        Perform a shutdown on the API.
        """
        VimbaDLL.shutdown()
