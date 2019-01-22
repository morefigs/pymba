from ctypes import byref, sizeof, c_void_p, c_uint32, c_uint64, c_bool
from typing import Union, Tuple, List, Optional

from .vimba_exception import VimbaException
from .vimba_feature import VimbaFeature
from . import vimba_c


class VimbaObject:
    """
    A Vimba object has a handle and features associated with it. Objects include System, Camera, Interface and
    AncillaryData. Features are automatically readable as instance attributes.
    """

    VMB_ACCESS_MODE_NONE = 0
    VMB_ACCESS_MODE_FULL = 1
    VMB_ACCESS_MODE_READ = 2
    VMB_ACCESS_MODE_CONFIG = 4
    VMB_ACCESS_MODE_LITE = 8

    def __init__(self, handle: Optional[int] = None):
        if handle is None:
            self._handle = c_void_p()
        else:
            self._handle = c_void_p(handle)

        # can't be populated until device is opened
        self._vmb_features_info = None

    @property
    def handle(self):
        return self._handle

    # override getattr for undefined attributes
    def __getattr__(self, attr):
        # if a feature value requested (requires object (camera) open)
        if attr in self.get_feature_names():
            return VimbaFeature(attr, self._handle).value

        # otherwise don't know about it
        raise AttributeError(''.join(["'VimbaObject' has no attribute '", attr, "'"]))

    # override setattr for undefined attributes
    def __setattr__(self, attr, val):

        # set privates as normal
        # check this first to allow all privates to set normally
        # and avoid recursion errors
        if attr.startswith('_'):
            super(VimbaObject, self).__setattr__(attr, val)

        # if it's an actual camera feature (requires camera open)
        elif attr in self.get_feature_names():
            VimbaFeature(attr, self._handle).value = val

        # otherwise just set the attribute value as normal
        else:
            super(VimbaObject, self).__setattr__(attr, val)

    def _get_feature_infos(self) -> List[vimba_c.VmbFeatureInfo]:
        """
        Gets feature info of all available features. Will
        cause error if object/camera is not opened.

        :returns: list -- feature info for available features.
        """
        # check it's populated as can't populate it in __init__
        if self._vmb_features_info is None:
            vmb_feature_info = vimba_c.VmbFeatureInfo()
            num_found = c_uint32(-1)

            # call once to get number of available features
            error = vimba_c.vmb_features_list(self._handle,
                                              None,
                                              0,
                                              byref(num_found),
                                              sizeof(vmb_feature_info))
            if error:
                raise VimbaException(error)

            # number of features specified by Vimba
            num_features = num_found.value
            vmb_feature_infos = (vimba_c.VmbFeatureInfo * num_features)()

            # call again to get the features
            error = vimba_c.vmb_features_list(self._handle,
                                              vmb_feature_infos,
                                              num_features,
                                              byref(num_found),
                                              sizeof(vmb_feature_info))
            if error:
                raise VimbaException(error)

            self._vmb_features_info = list(vmb_feature_info for vmb_feature_info in vmb_feature_infos)

        return self._vmb_features_info

    def get_feature_names(self) -> List[str]:
        """
        Get names of all available features.
        """
        return list(feature_info.name for feature_info in self._get_feature_infos())

    def get_feature_info(self, feature_name: str) -> vimba_c.VmbFeatureInfo:
        """
        Gets feature info object of specified feature.
        :param feature_name: the name of the feature.
        """
        # don't do this live as we already have this info
        # return info object, if it exists
        for vmb_feature_info in self._get_feature_infos():
            if vmb_feature_info.name == feature_name:
                return vmb_feature_info
        # otherwise raise error
        raise VimbaException(VimbaException.ERR_FEATURE_NOT_FOUND)

    # don't think we ever need to return a feature object...
    # def getFeature(self, featureName):

    def get_feature_range(self, feature_name: str) -> Union[Tuple[float, float], Tuple[int, int], List[str]]:
        """
        Get valid range of feature values.
        :param feature_name: name of the feature to query.
        :returns: tuple -- range as (feature min value, feature max value, for int or float features only).
                  list -- names of possible enum values (for enum features only).
        """
        # shouldn't cache this
        return VimbaFeature(feature_name, self._handle).range

    def run_feature_command(self, feature_name: str) -> None:
        """
        Run a feature command.
        :param feature_name: the name of the feature.
        """
        # run a command
        error = vimba_c.vmb_feature_command_run(self._handle,
                                                feature_name.encode())
        if error:
            raise VimbaException(error)

    def feature_command_is_done(self, feature_name: str) -> bool:
        is_done = c_bool()
        error = vimba_c.vmb_feature_command_is_done(self._handle,
                                                    feature_name.encode(),
                                                    byref(is_done))
        if error:
            raise VimbaException(error)

        return is_done.value

    def read_register(self, address: int) -> int:
        # note that the underlying Vimba function allows reading of an array
        # of registers, but only one address/value at a time is implemented
        # here
        """
        Read from a register of the module (camera) and return its value.
        :param address: the address of the register to read.
        """
        read_count = 1

        # todo expects bytes not int

        reg_address = c_uint64(int(address, 16))

        reg_data = c_uint64()
        num_complete_reads = c_uint32()

        error = vimba_c.vmb_registers_read(self.handle,
                                           read_count,
                                           byref(reg_address),
                                           byref(reg_data),
                                           byref(num_complete_reads))
        if error:
            raise VimbaException(error)

        return reg_data.value

    def write_register(self, address: int, value: int) -> None:
        # note that the underlying Vimba function allows writing of an array
        # of registers, but only one address/value at a time is implemented
        # here
        """
        Write to a register of the module (camera).
        :param address: the address of the register to read.
        :param value: the value to set in hex.
        """
        write_count = 1

        # todo expects bytes not int

        reg_address = c_uint64(int(address, 16))
        reg_data = c_uint64(int(value, 16))

        num_complete_writes = c_uint32()

        error = vimba_c.vmb_registers_write(self.handle,
                                            write_count,
                                            byref(reg_address),
                                            byref(reg_data),
                                            byref(num_complete_writes))
        if error:
            raise VimbaException(error)
