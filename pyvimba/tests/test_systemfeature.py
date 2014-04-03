#!/usr/bin/python

from pyvimba.vimba import *

def test_systemfeature():
    # get system object
    vimba = Vimba()
    system = vimba.getSystem()
    
    # list system features
    for featureName in system.getFeatureNames():
        print 'System feature:', featureName
        
    # shutdown Vimba
    vimba.shutdown()

