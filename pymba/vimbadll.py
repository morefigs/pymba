# -*- coding: utf-8 -*-
from __future__ import absolute_import

from sys import platform as sys_plat
import platform
import os
from ctypes import *

from . import vimbastructure as structs
from .vimbaexception import VimbaException

if sys_plat == "win32":

    def find_win_dll(arch):
        """ Finds the highest versioned windows dll for the specified architecture. """
        bases = [
            r'C:\Program Files\Allied Vision Technologies\AVTVimba_%i.%i\VimbaC\Bin\Win%i\VimbaC.dll',
            r'C:\Program Files\Allied Vision\Vimba_%i.%i\VimbaC\Bin\Win%i\VimbaC.dll'
        ]
        dlls = []
        for base in bases:
            for major in range(3):
                for minor in range(10):
                    candidate = base % (major, minor, arch)
                    if os.path.isfile(candidate):
                        dlls.append(candidate)
        if not dlls:
            if 'VIMBA_HOME' in os.environ:
                candidate = os.environ ['VIMBA_HOME'] + '\VimbaC\Bin\Win%i\VimbaC.dll' % (arch)
                if os.path.isfile(candidate):
                    dlls.append(candidate)
        if not dlls:
            raise IOError("VimbaC.dll not found.")
        return dlls[-1]

    if '64' in platform.architecture()[0]:
        vimbaC_path = find_win_dll(64)
    else:
        vimbaC_path = find_win_dll(32)
    dll_loader = windll
else:

    dll_loader = cdll

    if 'x86_64' in os.uname()[4]:
        assert os.environ.get(
            "GENICAM_GENTL64_PATH"), "you need your GENICAM_GENTL64_PATH environment set.  Make sure you have Vimba installed, and you have loaded the /etc/profile.d/ scripts"
        tlPath = [p for p in os.environ.get("GENICAM_GENTL64_PATH").split(":") if p][0]
        vimba_dir = "/".join(tlPath.split("/")[1:-3])
        vimbaC_path = "/" + vimba_dir + "/VimbaC/DynamicLib/x86_64bit/libVimbaC.so"
    elif 'x86_32' in os.uname()[4]:
        print("Warning: x86_32 reached!")
        assert os.environ.get(
            "GENICAM_GENTL32_PATH"), "you need your GENICAM_GENTL32_PATH environment set.  Make sure you have Vimba installed, and you have loaded the /etc/profile.d/ scripts"
        tlPath = [p for p in os.environ.get("GENICAM_GENTL32_PATH").split(":") if p][0]
        vimba_dir = "/".join(tlPath.split("/")[1:-3])
        vimbaC_path = "/" + vimba_dir + "/VimbaC/DynamicLib/x86_32bit/libVimbaC.so"
    elif 'arm' in os.uname()[4]:
        assert os.environ.get(
            "GENICAM_GENTL32_PATH"), "you need your GENICAM_GENTL32_PATH environment set.  Make sure you have Vimba installed, and you have loaded the /etc/profile.d/ scripts"
        tlPath = [p for p in os.environ.get("GENICAM_GENTL32_PATH").split(":") if p][0]
        vimba_dir = "/".join(tlPath.split("/")[1:-3])
        vimbaC_path = "/" + vimba_dir + "/VimbaC/DynamicLib/arm_32bit/libVimbaC.so"    
    elif 'aarch64' in os.uname()[4]:
        assert os.environ.get(
            "GENICAM_GENTL64_PATH"), "you need your GENICAM_GENTL64_PATH environment set.  Make sure you have Vimba installed, and you have loaded the /etc/profile.d/ scripts"
        tlPath = [p for p in os.environ.get("GENICAM_GENTL64_PATH").split(":") if p][0]
        vimba_dir = "/".join(tlPath.split("/")[1:-3])
        vimbaC_path = "/" + vimba_dir + "/VimbaC/DynamicLib/arm_64bit/libVimbaC.so"
    else:
        raise ValueError("Pymba currently doesn't support %s" % os.uname()[4])


