# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .vimbaobject import VimbaObject
from ctypes import c_void_p

# system features are automatically readable as attributes.


class VimbaSystem(VimbaObject):

    """
    A Vimba system object. This class provides the minimal access
    to Vimba functions required to control the system.
    """

    # own handle is inherited as self._handle

    def __init__(self):

        # call super constructor
        super(VimbaSystem, self).__init__()

        # set own handle manually
        self._handle = c_void_p(1)
