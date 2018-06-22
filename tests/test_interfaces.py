#!/usr/bin/python
from __future__ import absolute_import, print_function, division
from pymba import *
import time


def test_interfaces():
    # start Vimba
    with Vimba() as vimba:
        # get list of available interfaces
        interfaceIds = vimba.getInterfaceIds()
        for interfaceId in interfaceIds:
            print('Interface ID:', interfaceId)

        # get interface object and open it
        interface0 = vimba.getInterface(interfaceIds[0])
        interface0.openInterface()

        # list interface features
        interfaceFeatureNames = interface0.getFeatureNames()
        for name in interfaceFeatureNames:
            print('Interface feature:', name)

        # close interface
        interface0.closeInterface()

if __name__ == '__main__':
    test_interfaces()