# Callback Function Type
if sys_plat == "win32":
    CB_FUNCTYPE = WINFUNCTYPE
else:
    # Untested!
    CB_FUNCTYPE = CFUNCTYPE


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
    # returned error code
    versionQuery.restype = c_int32
    versionQuery.argtypes = (POINTER(structs.VimbaVersion),            # pointer to version structure
                             c_uint32)                                # version structure size

    # startup
    startup = _vimbaDLL.VmbStartup
    # returned error code
    startup.restype = c_int32

    # shutdown
    shutdown = _vimbaDLL.VmbShutdown

    # list cameras
    camerasList = _vimbaDLL.VmbCamerasList
    # returned error code
    camerasList.restype = c_int32
    camerasList.argtypes = (POINTER(structs.VimbaCameraInfo),        # pointer to camera info structure
                            # length of list
                            c_uint32,
                            # pointer to number of cameras
                            POINTER(c_uint32),
                            c_uint32)                                # camera info structure size

    # camera info query
    cameraInfoQuery = _vimbaDLL.VmbCameraInfoQuery
    cameraInfoQuery.restype = c_int32
    cameraInfoQuery.argtypes = (c_char_p,                            # camera unique id
                                # pointer to camera info structure
                                POINTER(structs.VimbaCameraInfo),
                                c_uint32)                            # size of structure

    # camera open
    cameraOpen = _vimbaDLL.VmbCameraOpen
    # returned error code
    cameraOpen.restype = c_int32
    cameraOpen.argtypes = (c_char_p,                                # camera unique id
                           # access mode
                           c_uint32,
                           c_void_p)                                # camera handle, pointer to a pointer

    # camera close
    cameraClose = _vimbaDLL.VmbCameraClose
    # returned error code
    cameraClose.restype = c_int32
    # camera handle
    cameraClose.argtypes = (c_void_p,)

    # list features
    featuresList = _vimbaDLL.VmbFeaturesList
    featuresList.restype = c_int32
    featuresList.argtypes = (c_void_p,                                # handle, in this case camera handle
                             # pointer to feature info structure
                             POINTER(structs.VimbaFeatureInfo),
                             # list length
                             c_uint32,
                             # pointer to num features found
                             POINTER(c_uint32),
                             c_uint32)                                # feature info size

    # feature info query
    featureInfoQuery = _vimbaDLL.VmbFeatureInfoQuery
    featureInfoQuery.restype = c_int32
    featureInfoQuery.argtypes = (c_void_p,                            # handle, in this case camera handle
                                 # name of feature
                                 c_char_p,
                                 # pointer to feature info structure
                                 POINTER(structs.VimbaFeatureInfo),
                                 c_uint32)                            # size of structure

    # get the int value of a feature
    featureIntGet = _vimbaDLL.VmbFeatureIntGet
    featureIntGet.restype = c_int32
    featureIntGet.argtypes = (c_void_p,                                # handle, in this case camera handle
                              # name of the feature
                              c_char_p,
                              POINTER(c_int64))                        # value to get

    # set the int value of a feature
    featureIntSet = _vimbaDLL.VmbFeatureIntSet
    featureIntSet.restype = c_int32
    featureIntSet.argtypes = (c_void_p,                                # handle, in this case camera handle
                              # name of the feature
                              c_char_p,
                              c_int64)                                # value to set    # get the value of an integer feature

    # query the range of values of the feature
    featureIntRangeQuery = _vimbaDLL.VmbFeatureIntRangeQuery
    featureIntRangeQuery.restype = c_int32
    featureIntRangeQuery.argtypes = (c_void_p,                        # handle
                                     # name of the feature
                                     c_char_p,
                                     # min range
                                     POINTER(c_int64),
                                     POINTER(c_int64))                # max range

    # get the float value of a feature
    featureFloatGet = _vimbaDLL.VmbFeatureFloatGet
    featureFloatGet.restype = c_int32
    featureFloatGet.argtypes = (c_void_p,                            # handle, in this case camera handle
                                # name of the feature
                                c_char_p,
                                POINTER(c_double))                    # value to get

    # set the float value of a feature
    featureFloatSet = _vimbaDLL.VmbFeatureFloatSet
    featureFloatSet.restype = c_int32
    featureFloatSet.argtypes = (c_void_p,                            # handle, in this case camera handle
                                # name of the feature
                                c_char_p,
                                c_double)                            # value to set

    # query the range of values of the feature
    featureFloatRangeQuery = _vimbaDLL.VmbFeatureFloatRangeQuery
    featureFloatRangeQuery.restype = c_int32
    featureFloatRangeQuery.argtypes = (c_void_p,                    # handle
                                       # name of the feature
                                       c_char_p,
                                       # min range
                                       POINTER(c_double),
                                       POINTER(c_double))            # max range

    # get the enum value of a feature
    featureEnumGet = _vimbaDLL.VmbFeatureEnumGet
    featureEnumGet.restype = c_int32
    featureEnumGet.argtypes = (c_void_p,                            # handle, in this case camera handle
                               # name of the feature
                               c_char_p,
                               POINTER(c_char_p))                    # value to get

    # set the enum value of a feature
    featureEnumSet = _vimbaDLL.VmbFeatureEnumSet
    featureEnumSet.restype = c_int32
    featureEnumSet.argtypes = (c_void_p,                            # handle, in this case camera handle
                               # name of the feature
                               c_char_p,
                               c_char_p)                            # value to set

    # get the string value of a feature
    featureStringGet = _vimbaDLL.VmbFeatureStringGet
    featureStringGet.restype = c_int32
    featureStringGet.argtypes = (c_void_p,                            # handle, in this case camera handle
                                 # name of the feature
                                 c_char_p,
                                 # string buffer to fill
                                 c_char_p,
                                 # size of the input buffer
                                 c_uint32,
                                 POINTER(c_uint32))                    # string buffer to fill

    # set the string value of a feature
    featureStringSet = _vimbaDLL.VmbFeatureStringSet
    featureStringSet.restype = c_int32
    featureStringSet.argtypes = (c_void_p,                            # handle, in this case camera handle
                                 # name of the feature
                                 c_char_p,
                                 c_char_p)                            # value to set

    # get the boolean value of a feature
    featureBoolGet = _vimbaDLL.VmbFeatureBoolGet
    featureBoolGet.restype = c_int32
    featureBoolGet.argtypes = (c_void_p,                            # handle, in this case camera handle
                               # name of the feature
                               c_char_p,
                               POINTER(c_bool))                        # value to get

    # set the boolean value of a feature
    featureBoolSet = _vimbaDLL.VmbFeatureBoolSet
    featureBoolSet.restype = c_int32
    featureBoolSet.argtypes = (c_void_p,                            # handle, in this case camera handle
                               # name of the feature
                               c_char_p,
                               c_bool)                                # value to set

    # run a feature command
    featureCommandRun = _vimbaDLL.VmbFeatureCommandRun
    featureCommandRun.restype = c_int32
    featureCommandRun.argtypes = (c_void_p,                            # handle for a module that exposes features
                                  c_char_p)                            # name of the command feature

    # Check if a feature command is done
    featureCommandIsDone = _vimbaDLL.VmbFeatureCommandIsDone
    featureCommandIsDone.restype = c_int32
    featureCommandIsDone.argtypes = (c_void_p,                          # handle
                                     c_char_p,                          # name of the command feature
                                     POINTER(c_bool))                   # pointer to a result bool

    # announce frames to the API that may be queued for frame capturing later
    frameAnnounce = _vimbaDLL.VmbFrameAnnounce
    frameAnnounce.restype = c_int32
    frameAnnounce.argtypes = (c_void_p,                                # camera handle
                              # pointer to frame
                              POINTER(structs.VimbaFrame),
                              c_uint32)                                # size of frame

    # callback for frame queue
    frameDoneCallback = CB_FUNCTYPE(c_void_p,                     # Return Type
                                    c_void_p,                     # Camera Hanlde
                                    POINTER(structs.VimbaFrame))  # Pointer to frame

    # revoke a frame from the API
    frameRevoke = _vimbaDLL.VmbFrameRevoke
    frameRevoke.restype = c_int32
    frameRevoke.argtypes = (c_void_p,                                # camera handle
                            POINTER(structs.VimbaFrame))            # pointer to frame

    # revoke all frames assigned to a certain camera
    frameRevokeAll = _vimbaDLL.VmbFrameRevokeAll
    frameRevokeAll.restype = c_int32
    # camera handle
    frameRevokeAll.argtypes = (c_void_p,)

    # prepare the API for incoming frames
    captureStart = _vimbaDLL.VmbCaptureStart
    captureStart.restype = c_int32
    # camera handle
    captureStart.argtypes = (c_void_p,)

    # stop the API from being able to receive frames
    captureEnd = _vimbaDLL.VmbCaptureEnd
    captureEnd.restype = c_int32
    # camera handle
    captureEnd.argtypes = (c_void_p,)

    # queue frames that may be filled during frame capturing
    captureFrameQueue = _vimbaDLL.VmbCaptureFrameQueue
    captureFrameQueue.restype = c_int32
    captureFrameQueue.argtypes = (c_void_p,
                                  POINTER(structs.VimbaFrame),
                                  c_void_p)                            # callback

    # wait for a queued frame to be filled (or dequeued)
    captureFrameWait = _vimbaDLL.VmbCaptureFrameWait
    captureFrameWait.restype = c_int32
    captureFrameWait.argtypes = (c_void_p,                            # camera handle
                                 POINTER(structs.VimbaFrame),
                                 c_uint32)                            # timeout

    # flush the capture queue
    captureQueueFlush = _vimbaDLL.VmbCaptureQueueFlush
    captureQueueFlush.restype = c_int32
    # camera handle
    captureQueueFlush.argtypes = (c_void_p,)

    # list interfaces
    interfacesList = _vimbaDLL.VmbInterfacesList
    interfacesList.restype = c_int32
    interfacesList.argtypes = (POINTER(structs.VimbaInterfaceInfo),        # pointer to interface info structure
                               # length of list
                               c_uint32,
                               # pointer to number of interfaces
                               POINTER(c_uint32),
                               c_uint32)

    # open interface
    interfaceOpen = _vimbaDLL.VmbInterfaceOpen
    interfaceOpen.restype = c_int32
    interfaceOpen.argtypes = (c_char_p,                                # unique id
                              c_void_p)                                # handle

    # close interface
    interfaceClose = _vimbaDLL.VmbInterfaceClose
    interfaceClose.restype = c_int32
    interfaceClose.argtypes = (c_void_p,)                            # handle

    # read from register
    registersRead = _vimbaDLL.VmbRegistersRead
    registersRead.restype = c_int32
    registersRead.argtypes = (c_void_p,                                # handle
                              # read count
                              c_uint32,
                              # pointer to address array
                              POINTER(c_uint64),
                              # pointer to data array
                              POINTER(c_uint64),
                              POINTER(c_uint32))                    # pointer to num complete reads

    # write to register
    registersWrite = _vimbaDLL.VmbRegistersWrite
    registersWrite.restype = c_int32
    registersWrite.argtypes = (c_void_p,                            # handle
                               # write count
                               c_uint32,
                               # pointer to address array
                               POINTER(c_uint64),
                               # pointer to data array
                               POINTER(c_uint64),
                               POINTER(c_uint32))                    # pointer to num complete write


class VimbaC_MemoryBlock(object):

    """
    Just a memory block object for dealing
    neatly with C memory allocations.
    """

    @property
    def block(self):
        return c_void_p(addressof(self._block))

    def __init__(self, blockSize):
        self._block = create_string_buffer(blockSize)

        # this seems to be None if too much memory is requested
        if self._block is None:
            raise VimbaException(-51)

    def __del__(self):
        del self._block
