from ctypes import byref, sizeof, addressof, create_string_buffer, cast, POINTER, c_ubyte, c_void_p
from typing import Optional, Callable
import numpy as np

from . import camera as _camera
from .vimba_exception import VimbaException
from . import vimba_c


class Frame:
    """
    A Vimba frame.
    """

    def __init__(self, camera: '_camera.Camera'):
        self._camera = camera
        self.pixel_format = self._camera.PixelFormat

        self._vmb_frame = vimba_c.VmbFrame()

        self._c_memory = None
        self._frame_callback = None
        self._frame_callback_wrapper_c = None

    @property
    def data(self) -> vimba_c.VmbFrame:
        return self._vmb_frame

    def announce(self) -> None:
        """
        Announce frames to the API that may be queued for frame capturing later. Should be called
        after the frame is created. Call startCapture after this method.
        """
        # allocate memory for the frame and keep a reference to keep alive
        self._c_memory = create_string_buffer(self._camera.PayloadSize)
        address = c_void_p(addressof(self._c_memory))
        if address is None:
            # this seems to be None if too much memory is requested
            raise VimbaException(VimbaException.ERR_FRAME_BUFFER_MEMORY)

        # tell the frame about the memory
        self.data.buffer = address
        self.data.bufferSize = self._camera.PayloadSize

        error = vimba_c.vmb_frame_announce(self._camera.handle,
                                           byref(self.data),
                                           sizeof(self.data))
        if error:
            raise VimbaException(error)

    def revoke(self) -> None:
        """
        Revoke a frame from the API.
        """
        error = vimba_c.vmb_frame_revoke(self._camera.handle,
                                         byref(self.data))
        if error:
            raise VimbaException(error)

    def queue_for_capture(self, frame_callback: Optional[Callable] = None) -> None:
        """
        Queue frames that may be filled during frame capturing. Call after announceFrame and
        startCapture. Callback must accept argument of type frame. Remember to requeue the frame by
        calling frame.queue_capture() at the end of your callback function.
        """
        self._frame_callback = frame_callback

        # define a callback wrapper here so it doesn't bind self
        def frame_callback_wrapper(camera_handle, frame_ptr):
            # call the user's callback with the self bound outside the wrapper
            # ignore the frame pointer since we already know the callback refers to this frame
            self._frame_callback(self)

        if self._frame_callback is None:
            self._frame_callback_wrapper_c = None
        else:
            # keep a reference to prevent gc issues
            self._frame_callback_wrapper_c = vimba_c.vmb_frame_callback_func(frame_callback_wrapper)

        error = vimba_c.vmb_capture_frame_queue(self._camera.handle,
                                                byref(self.data),
                                                self._frame_callback_wrapper_c)
        if error:
            raise VimbaException(error)

    def wait_for_capture(self, timeout_ms: Optional[int] = 2000) -> None:
        """
        Wait for a queued frame to be filled (or dequeued). Call after an acquisition command.
        :param timeout_ms: time out in milliseconds.
        """
        error = vimba_c.vmb_capture_frame_wait(self._camera.handle,
                                               byref(self.data),
                                               timeout_ms)
        if error:
            raise VimbaException(error)

    def buffer_data(self):
        """
        Get a copy of the frame's buffer data as a ctypes c_ubyte array.
        """
        # create a ctypes pointer to the buffer
        buffer_ptr = cast(self.data.buffer, POINTER(c_ubyte * self.data.bufferSize))

        # contents always returns a copy
        return buffer_ptr.contents

    def buffer_data_numpy(self) -> np.ndarray:
        """
        Get a copy of the frame's buffer data as a NumPy array. This can easily be used with OpenCV.
        """
        # todo pixel formats larger than 8-bit

        return np.ndarray(buffer=self.buffer_data(),
                          dtype=np.uint8,
                          shape=(self.data.height, self.data.width))
