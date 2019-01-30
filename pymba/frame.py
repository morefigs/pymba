from ctypes import byref, sizeof, addressof, create_string_buffer, cast, POINTER, c_ubyte, c_void_p
from typing import Optional, Callable
import numpy as np

from . import camera as _camera
from .vimba_exception import VimbaException
from . import vimba_c


class MemoryBlock:
    """
    A memory block object for dealing neatly with C memory allocations.
    """

    @property
    def block(self):
        return c_void_p(addressof(self._block))

    def __init__(self, block_size):
        self._block = create_string_buffer(block_size)

        # this seems to be None if too much memory is requested
        if self._block is None:
            raise VimbaException(VimbaException.ERR_FRAME_BUFFER_MEMORY)


class Frame:
    """
    A Vimba frame.
    """

    def __init__(self, camera: '_camera.Camera'):
        self._camera = camera

        self._vmb_frame = vimba_c.VmbFrame()

        self._c_mem = None
        self._frame_callback = None
        self._frame_callback_wrapper_c = None

    def announce(self) -> None:
        """
        Announce frames to the API that may be queued for frame capturing later. Should be called after the frame is
        created. Call startCapture after this method.
        """
        # keep this reference to keep block alive for life of frame
        self._c_mem = MemoryBlock(self._camera.PayloadSize)

        # set buffer to have length of expected payload size
        self._vmb_frame.buffer = self._c_mem.block

        # set buffer size to expected payload size
        self._vmb_frame.bufferSize = self._camera.PayloadSize

        error = vimba_c.vmb_frame_announce(self._camera.handle,
                                           byref(self._vmb_frame),
                                           sizeof(self._vmb_frame))
        if error:
            raise VimbaException(error)

    def revoke(self) -> None:
        """
        Revoke a frame from the API.
        """
        error = vimba_c.vmb_frame_revoke(self._camera.handle,
                                         byref(self._vmb_frame))
        if error:
            raise VimbaException(error)

    def queue_for_capture(self, frame_callback: Optional[Callable] = None) -> None:
        """
        Queue frames that may be filled during frame capturing. Call after announceFrame and startCapture. Callback
        must accept argument of type frame. Remember to requeue the frame by calling frame.queue_capture() at the end
        of your callback function.
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
                                                byref(self._vmb_frame),
                                                self._frame_callback_wrapper_c)
        if error:
            raise VimbaException(error)

    def wait_for_capture(self, timeout_ms: Optional[int] = 2000) -> None:
        """
        Wait for a queued frame to be filled (or dequeued). Call after an acquisition command.
        :param timeout_ms: time out in milliseconds.
        """
        error = vimba_c.vmb_capture_frame_wait(self._camera.handle,
                                               byref(self._vmb_frame),
                                               timeout_ms)
        if error:
            raise VimbaException(error)

    def image_pointer(self):
        """
        Get a pointer to the frame's image data as a ctypes c_ubyte array pointer.
        """
        return cast(self._vmb_frame.buffer, POINTER(c_ubyte * self._vmb_frame.bufferSize))

    def image_buffer(self):
        """
        Get a copy of the frame's image data as a ctypes c_ubyte array.
        """
        return self.image_pointer().contents

    def image_numpy_array(self) -> np.ndarray:
        """
        Get the frame's image data as a NumPy array, which can be used with OpenCV.
        """
        # todo pixel formats larger than 8-bit

        return np.ndarray(buffer=self.image_buffer(),
                          dtype=np.uint8,
                          shape=(self._vmb_frame.height, self._vmb_frame.width))
