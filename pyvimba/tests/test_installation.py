#!/usr/bin/python

from pyvimba.vimba import *

def test_installation():
    vimba = Vimba()
    version = vimba.getVersion()
    assert version == '1.2.0'
