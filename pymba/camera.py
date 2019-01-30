from ctypes import byref, sizeof, c_uint32
from typing import Optional, List

from .vimba_object import VimbaObject
from .vimba_exception import VimbaException
from .frame import Frame
from . import vimba_c


# todo update this to be more like VmbPixelFormatType in VmbCommonTypes.h
# Map pixel formats to bytes per pixel
PIXEL_FORMAT_BYTES = {
    "Mono8": 1,
    "Mono12": 2,
    "Mono12Packed": 1.5,
    "Mono14": 2,
    "Mono16": 2,
    "RGB8": 3,
    "RGB8Packed": 3,
    "BGR8Packed": 3,
    "RGBA8Packed": 4,
    "BGRA8Packed": 4,
    "YUV411Packed": 4 / 3.0,
    "YUV422Packed": 2,
    "YUV444Packed": 3,
    "BayerRG8": 1,
    "BayerRG12": 2,
    "BayerGR8": 1,
    "BayerGR12": 2,
    "BayerGR12Packed": 1.5,
}


def _camera_infos() -> List[vimba_c.VmbCameraInfo]:
    """
    Gets camera info of all attached cameras.
    """
    # call once just to get the number of cameras
    vmb_camera_info = vimba_c.VmbCameraInfo()
    num_found = c_uint32(-1)
    error = vimba_c.vmb_cameras_list(byref(vmb_camera_info),
                                     0,
                                     byref(num_found),
                                     sizeof(vmb_camera_info))
    if error and error != VimbaException.ERR_DATA_TOO_LARGE:
        raise VimbaException(error)

    # call again to get the features
    num_cameras = num_found.value
    vmb_camera_infos = (vimba_c.VmbCameraInfo * num_cameras)()
    error = vimba_c.vmb_cameras_list(vmb_camera_infos,
                                     num_cameras,
                                     byref(num_found),
                                     sizeof(vmb_camera_info))
    if error:
        raise VimbaException(error)
    return list(vmb_camera_info for vmb_camera_info in vmb_camera_infos)


def _camera_info(id_string: str) -> vimba_c.VmbCameraInfo:
    """
    Gets camera info object of specified camera.
    :param id_string: the ID of the camera object to get. This can be an ID or e.g. a serial number. Check the Vimba
                      documentation for other possible values.
    """
    vmb_camera_info = vimba_c.VmbCameraInfo()
    error = vimba_c.vmb_camera_info_query(id_string.encode(),
                                          vmb_camera_info,
                                          sizeof(vmb_camera_info))
    if error:
        raise VimbaException(error)
    return vmb_camera_info


def camera_ids():
    """
    Gets IDs of all available cameras.
    """
    return list(vmb_camera_info.cameraIdString.decode()
                for vmb_camera_info in _camera_infos())


class Camera(VimbaObject):
    """
    A Vimba camera object.
    """

    def __init__(self, camera_id: str):
        self._camera_id = camera_id
        super().__init__()

    @property
    def handle(self):
        return self._handle

    @property
    def camera_id(self) -> str:
        return self._camera_id

    @property
    def info(self) -> vimba_c.VmbCameraInfo:
        """
        Get info of the camera. Does not require the camera to be opened.
        """
        return _camera_info(self.camera_id)

    def open(self, camera_access_mode: Optional[int] = VimbaObject.VMB_ACCESS_MODE_FULL):
        """
        Open the camera with requested access mode.
        """
        error = vimba_c.vmb_camera_open(self.camera_id.encode(),
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

    def create_frame(self) -> Frame:
        """
        Creates and returns a new frame object. Multiple frames per camera can therefore be returned.
        """
        return Frame(self)
