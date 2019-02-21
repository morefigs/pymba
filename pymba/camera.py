from ctypes import byref, sizeof, c_uint32
from typing import Optional, List, Callable
import gc

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

SINGLE_FRAME = 'SingleFrame'
CONTINUOUS = 'Continuous'


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

        # remember state
        self._is_armed = False
        self._is_acquiring = False
        self._acquisition_mode = None

        # frame to reuse when in single frame mode
        self._single_frame = None

        # user registered callback function
        self._user_callback = None

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

    def open(self,
             camera_access_mode: Optional[int] = VimbaObject.VMB_ACCESS_MODE_FULL,
             adjust_packet_size: Optional[bool] = True):
        """
        Open the camera with requested access mode. Adjusts packet size by default.
        """
        error = vimba_c.vmb_camera_open(self.camera_id.encode(),
                                        camera_access_mode,
                                        byref(self._handle))
        if error:
            raise VimbaException(error)

        # may experience issues with camera comms if not called
        if adjust_packet_size:
            self.GVSPAdjustPacketSize()

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

    def new_frame(self) -> Frame:
        """
        Creates and returns a new frame object. Multiple frames per camera can therefore be returned.
        """
        return Frame(self)

    def arm(self, mode: str, callback: Optional[Callable] = None, frame_buffer_size: Optional[int] = 10) -> None:
        """
        Arm the camera by starting the capture engine and creating frames.
        :param mode: Either 'SingleFrame' to acquire a single frame or 'Continuous' for streaming frames.
        :param callback: A function reference to call when each frame is ready. Applies to 'Continuous' acquisition
        mode only. The callback function should execute relatively quickly to avoid dropping frames (if the camera
        captures a frame but no frame is currently queued for capture then the frame will be dropped. Therefore the
        callback function should execute (on average) at least as fast as the camera frame rate. It may be desirable
        for the callback to copy frame data and pass the data to a separate thread/process for processing.
        :param frame_buffer_size: number of frames to create and use for the acquisition buffer. Increasing this may
        help if frames are being dropped.
        """
        if self._is_armed:
            raise VimbaException(VimbaException.ERR_INVALID_CAMERA_MODE)

        if mode not in (SINGLE_FRAME, CONTINUOUS):
            raise ValueError('unknown mode')

        # set and cache mode
        self.AcquisitionMode = mode
        self._acquisition_mode = mode

        if mode == SINGLE_FRAME:
            self._arm_single_frame()
        elif mode == CONTINUOUS:
            if callback is None:
                raise ValueError('a callback function must be provided in continuous mode')
            self._arm_continuous(callback, frame_buffer_size)

        self._is_armed = True

    def _arm_single_frame(self) -> None:
        self._single_frame = self.new_frame()
        self._single_frame.announce()

        self.start_capture()

    def acquire_frame(self) -> Frame:
        """
        Acquire and return a single frame when the camera is armed in 'SingleFrame' acquisition mode. Can be called
        multiple times in a row, but don't call again until the frame has been copied or processed the internal frame
        object is reused.
        """
        if not self._is_armed or self._acquisition_mode != SINGLE_FRAME:
            raise VimbaException(VimbaException.ERR_INVALID_CAMERA_MODE)

        # capture a single frame
        self._single_frame.queue_for_capture()
        self.AcquisitionStart()
        self._single_frame.wait_for_capture()
        self.AcquisitionStop()

        return self._single_frame

    def _arm_continuous(self, callback: Callable, frame_buffer_size: int) -> None:
        self._user_callback = callback

        # create frame buffer and announce frames to camera
        _frame_buffer = tuple(self.new_frame() for _ in range(frame_buffer_size))
        for frame in _frame_buffer:
            frame.announce()

        self.start_capture()

        # queue
        for frame in _frame_buffer:
            frame.queue_for_capture(self._streaming_callback)

    def start_frame_acquisition(self) -> None:
        """
        Acquire and stream frames (to the specified callback function) indefinitely when the camera is armed in
        'Continuous' acquisition mode.
        """
        # no need to check self._is_acquiring
        if not self._is_armed or self._acquisition_mode != CONTINUOUS:
            raise VimbaException(VimbaException.ERR_INVALID_CAMERA_MODE)

        # safe to call multiple times
        self.AcquisitionStart()
        self._is_acquiring = True

    def _streaming_callback(self, frame: Frame) -> None:
        """
        Called upon the frame ready event. Wraps the user's callback and requeues the frame.
        """
        self._user_callback(frame)

        # streaming may have stopped by now, especially if callback is long running
        if self._is_armed and self._acquisition_mode == CONTINUOUS:
            frame.queue_for_capture(self._streaming_callback)

    def stop_frame_acquisition(self) -> None:
        """
        Stop acquiring and streaming frames.
        """
        # implies both is armed and in continuous mode
        if self._is_acquiring:
            self._is_acquiring = False
            self.AcquisitionStop()

    def disarm(self) -> None:
        """
        Disarm the camera by stopping the capture engine and cleaning up frames.
        """
        # among other things this prevents callback from requeuing frames
        self._is_armed = False

        # automatically stop acquisition if required
        if self._is_acquiring:
            self.stop_frame_acquisition()

        # clean up
        self.end_capture()
        self.flush_capture_queue()
        self.revoke_all_frames()

        self._single_frame = None

        # encourage garbage collection of frame buffer memory
        gc.collect()
