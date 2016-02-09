#!/usr/bin/python
from __future__ import absolute_import, print_function, division
from pymba import Vimba


def test_installation():
    with Vimba() as vimba:
	    version = vimba.getVersion()
	    assert version == '1.2.0'
