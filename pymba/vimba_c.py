from sys import platform as sys_plat
import platform
import os
from ctypes import *


if sys_plat == "win32":

    def find_win_dll(arch):
        """ Finds the highest versioned windows dll for the specified architecture. """
        dlls = []

        filename = 'VimbaC.dll'

        # look in local working directory first
        if os.path.isfile(filename):
            dlls.append(filename)

        if not dlls:
            if 'VIMBA_HOME' in os.environ:
                candidate = os.environ['VIMBA_HOME'] + r'\VimbaC\Bin\Win%i\VimbaC.dll' % (arch)
                if os.path.isfile(candidate):
                    dlls.append(candidate)

        if not dlls:
            bases = [
                r'C:\Program Files\Allied Vision Technologies\AVTVimba_%i.%i\VimbaC\Bin\Win%i\VimbaC.dll',
                r'C:\Program Files\Allied Vision\Vimba_%i.%i\VimbaC\Bin\Win%i\VimbaC.dll'
            ]
            for base in bases:
                for major in range(4):
                    for minor in range(10):
                        candidate = base % (major, minor, arch)
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
    
    def find_so(platform, genicam_path):
        vimbaC_found = False
        for tlPath in [p for p in os.environ.get(genicam_path).split(":") if p]:
            vimba_dir = "/".join(tlPath.split("/")[1:-3])
            vimbaC_path = "/" + vimba_dir + "/VimbaC/DynamicLib/" + platform + "/libVimbaC.so"
            if os.path.isfile(vimbaC_path):
                vimbaC_found = True
                break
        if not vimbaC_found:
            raise OSError('No libVimbaC.so found')
        return vimbaC_path

    if 'x86_64' in os.uname()[4]:
        assert os.environ.get(
            "GENICAM_GENTL64_PATH"), "you need your GENICAM_GENTL64_PATH environment set.  Make sure you have Vimba installed, and you have loaded the /etc/profile.d/ scripts"
        vimbaC_path = find_so('x86_64bit', "GENICAM_GENTL64_PATH")
    elif 'x86_32' in os.uname()[4]:
        print("Warning: x86_32 reached!")
        assert os.environ.get(
            "GENICAM_GENTL32_PATH"), "you need your GENICAM_GENTL32_PATH environment set.  Make sure you have Vimba installed, and you have loaded the /etc/profile.d/ scripts"
        vimbaC_path = find_so('x86_32bit', 'GENICAM_GENTL32_PATH')
    elif 'arm' in os.uname()[4]:
        assert os.environ.get(
            "GENICAM_GENTL32_PATH"), "you need your GENICAM_GENTL32_PATH environment set.  Make sure you have Vimba installed, and you have loaded the /etc/profile.d/ scripts"
        vimbaC_path = find_so('arm_32bit', 'GENICAM_GENTL32_PATH')
    elif 'aarch64' in os.uname()[4]:
        assert os.environ.get(
            "GENICAM_GENTL64_PATH"), "you need your GENICAM_GENTL64_PATH environment set.  Make sure you have Vimba installed, and you have loaded the /etc/profile.d/ scripts"
        vimbaC_path = find_so('arm_64bit', "GENICAM_GENTL64_PATH")
    else:
        raise ValueError("Pymba currently doesn't support %s" % os.uname()[4])


# Callback function type
if sys_plat == "win32":
    CALLBACK_FUNCTYPE = WINFUNCTYPE
else:
    CALLBACK_FUNCTYPE = CFUNCTYPE


class NiceStructure(Structure):
    def __repr__(self):
        field_names = (field[0] for field in self._fields_)
        return '{}({})'.format(
            type(self).__name__,
            ", ".join("=".join((field, str(getattr(self, field))))
                      for field in field_names)
        )


class VmbVersionInfo(NiceStructure):
    _fields_ = [
        ('major', c_uint32),
        ('minor', c_uint32),
        ('patch', c_uint32)]


