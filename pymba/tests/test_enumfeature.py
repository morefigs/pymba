#!/usr/bin/python
from __future__ import absolute_import, print_function, division
from pymba import *


def test_enumfeature():
    # get system object
    with Vimba() as vimba:
        system = vimba.getSystem()
        
        # get enum value
        print ("get enum value (DiscoveryCameraEvent): '%s'" % (system.DiscoveryCameraEvent))
        
        # get enum range
        range = system.getFeatureRange('DiscoveryCameraEvent')
        print ("get enum value range (DiscoveryCameraEvent): '%s'" % (str(range)))
        
        # set enum value
        #print ("setting enum value (DiscoveryCameraEvent)...")
        #system.DiscoveryCameraEvent = 'Unreachable'
        #print ("enum value (DiscoveryCameraEvent)set to '%s'." % (system.DiscoveryCameraEvent.value))


if __name__ == '__main__':
    test_enumfeature()