from .vimba_object import VimbaObject


class System(VimbaObject):
    """
    A Vimba system object. This class provides the minimal access to Vimba functions required to
    control the system.
    """
    def __init__(self, vimba):
        super().__init__(vimba, handle=1)
