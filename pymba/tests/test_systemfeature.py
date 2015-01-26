#!/usr/bin/python

from pymba import *


def test_systemfeature():
    # get system object
    with Vimba() as vimba:
        system = vimba.getSystem()

        # list system features
        for featureName in system.getFeatureNames():
            print 'System feature:', featureName
            fInfo = system.getFeatureInfo(featureName)
            for field in fInfo.getFieldNames():
                print "\t", featureName, ":", field, getattr(fInfo, field)


