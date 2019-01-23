from ctypes import byref, sizeof, addressof, create_string_buffer, cast, POINTER, c_ubyte, c_void_p
from typing import Optional
import warnings
try:
    import numpy as np
except ImportError:
    warnings.warn('could not import numpy, some Frame methods may not work.')

from .camera import Camera
from .vimba_exception import VimbaException
from . import vimba_c


# Map pixel formats to bytes per pixel.
PIXEL_FORMATS = {
    "Mono8": 1,
    "Mono12": 2,
    # untested
    "Mono12Packed": 1.5,
    "Mono14": 2,
    "Mono16": 2,
    "RGB8": 3,
    "RGB8Packed": 3,
    "BGR8Packed": 3,
    "RGBA8Packed": 4,
    "BGRA8Packed": 4,
    # untested
    "YUV411Packed": 4 / 3.0,
    "YUV422Packed": 2,
    "YUV444Packed": 3,
    "BayerRG8": 1,
    "BayerRG12": 2,
    "BayerGR8": 1,
    "BayerGR12": 2,
    # untested
    "BayerGR12Packed": 1.5,
}


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

    def __del__(self):
        del self._block


class Frame:
    """
    A Vimba frame.
    """

    def __init__(self, camera: Camera):
        self._camera = camera
        self._handle = camera.handle

        # get frame sizes
        self.payload_size = self._camera.PayloadSize
        self.width = self._camera.Width
        self.height = self._camera.Height
        self.pixel_bytes = PIXEL_FORMATS[self._camera.PixelFormat]

        # frame structure
        self._frame = vimba_c.VmbFrame()

        self._c_mem = None

    def announce(self):
        """
        Announce frames to the API that may be queued for frame capturing later. Should be called after the frame is
        created. Call startCapture after this method.
        """
        # keep this reference to keep block alive for life of frame
        self._c_mem = MemoryBlock(self.payload_size)
        # set buffer to have length of expected payload size
        self._frame.buffer = self._c_mem.block

        # set buffer size to expected payload size
        self._frame.bufferSize = self.payload_size

        error = vimba_c.vmb_frame_announce(self._handle,
                                           byref(self._frame),
                                           sizeof(self._frame))
        if error:
            raise VimbaException(error)

    def revoke(self):
        """
        Revoke a frame from the API.
        """
        error = vimba_c.vmb_frame_revoke(self._handle,
                                         byref(self._frame))
        if error:
            raise VimbaException(error)

    def queue_capture(self, frame_callback: Optional[bool] = None) -> None:
        """
        Queue frames that may be filled during frame capturing. Call after announceFrame and startCapture. Callback
        must accept argument of type frame. Remember to requeue the frame by calling frame.queue_capture() at the end
        of your callback function.
        """
        self._frame_callback = frame_callback

        # define a callback wrapper here so it doesn't bind self
        def frame_callback_wrapper(cam_handle, p_frame):
            # call the user's callback with the self bound outside the wrapper
            # ignore the frame pointer since we already know the callback
            # refers to this frame
            self._frame_callback(self)

        if self._frame_callback is None:
            self._frame_callback_wrapper_c = None
        else:
            # keep a reference to prevent gc issues
            self._frame_callback_wrapper_c = vimba_c.vmb_frame_callback(frame_callback_wrapper)

        error = vimba_c.vmb_capture_frame_queue(self._handle,
                                                byref(self._frame),
                                                self._frame_callback_wrapper_c)
        if error:
            raise VimbaException(error)

    def wait_capture(self, timeout_ms: Optional[int] = 2000) -> int:
        """
        Wait for a queued frame to be filled (or dequeued). Call after an acquisition command.
        :param timeout_ms: time out in milliseconds.
        """
        error = vimba_c.vmb_capture_frame_wait(self._handle,
                                               byref(self._frame),
                                               timeout_ms)

        # error to be processed by the end user for this function.
        # Prevents system for breaking for example on a hardware trigger timeout

        # todo raise error instead?

        return error

    def get_buffer_data(self) -> c_ubyte * int:
        """
        Retrieve buffer data in a useful format.
        """
        # cast frame buffer memory contents to a usable type
        data = cast(self._frame.buffer, POINTER(c_ubyte * self.payload_size))

        # make array of c_ubytes from buffer
        image_bytes = int(self.height * self.width * self.pixel_bytes)
        return (c_ubyte * image_bytes).from_address(addressof(data.contents))

    def get_image(self) -> np.ndarray:
        """
        Returns the frame's image data as a NumPy array.
        """
        data = cast(self._frame.buffer, POINTER(c_ubyte * self._frame.imageSize))
        return np.ndarray(buffer=data.contents, dtype=np.uint8, shape=(self._frame.height, self._frame.width))

    @property
    def timestamp(self) -> int:
        return self._frame.timestamp

    @property
    def receive_status(self) -> int:
        return self._frame.receiveStatus
