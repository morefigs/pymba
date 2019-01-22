from ctypes import byref, sizeof
from typing import Optional

from .vimba_object import VimbaObject
from .vimba_exception import VimbaException
from .vimba_frame import VimbaFrame
from . import vimba_c


class VimbaCamera(VimbaObject):
    """
    A Vimba camera object.
    """

    def __init__(self, id_string: str):
        self._id_string = id_string.encode()
        super().__init__()
        self._info = self._get_info()

    @property
    def id_string(self) -> str:
        return self._id_string.decode()

    def _get_info(self) -> vimba_c.VmbCameraInfo:
        """
        Get info of the camera. Does not require the camera to be opened.
        """
        vmb_camera_info = vimba_c.VmbCameraInfo()
        error = vimba_c.vmb_camera_info_query(self._id_string,
                                              byref(vmb_camera_info),
                                              sizeof(vmb_camera_info))
        if error:
            raise VimbaException(error)

        return vmb_camera_info

    def open(self, camera_access_mode: Optional[int] = VimbaObject.VMB_ACCESS_MODE_FULL):
        """
        Open the camera with requested access mode.
        """
        error = vimba_c.vmb_camera_open(self._id_string,
                                        camera_access_mode,
                                        byref(self._handle))
        if error:
            raise VimbaException(error)

    def close(self):
        """
        Close the camera.
        """
        error = vimba_c.vmb_camera_close(self._handle)
        if error:
            raise VimbaException(error)

    def revoke_all_frames(self):
        """
        Revoke all frames assigned to the camera.
        """
        error = vimba_c.vmb_frame_revoke_all(self._handle)
        if error:
            raise VimbaException(error)

    def start_capture(self):
        """
        Prepare the API for incoming frames.
        """
        error = vimba_c.vmb_capture_start(self._handle)
        if error:
            raise VimbaException(error)

    def end_capture(self):
        """
        Stop the API from being able to receive frames.
        """
        error = vimba_c.vmb_capture_end(self._handle)
        if error:
            raise VimbaException(error)

    def flush_capture_queue(self):
        """
        Flush the capture queue.
        """
        error = vimba_c.vmb_capture_queue_flush(self._handle)
        if error:
            raise VimbaException(error)

    def create_frame(self) -> VimbaFrame:
        """
        Creates and returns a new frame object. Multiple frames per camera can therefore be returned.
        """
        return VimbaFrame(self)
