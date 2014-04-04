#!/usr/bin/python

from pymba import Vimba


def test_installation():
    vimba = Vimba()
    version = vimba.getVersion()
    assert version == '1.2.0'
