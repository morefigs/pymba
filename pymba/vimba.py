from ctypes import byref, sizeof, c_uint32
from typing import List

from .vimba_exception import VimbaException
from .vimba_system import VimbaSystem
from .vimba_camera import VimbaCamera
from .vimba_interface import VimbaInterface
from . import vimba_c


class Vimba(object):
    """
    Python wrapper for Allied Vision's Vimba C API.
    """

    # todo - assign camera info and feature info as own object properties

    def __init__(self):
        # create own system singleton object
        self._system = VimbaSystem()
        self._vmb_interface_infos = None
        self._interfaces = {}
        self._cameras = {}

    def __enter__(self):
        """
        Define vimba context for safe execution.
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

    @property
    def system(self) -> VimbaSystem:
        """
        Get the system object.
        """
        return self._system

    @property
    def version(self) -> str:
        """
        Retrieve the version number of the Vimba C API.
        """
        vmb_version_info = vimba_c.VmbVersionInfo()
        error = vimba_c.vmb_version_query(vmb_version_info, sizeof(vmb_version_info))
        if error:
            raise VimbaException(error)

        return '.'.join(str(x) for x in (vmb_version_info.major,
                                         vmb_version_info.minor,
                                         vmb_version_info.patch))

    def startup(self):
        """
        Initialize the Vimba C API.
        """
        error = vimba_c.vmb_startup()
        if error:
            raise VimbaException(error)

    def shutdown(self):
        """
        Perform a shutdown on the API.
        """
        vimba_c.vmb_shutdown()

    def _get_interface_infos(self) -> List[vimba_c.VmbInterfaceInfo]:
        """
        Gets interface info of all available interfaces.
        """

        # todo is this caching required/harmful?

        if self._vmb_interface_infos is None:
            num_found = c_uint32(-1)

            # call once just to get the number of interfaces
            error = vimba_c.vmb_interfaces_list(None,
                                                0,
                                                byref(num_found),
                                                sizeof(vimba_c.VmbInterfaceInfo))
            if error:
                raise VimbaException(error)

            # call again to get the features
            num_interfaces = num_found.value
            vmb_interface_infos = (vimba_c.VmbInterfaceInfo * num_interfaces)()
            error = vimba_c.vmb_interfaces_list(vmb_interface_infos,
                                                num_interfaces,
                                                byref(num_found),
                                                sizeof(vimba_c.VmbInterfaceInfo))
            if error:
                raise VimbaException(error)

            self._vmb_interface_infos = list(vmb_interface_info for vmb_interface_info in vmb_interface_infos)

        return self._vmb_interface_infos

    def _get_camera_infos(self) -> List[vimba_c.VmbCameraInfo]:
        """
        Gets camera info of all attached cameras.
        """
        vmb_camera_info = vimba_c.VmbCameraInfo()
        num_found = c_uint32(-1)

        # call once just to get the number of cameras
        error = vimba_c.vmb_cameras_list(byref(vmb_camera_info),
                                         0,
                                         byref(num_found),
                                         sizeof(vmb_camera_info))
        if error and error != -9:
            raise VimbaException(error)

        num_cameras = num_found.value

        # call again to get the features
        vmb_camera_infos = (vimba_c.VmbCameraInfo * num_cameras)()
        error = vimba_c.vmb_cameras_list(vmb_camera_infos,
                                         num_cameras,
                                         byref(num_found),
                                         sizeof(vmb_camera_info))
        if error:
            raise VimbaException(error)
        return list(vmb_camera_info for vmb_camera_info in vmb_camera_infos)

    def get_interface_ids(self) -> List[str]:
        """
        Gets IDs of all available interfaces.
        """
        return list(vmb_interface_info.id_string for vmb_interface_info in self._get_interface_infos())

    def get_camera_ids(self) -> List[str]:
        """
        Gets IDs of all available cameras.
        """
        return list(camera_info.id_string.decode() for camera_info in self._get_camera_infos())

    def _get_interface_info(self, id_string: str) -> vimba_c.VmbInterfaceInfo:
        """
        Gets interface info object of specified interface.
        :param id_string: the ID of the interface object to get.
        """
        # don't do this live as we already have this info
        # return info object if it exists
        for vmb_interface_info in self._get_interface_infos():

            # todo broken lookup on info objects

            if vmb_interface_info.id_string == id_string:
                return vmb_interface_info
        raise VimbaException(VimbaException.ERR_INTERFACE_NOT_FOUND)

    def _get_camera_info(self, id_string: str) -> vimba_c.VmbCameraInfo:
        """
        Gets camera info object of specified camera.
        :param cameraId: the ID of the camera object to get. This can be an ID or e.g. a serial number. Check the Vimba
                         documentation for other possible values.
        """
        vmb_camera_info = vimba_c.VmbCameraInfo()
        error = vimba_c.vmb_camera_info_query(id_string.encode(),
                                              vmb_camera_info,
                                              sizeof(vmb_camera_info))
        if error:
            raise VimbaException(error)
        return vmb_camera_info

    def get_interface(self, id_string) -> VimbaInterface:
        """
        Gets interface object based on interface ID string. Will not recreate interface object if it already exists.
        :param id_string: the ID of the interface.
        """
        # check ID is valid
        if id_string in self.get_interface_ids():
            # create it if it doesn't exist
            if id_string not in self._interfaces:
                self._interfaces[id_string] = VimbaInterface(id_string)
            return self._interfaces[id_string]
        raise VimbaException(VimbaException.ERR_INTERFACE_NOT_FOUND)

    def get_camera(self, camera_id: str) -> VimbaCamera:
        """
        Gets camera object based on camera ID string. Will not recreate camera object if it already exists.
        :param camera_id: the ID of the camera object to get. This can be an ID or e.g. a serial number. Check the Vimba
                          documentation for other possible values.
        """
        # check ID is valid
        if camera_id in self.get_camera_ids():
            # create it if it doesn't exist
            if camera_id not in self._cameras:
                self._cameras[camera_id] = VimbaCamera(camera_id)
            return self._cameras[camera_id]
        else:
            # the given string might not be a camera ID -> check for other IDs
            vmb_camera_info = vimba_c.VmbCameraInfo()
            error = vimba_c.vmb_camera_info_query(camera_id.encode(),
                                                  vmb_camera_info,
                                                  sizeof(vmb_camera_info))
            if error:
                raise VimbaException(error)
            
            camera_id_string = vmb_camera_info.id_string.decode()
            if camera_id_string not in self._cameras:
                self._cameras[camera_id_string] = VimbaCamera(camera_id_string)
            return self._cameras[camera_id_string]
