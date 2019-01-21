from pymba.vimba import Vimba
from time import sleep


if __name__ == '__main__':

    with Vimba() as vmb:
        # required for discovering GigE cameras
        if vmb.system.GeVTLIsPresent:
            vmb.system.runFeatureCommand("GeVDiscoveryAllOnce")
            sleep(0.2)
        print(vmb.camera_ids)
