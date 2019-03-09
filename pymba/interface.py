from ctypes import byref, sizeof, c_uint32
from typing import List

from .vimba_object import VimbaObject
from .vimba_exception import VimbaException
from . import vimba_c


def _interface_infos() -> List[vimba_c.VmbInterfaceInfo]:
    """
    Gets interface info of all available interfaces.
    """
    # call once just to get the number of interfaces
    num_found = c_uint32(-1)
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

    return list(vmb_interface_info for vmb_interface_info in vmb_interface_infos)


def _interface_info(interface_id: str) -> vimba_c.VmbInterfaceInfo:
    """
    Gets interface info object of specified interface.
    :param interface_id: the ID of the interface object to get.
    """
    for vmb_interface_info in _interface_infos():
        if interface_id == vmb_interface_info.interfaceIdString.decode():
            return vmb_interface_info
    raise VimbaException(VimbaException.ERR_INSTANCE_NOT_FOUND)


def interface_ids() -> List[str]:
    """
    Gets IDs of all available interfaces.
    """
    return list(vmb_interface_info.interfaceIdString.decode()
                for vmb_interface_info in _interface_infos())


class Interface(VimbaObject):
    """
    A Vimba interface object. This class provides the minimal access
    to Vimba functions required to control the interface.
    """

    def __init__(self, vimba, interface_id: str):
        if interface_id not in interface_ids():
            raise VimbaException(VimbaException.ERR_INSTANCE_NOT_FOUND)
        self._interface_id = interface_id
        super().__init__(vimba)

    @property
    def interface_id(self):
        return self._interface_id

    @property
    def info(self) -> vimba_c.VmbInterfaceInfo:
        """
        Get info of the interface. Does not require the interface to be opened.
        """
        return _interface_info(self.interface_id)

    def open(self):
        """
        Open the interface.
        """
        error = vimba_c.vmb_interface_open(self.interface_id.encode(),
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
