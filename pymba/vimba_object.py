from ctypes import byref, sizeof, c_void_p, c_uint32, c_uint64, c_bool
from typing import List, Optional

from .vimba_exception import VimbaException
from .feature import Feature, _FEATURE_DATA_COMMAND
from . import vimba_c


class VimbaObject:
    """
    A Vimba object has a handle and features associated with it. Objects include System, Camera,
    Interface and AncillaryData. Features are automatically readable as instance attributes.
    """

    VMB_ACCESS_MODE_NONE = 0
    VMB_ACCESS_MODE_FULL = 1
    VMB_ACCESS_MODE_READ = 2
    VMB_ACCESS_MODE_CONFIG = 4
    VMB_ACCESS_MODE_LITE = 8

    def __init__(self, vimba, handle: Optional[int] = None):
        self._vimba = vimba
        self._handle = c_void_p(handle)

        self._features = {}

    def __getattr__(self, item: str):
        # allow direct access to feature values as an attribute
        if item in self.feature_names():
            feature = self.feature(item)

            # command feature types are a special case, return a callable
            if feature.info.featureDataType == _FEATURE_DATA_COMMAND:
                return lambda: self.run_feature_command(item)

            # otherwise attempt to get their value
            return feature.value

        raise AttributeError('{} object has no attribute {}'.format(self.__class__.__name__, item))

    # allow direct access to feature values as an attribute
    def __setattr__(self, item: str, value):
        # set privates as normally to avoid recursion errors
        if item.startswith('_'):
            super().__setattr__(item, value)

        # allow direct access to feature values as an attribute
        elif item in self.feature_names():
            self.feature(item).value = value

        else:
            super().__setattr__(item, value)

    def _feature_infos(self) -> List[vimba_c.VmbFeatureInfo]:
        """
        Gets feature info of all available features. Will cause error if object/camera/etc is not
        opened.
        """
        # call once to get number of available features
        vmb_feature_info = vimba_c.VmbFeatureInfo()
        num_found = c_uint32(-1)
        error = vimba_c.vmb_features_list(self._handle,
                                          None,
                                          0,
                                          byref(num_found),
                                          sizeof(vmb_feature_info))
        if error:
            raise VimbaException(error)

        # call again to get the features
        num_features = num_found.value
        vmb_feature_infos = (vimba_c.VmbFeatureInfo * num_features)()
        error = vimba_c.vmb_features_list(self._handle,
                                          vmb_feature_infos,
                                          num_features,
                                          byref(num_found),
                                          sizeof(vmb_feature_info))
        if error:
            raise VimbaException(error)

        return list(vmb_feature_info for vmb_feature_info in vmb_feature_infos)

    def _feature_info(self, feature_name: str) -> vimba_c.VmbFeatureInfo:
        """
        Gets feature info object of specified feature.
        :param feature_name: the name of the feature.
        """
        for vmb_feature_info in self._feature_infos():
            if feature_name == vmb_feature_info.name.decode():
                return vmb_feature_info
        raise VimbaException(VimbaException.ERR_INSTANCE_NOT_FOUND)

    def feature_names(self) -> List[str]:
        """
        Get names of all available features.
        """
        return list(vmb_feature_info.name.decode()
                    for vmb_feature_info in self._feature_infos())

    def feature(self, feature_name: str) -> Feature:
        """
        Gets feature object by name from the corresponding Vimba object.
        :param feature_name: name of the feature to get.
        """
        if feature_name in self._features:
            return self._features[feature_name]

        # cache feature
        feature = Feature(feature_name, self._handle)
        self._features[feature_name] = feature

        return feature

    def run_feature_command(self, feature_name: str) -> None:
        """
        Run a feature command.
        :param feature_name: the name of the feature.
        """
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

    # todo test
    def read_register(self, address: int) -> int:
        # note that the underlying Vimba function allows reading of an array of registers, but only
        # one address/value at a time is implemented here
        """
        Read from a register of the module (camera) and return its value.
        :param address: the address of the register to read.
        """
        read_count = 1
        reg_address = c_uint64(address)
        reg_data = c_uint64()
        num_complete_reads = c_uint32()
        error = vimba_c.vmb_registers_read(self._handle,
                                           read_count,
                                           byref(reg_address),
                                           byref(reg_data),
                                           byref(num_complete_reads))
        if error:
            raise VimbaException(error)

        return reg_data.value

    # todo test
    def write_register(self, address: int, value: int) -> None:
        # note that the underlying Vimba function allows writing of an array of registers, but only
        # one address/value at a time is implemented here
        """
        Write to a register of the module (camera).
        :param address: the address of the register to read.
        :param value: the value to set in hex.
        """
        write_count = 1
        reg_address = c_uint64(address)
        reg_data = c_uint64(value)
        num_complete_writes = c_uint32()
        error = vimba_c.vmb_registers_write(self._handle,
                                            write_count,
                                            byref(reg_address),
                                            byref(reg_data),
                                            byref(num_complete_writes))
        if error:
            raise VimbaException(error)
