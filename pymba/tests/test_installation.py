#!/usr/bin/python

from pymba import Vimba


def test_installation():
    with Vimba() as vimba:
	    version = vimba.getVersion()
	    assert version == '1.2.0'