class VmbInterfaceInfo(NiceStructure):
    _fields_ = [
        # Unique identifier for each interface
        ('interfaceIdString', c_char_p),
        # Interface type, see VmbInterfaceType
        ('interfaceType', c_uint32),
        # Interface name, given by the transport layer
        ('interfaceName', c_char_p),
        # Serial number
        ('serialString', c_char_p),
        # Used access mode, see VmbAccessModeType
        ('permittedAccess', c_uint32)]


class VmbCameraInfo(NiceStructure):
    _fields_ = [
        # Unique identifier for each camera
        ('cameraIdString', c_char_p),
        # Name of the camera
        ('cameraName', c_char_p),
        # Model name
        ('modelName', c_char_p),
        # Serial number
        ('serialString', c_char_p),
        # Used access mode, see VmbAccessModeType
        ('permittedAccess', c_uint32),
        # Unique value for each interface or bus
        ('interfaceIdString', c_char_p)]


class VmbFeatureInfo(NiceStructure):
    _fields_ = [
        ('name', c_char_p),
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


class VmbFrame(Structure):
    _fields_ = [
        # ---- IN ----
        # Comprises image and ancillary data
        ('buffer', c_void_p),
        # Size of the data buffer
        ('bufferSize', c_uint32),

        # User context filled during queuing
        ('context', c_void_p * 4),

        # ---- OUT ----
        # Resulting status of the receive operation
        ('receiveStatus', c_int32),
        # Resulting flags of the receive operation
        ('receiveFlags', c_uint32),

        # Size of the image data inside the data buffer
        ('imageSize', c_uint32),
        # Size of the ancillary data inside the data buffer
        ('ancillarySize', c_uint32),

        # Pixel format of the image
        ('pixelFormat', c_uint32),

        # Width of an image
        ('width', c_uint32),
        # Height of an image
        ('height', c_uint32),
        # Horizontal offset of an image
        ('offsetX', c_uint32),
        # Vertical offset of an image
        ('offsetY', c_uint32),

        # Unique ID of this frame in this stream
        ('frameID', c_uint64),
        # Timestamp of the data transfer
        ('timestamp', c_uint64)]


_vimba_lib = dll_loader.LoadLibrary(vimbaC_path)

# ----- The below function signatures are defined in VimbaC.h -----

# callback for frame queue
vmb_frame_callback_func = CALLBACK_FUNCTYPE(c_void_p,
                                            c_void_p,
                                            POINTER(VmbFrame))

vmb_version_query = _vimba_lib.VmbVersionQuery
vmb_version_query.restype = c_int32
vmb_version_query.argtypes = (POINTER(VmbVersionInfo),
                              c_uint32)

vmb_startup = _vimba_lib.VmbStartup
vmb_startup.restype = c_int32

vmb_shutdown = _vimba_lib.VmbShutdown

vmb_cameras_list = _vimba_lib.VmbCamerasList
vmb_cameras_list.restype = c_int32
vmb_cameras_list.argtypes = (POINTER(VmbCameraInfo),
                             c_uint32,
                             POINTER(c_uint32),
                             c_uint32)

vmb_camera_info_query = _vimba_lib.VmbCameraInfoQuery
vmb_camera_info_query.restype = c_int32
vmb_camera_info_query.argtypes = (c_char_p,
                                  POINTER(VmbCameraInfo),
                                  c_uint32)

vmb_camera_open = _vimba_lib.VmbCameraOpen
vmb_camera_open.restype = c_int32
vmb_camera_open.argtypes = (c_char_p,
                            c_uint32,
                            c_void_p)

vmb_camera_close = _vimba_lib.VmbCameraClose
vmb_camera_close.restype = c_int32
vmb_camera_close.argtypes = (c_void_p,)

vmb_features_list = _vimba_lib.VmbFeaturesList
vmb_features_list.restype = c_int32
vmb_features_list.argtypes = (c_void_p,
                              POINTER(VmbFeatureInfo),
                              c_uint32,
                              POINTER(c_uint32),
                              c_uint32)

vmb_feature_info_query = _vimba_lib.VmbFeatureInfoQuery
vmb_feature_info_query.restype = c_int32
vmb_feature_info_query.argtypes = (c_void_p,
                                   c_char_p,
                                   POINTER(VmbFeatureInfo),
                                   c_uint32)

# todo VmbFeatureListAffected
# todo VmbFeatureListSelected
# todo VmbFeatureAccessQuery

vmb_feature_int_get = _vimba_lib.VmbFeatureIntGet
vmb_feature_int_get.restype = c_int32
vmb_feature_int_get.argtypes = (c_void_p,
                                c_char_p,
                                POINTER(c_int64))

vmb_feature_int_set = _vimba_lib.VmbFeatureIntSet
vmb_feature_int_set.restype = c_int32
vmb_feature_int_set.argtypes = (c_void_p,
                                c_char_p,
                                c_int64)

vmb_feature_int_range_query = _vimba_lib.VmbFeatureIntRangeQuery
vmb_feature_int_range_query.restype = c_int32
vmb_feature_int_range_query.argtypes = (c_void_p,
                                        c_char_p,
                                        POINTER(c_int64),
                                        POINTER(c_int64))

# todo VmbFeatureIntIncrementQuery

vmb_feature_float_get = _vimba_lib.VmbFeatureFloatGet
vmb_feature_float_get.restype = c_int32
vmb_feature_float_get.argtypes = (c_void_p,
                                  c_char_p,
                                  POINTER(c_double))

vmb_feature_float_set = _vimba_lib.VmbFeatureFloatSet
vmb_feature_float_set.restype = c_int32
vmb_feature_float_set.argtypes = (c_void_p,
                                  c_char_p,
                                  c_double)

vmb_feature_float_range_query = _vimba_lib.VmbFeatureFloatRangeQuery
vmb_feature_float_range_query.restype = c_int32
vmb_feature_float_range_query.argtypes = (c_void_p,
                                          c_char_p,
                                          POINTER(c_double),
                                          POINTER(c_double))

# todo VmbFeatureFloatIncrementQuery

vmb_feature_enum_get = _vimba_lib.VmbFeatureEnumGet
vmb_feature_enum_get.restype = c_int32
vmb_feature_enum_get.argtypes = (c_void_p,
                                 c_char_p,
                                 POINTER(c_char_p))

vmb_feature_enum_set = _vimba_lib.VmbFeatureEnumSet
vmb_feature_enum_set.restype = c_int32
vmb_feature_enum_set.argtypes = (c_void_p,
                                 c_char_p,
                                 c_char_p)

vmb_feature_enum_range_query = _vimba_lib.VmbFeatureEnumRangeQuery
vmb_feature_enum_range_query.restype = c_int32
vmb_feature_enum_range_query.argtypes = (c_void_p,
                                         c_char_p,
                                         POINTER(c_char_p),
                                         c_uint32,
                                         POINTER(c_uint32))

# todo VmbFeatureEnumIsAvailable
# todo VmbFeatureEnumAsInt
# todo VmbFeatureEnumAsString
# todo VmbFeatureEnumEntryGet

vmb_feature_string_get = _vimba_lib.VmbFeatureStringGet
vmb_feature_string_get.restype = c_int32
vmb_feature_string_get.argtypes = (c_void_p,
                                   c_char_p,
                                   c_char_p,
                                   c_uint32,
                                   POINTER(c_uint32))

vmb_feature_string_set = _vimba_lib.VmbFeatureStringSet
vmb_feature_string_set.restype = c_int32
vmb_feature_string_set.argtypes = (c_void_p,
                                   c_char_p,
                                   c_char_p)

# todo VmbFeatureStringMaxlengthQuery

vmb_feature_bool_get = _vimba_lib.VmbFeatureBoolGet
vmb_feature_bool_get.restype = c_int32
vmb_feature_bool_get.argtypes = (c_void_p,
                                 c_char_p,
                                 POINTER(c_bool))

vmb_feature_bool_set = _vimba_lib.VmbFeatureBoolSet
vmb_feature_bool_set.restype = c_int32
vmb_feature_bool_set.argtypes = (c_void_p,
                                 c_char_p,
                                 c_bool)

vmb_feature_command_run = _vimba_lib.VmbFeatureCommandRun
vmb_feature_command_run.restype = c_int32
vmb_feature_command_run.argtypes = (c_void_p,
                                    c_char_p)

vmb_feature_command_is_done = _vimba_lib.VmbFeatureCommandIsDone
vmb_feature_command_is_done.restype = c_int32
vmb_feature_command_is_done.argtypes = (c_void_p,
                                        c_char_p,
                                        POINTER(c_bool))

# todo VmbFeatureRawGet
# todo VmbFeatureRawSet
# todo VmbFeatureRawLengthQuery
# todo VmbFeatureInvalidationRegister
# todo VmbFeatureInvalidationUnregister

vmb_frame_announce = _vimba_lib.VmbFrameAnnounce
vmb_frame_announce.restype = c_int32
vmb_frame_announce.argtypes = (c_void_p,
                               POINTER(VmbFrame),
                               c_uint32)

vmb_frame_revoke = _vimba_lib.VmbFrameRevoke
vmb_frame_revoke.restype = c_int32
vmb_frame_revoke.argtypes = (c_void_p,
                             POINTER(VmbFrame))

vmb_frame_revoke_all = _vimba_lib.VmbFrameRevokeAll
vmb_frame_revoke_all.restype = c_int32
vmb_frame_revoke_all.argtypes = (c_void_p,)

vmb_capture_start = _vimba_lib.VmbCaptureStart
vmb_capture_start.restype = c_int32
vmb_capture_start.argtypes = (c_void_p,)

vmb_capture_end = _vimba_lib.VmbCaptureEnd
vmb_capture_end.restype = c_int32
vmb_capture_end.argtypes = (c_void_p,)

vmb_capture_frame_queue = _vimba_lib.VmbCaptureFrameQueue
vmb_capture_frame_queue.restype = c_int32
vmb_capture_frame_queue.argtypes = (c_void_p,
                                    POINTER(VmbFrame),
                                    c_void_p)

vmb_capture_frame_wait = _vimba_lib.VmbCaptureFrameWait
vmb_capture_frame_wait.restype = c_int32
vmb_capture_frame_wait.argtypes = (c_void_p,
                                   POINTER(VmbFrame),
                                   c_uint32)

vmb_capture_queue_flush = _vimba_lib.VmbCaptureQueueFlush
vmb_capture_queue_flush.restype = c_int32
vmb_capture_queue_flush.argtypes = (c_void_p,)

vmb_interfaces_list = _vimba_lib.VmbInterfacesList
vmb_interfaces_list.restype = c_int32
vmb_interfaces_list.argtypes = (POINTER(VmbInterfaceInfo),
                                c_uint32,
                                POINTER(c_uint32),
                                c_uint32)

vmb_interface_open = _vimba_lib.VmbInterfaceOpen
vmb_interface_open.restype = c_int32
vmb_interface_open.argtypes = (c_char_p,
                               c_void_p)

vmb_interface_close = _vimba_lib.VmbInterfaceClose
vmb_interface_close.restype = c_int32
vmb_interface_close.argtypes = (c_void_p,)

# todo VmbAncillaryDataOpen
# todo VmbAncillaryDataClose
# todo VmbMemoryRead
# todo VmbMemoryWrite
# todo VmbAncillaryDataOpen

vmb_registers_read = _vimba_lib.VmbRegistersRead
vmb_registers_read.restype = c_int32
vmb_registers_read.argtypes = (c_void_p,
                               c_uint32,
                               POINTER(c_uint64),
                               POINTER(c_uint64),
                               POINTER(c_uint32))

vmb_registers_write = _vimba_lib.VmbRegistersWrite
vmb_registers_write.restype = c_int32
vmb_registers_write.argtypes = (c_void_p,
                                c_uint32,
                                POINTER(c_uint64),
                                POINTER(c_uint64),
                                POINTER(c_uint32))

# todo VmbCameraSettingsSave
# todo VmbCameraSettingsLoad
