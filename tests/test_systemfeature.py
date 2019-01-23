#!/usr/bin/python
from __future__ import absolute_import, print_function, division
from pymba import *


def test_systemfeature():
    # get system object
    with Vimba() as vimba:
        system = vimba.getSystem()

        # list system features
        for featureName in system.get_feature_names():
            print('System feature:', featureName)
            fInfo = system.get_feature_info(featureName)
            for field in fInfo.getFieldNames():
                print("\t", featureName, ":", field, getattr(fInfo, field))


if __name__ == '__main__':
    test_systemfeature()