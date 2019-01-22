from ctypes import byref, sizeof, c_uint32, c_double, c_char_p, c_bool, c_int64, create_string_buffer
from typing import Tuple, List

from .vimba_exception import VimbaException
from . import vimba_c


class VimbaFeature:
    """
    A feature of a Vimba object.
    """

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

    @property
    def name(self):
        return self._name.decode()

    @property
    def handle(self):
        return self._handle

    # lookup relevant function for feature type and pass to that function
    @property
    def value(self):
        return self._feature_data_value_funcs[self._info.featureDataType][0]()

    @value.setter
    def value(self, val):
        self._feature_data_value_funcs[self._info.featureDataType][1](val)

    @property
    def range(self):
        return self._feature_data_range_funcs[self._info.featureDataType]()

    def __init__(self, name, handle):
        self._name = name.encode()
        self._handle = handle

        # type functions dict for looking up correct get/set function to use
        self._feature_data_value_funcs = {
            self._FEATURE_DATA_UNKNOWN: None,
            self._FEATURE_DATA_INT: (self._get_int, self._set_int),
            self._FEATURE_DATA_FLOAT: (self._get_float, self._set_float),
            self._FEATURE_DATA_ENUM: (self._get_enum, self._set_enum),
            self._FEATURE_DATA_STRING: (self._get_string, self._set_string),
            self._FEATURE_DATA_BOOL: (self._get_bool, self._set_bool),
            self._FEATURE_DATA_COMMAND: None,
            self._FEATURE_DATA_RAW: None,
            self._FEATURE_DATA_NONE: None,
        }

        # type functions dict for looking up correct range function to use
        self._feature_data_range_funcs = {
            self._FEATURE_DATA_UNKNOWN: None,
            self._FEATURE_DATA_INT: self._range_query_int,
            self._FEATURE_DATA_FLOAT: self._range_query_float,
            self._FEATURE_DATA_ENUM: self._range_query_enum,
            self._FEATURE_DATA_STRING: None,
            self._FEATURE_DATA_BOOL: None,
            self._FEATURE_DATA_COMMAND: None,
            self._FEATURE_DATA_RAW: None,
            self._FEATURE_DATA_NONE: None,
        }

        # get info once
        self._info = self._get_info()

    def _get_info(self) -> vimba_c.VmbFeatureInfo:
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
        value = create_string_buffer('\x00' * buffer_size)
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
