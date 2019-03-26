from ctypes import byref, sizeof, c_uint32, c_double, c_char_p, c_bool, c_int64, create_string_buffer
from typing import Union, Tuple, List, Callable

from .vimba_exception import VimbaException
from . import vimba_c


(
    _FEATURE_DATA_UNKNOWN,
    _FEATURE_DATA_INT,
    _FEATURE_DATA_FLOAT,
    _FEATURE_DATA_ENUM,
    _FEATURE_DATA_STRING,
    _FEATURE_DATA_BOOL,
    _FEATURE_DATA_COMMAND,
    _FEATURE_DATA_RAW,
    _FEATURE_DATA_NONE,
) = range(9)


class Feature:
    """
    A feature of a Vimba object.
    """

    @property
    def name(self) -> str:
        return self._name.decode()

    @property
    def info(self) -> vimba_c.VmbFeatureInfo:
        return self._feature_info()

    @property
    def value(self) -> Union[str, int, float, bool]:
        return self._access_func('get', self.info.featureDataType)()

    @value.setter
    def value(self, value: Union[str, int, float, bool]) -> None:
        self._access_func('set', self.info.featureDataType)(value)

    @property
    def range(self) -> Union[None, Tuple[int, int], Tuple[float, float], Tuple[str, str]]:
        # only some types actually have a range
        if self.info.featureDataType in (_FEATURE_DATA_INT,
                                         _FEATURE_DATA_FLOAT,
                                         _FEATURE_DATA_ENUM):
            return self._access_func('range', self.info.featureDataType)()
        return None

    def __init__(self, name, handle):
        self._name = name.encode()
        self._handle = handle

    def _access_func(self, func_type: str, data_type: int) -> Callable:
        """
        Get the correct function needed to access the feature attribute based on the feature's data
        type.
        :param func_type: One of 'get', 'set', or 'range'.
        :param data_type: Data type as defined in VmbFeatureDataType.
        """
        # (getter, setter, range) funcs
        access_funcs = {
            _FEATURE_DATA_UNKNOWN: (),
            _FEATURE_DATA_INT: (self._get_int,
                                self._set_int,
                                self._range_query_int),
            _FEATURE_DATA_FLOAT: (self._get_float,
                                  self._set_float,
                                  self._range_query_float),
            _FEATURE_DATA_ENUM: (self._get_enum,
                                 self._set_enum,
                                 self._range_query_enum),
            _FEATURE_DATA_STRING: (self._get_string,
                                   self._set_string),
            _FEATURE_DATA_BOOL: (self._get_bool,
                                 self._set_bool),
            _FEATURE_DATA_COMMAND: (),
            _FEATURE_DATA_RAW: (),
            _FEATURE_DATA_NONE: (),
        }

        access_indices = {
            'get': 0,
            'set': 1,
            'range': 2,
        }

        # doesn't make sense to get / set a command data type
        if data_type == _FEATURE_DATA_COMMAND:
            raise VimbaException(VimbaException.ERR_COMMAND_MUST_BE_CALLED)

        # some data types aren't implemented
        try:
            return access_funcs[data_type][access_indices[func_type]]
        except IndexError:
            raise VimbaException(VimbaException.ERR_NOT_IMPLEMENTED_IN_PYMBA)

    def _feature_info(self) -> vimba_c.VmbFeatureInfo:
        vmb_feature_info = vimba_c.VmbFeatureInfo()
        error = vimba_c.vmb_feature_info_query(self._handle,
                                               self._name,
                                               byref(vmb_feature_info),
                                               sizeof(vmb_feature_info))
        if error:
            raise VimbaException(error)

        return vmb_feature_info

    def _get_int(self) -> int:
        value = c_int64()
        error = vimba_c.vmb_feature_int_get(self._handle,
                                            self._name,
                                            byref(value))
        if error:
            raise VimbaException(error)

        return value.value

    def _set_int(self, value: int) -> None:
        error = vimba_c.vmb_feature_int_set(self._handle,
                                            self._name,
                                            value)
        if error:
            raise VimbaException(error)

    def _get_float(self) -> float:
        value = c_double()
        error = vimba_c.vmb_feature_float_get(self._handle,
                                              self._name,
                                              byref(value))
        if error:
            raise VimbaException(error)

        return value.value

    def _set_float(self, value: float) -> None:
        error = vimba_c.vmb_feature_float_set(self._handle,
                                              self._name,
                                              value)
        if error:
            raise VimbaException(error)

    def _get_enum(self) -> str:
        value = c_char_p()
        error = vimba_c.vmb_feature_enum_get(self._handle,
                                             self._name,
                                             byref(value))
        if error:
            raise VimbaException(error)

        return value.value.decode()

    def _set_enum(self, value: str):
        error = vimba_c.vmb_feature_enum_set(self._handle,
                                             self._name,
                                             value.encode())
        if error:
            raise VimbaException(error)

    def _get_string(self) -> str:
        buffer_size = 256
        value = create_string_buffer(buffer_size)
        size_filled = c_uint32()

        error = vimba_c.vmb_feature_string_get(self._handle,
                                               self._name,
                                               value,
                                               buffer_size,
                                               byref(size_filled))
        if error:
            raise VimbaException(error)
        return value.value.decode()

    def _set_string(self, value: str) -> None:
        error = vimba_c.vmb_feature_string_set(self._handle,
                                               self._name,
                                               value.encode())
        if error:
            raise VimbaException(error)

    def _get_bool(self) -> bool:
        value = c_bool()
        error = vimba_c.vmb_feature_bool_get(self._handle,
                                             self._name,
                                             byref(value))
        if error:
            raise VimbaException(error)

        return value.value

    def _set_bool(self, value: bool):
        error = vimba_c.vmb_feature_bool_set(self._handle,
                                             self._name,
                                             value)
        if error:
            raise VimbaException(error)

    def _range_query_int(self) -> Tuple[int, int]:
        range_min = c_int64()
        range_max = c_int64()
        error = vimba_c.vmb_feature_int_range_query(self._handle,
                                                    self._name,
                                                    byref(range_min),
                                                    byref(range_max))
        if error:
            raise VimbaException(error)

        return int(range_min.value), int(range_max.value)

    def _range_query_float(self) -> Tuple[float, float]:
        range_min = c_double()
        range_max = c_double()
        error = vimba_c.vmb_feature_float_range_query(self._handle,
                                                      self._name,
                                                      byref(range_min),
                                                      byref(range_max))
        if error:
            raise VimbaException(error)

        return range_min.value, range_max.value

    def _range_query_enum(self) -> List[str]:
        # call once to get number of available enum names
        num_found = c_uint32(-1)
        error = vimba_c.vmb_feature_enum_range_query(self._handle,
                                                     self._name,
                                                     None,
                                                     0,
                                                     byref(num_found))
        if error:
            raise VimbaException(error)

        # call again to get the actual enum names
        num_enum_names = num_found.value
        enum_names = (c_char_p * num_enum_names)()
        error = vimba_c.vmb_feature_enum_range_query(self._handle,
                                                     self._name,
                                                     enum_names,
                                                     num_enum_names,
                                                     byref(num_found))
        if error:
            raise VimbaException(error)

        return list(enum_name.decode() for enum_name in enum_names)
