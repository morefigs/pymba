# -*- coding: utf-8 -*-
from __future__ import absolute_import
from . import vimbastructure as structs
from .vimbaobject import VimbaObject
from .vimbaexception import VimbaException
from .vimbadll import VimbaDLL
from ctypes import *

# interface features are automatically readable as object attributes.


class VimbaInterface(VimbaObject):

    """
    A Vimba interface object. This class provides the minimal access
    to Vimba functions required to control the interface.
    """

    @property
    def interfaceIdString(self):
        return self._interfaceIdString

    # own handle is inherited as self._handle
    def __init__(self, interfaceIdString):

        # call super constructor
        super(VimbaInterface, self).__init__()

        # set ID
        self._interfaceIdString = interfaceIdString

    def openInterface(self):
        """
        Open the interface.
        """
        errorCode = VimbaDLL.interfaceOpen(self._interfaceIdString,
                                           byref(self._handle))
        if errorCode != 0:
            raise VimbaException(errorCode)

    def closeInterface(self):
        """
        Close the interface.
        """
        errorCode = VimbaDLL.interfaceClose(self._handle)
        if errorCode != 0:
            raise VimbaException(errorCode)
