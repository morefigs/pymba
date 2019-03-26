from ctypes import sizeof
from typing import List, Union

from .vimba_exception import VimbaException
from .system import System
from .interface import Interface, interface_ids
from .camera import Camera, camera_ids
from . import vimba_c


class Vimba:
    """
    Python wrapper for Allied Vision's Vimba C API.
    """

    @staticmethod
    def version() -> str:
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

    def __init__(self):
        # create own system singleton object
        self._system = System(self)
        self._interfaces = {}
        self._cameras = {}

    def __enter__(self):
        """
        Define vimba context for safe execution.
        """
        self.startup()
        return self

    def __exit__(self, type_, value, traceback):
        """
        Shutdown Vimba when the with context is left. This allows cleanup
        when an error occurs in the main program. The system will not hang
        on a kernel call after an exception.
        """
        self.shutdown()

    def startup(self):
        """
        Initialize the Vimba C API.
        """
        error = vimba_c.vmb_startup()
        if error:
            raise VimbaException(error)

        # automatically check for the presence of a GigE transport layer
        if self.system().GeVTLIsPresent:
            self.system().GeVDiscoveryAllDuration = 250
            self.system().GeVDiscoveryAllOnce()

    @staticmethod
    def shutdown():
        """
        Perform a shutdown on the API.
        """
        vimba_c.vmb_shutdown()

    def system(self) -> System:
        """
        Get the system object.
        """
        return self._system

    @staticmethod
    def interface_ids():
        return interface_ids()

    def interface(self, interface_id: Union[str, int]) -> Interface:
        """
        Gets interface object based on interface ID string or index. Will not recreate interface
        object if it already exists.
        :param interface_id: the ID or the index of the interface.
        """
        # if index is provided, look up the camera id using the index
        if isinstance(interface_id, int):
            interface_id = interface_ids()[interface_id]

        if interface_id in self._interfaces:
            return self._interfaces[interface_id]

        # cache interface instances
        interface = Interface(self, interface_id)
        self._interfaces[interface_id] = interface

        return interface

    @staticmethod
    def camera_ids() -> List[str]:
        return camera_ids()

    def camera(self, camera_id: Union[str, int]) -> Camera:
        """
        Gets camera object based on camera ID string or index. Will not recreate camera object if
        it already exists.
        :param camera_id: the ID or the index of the camera object to get. This can be an ID or
        e.g. a serial number. Check the Vimba documentation for other possible values.
        """
        # if index is provided, look up the camera id using the index
        if isinstance(camera_id, int):
            camera_id = camera_ids()[camera_id]

        if camera_id in self._cameras:
            return self._cameras[camera_id]

        # cache camera instance
        camera = Camera(self, camera_id)
        self._cameras[camera_id] = camera

        return camera
