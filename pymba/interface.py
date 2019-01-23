from ctypes import byref

from .vimba_object import VimbaObject
from .vimba_exception import VimbaException
from . import vimba_c


class Interface(VimbaObject):
    """
    A Vimba interface object. This class provides the minimal access
    to Vimba functions required to control the interface.
    """

    def __init__(self, id_string: str):
        self._id_string = id_string.encode()
        super().__init__()

    @property
    def id_string(self):
        return self._id_string.decode()

    def open(self):
        """
        Open the interface.
        """
        error = vimba_c.vmb_interface_open(self._id_string,
                                           byref(self._handle))
        if error:
            raise VimbaException(error)

    def close(self):
        """
        Close the interface.
        """
        error = vimba_c.vmb_interface_close(self._handle)
        if error:
            raise VimbaException(error)
