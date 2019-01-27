from pymba import Vimba
from time import sleep


if __name__ == '__main__':

    with Vimba() as vmb:

        # required for discovering GigE cameras
        if vmb.system().GeVTLIsPresent:
            vmb.system().run_feature_command("GeVDiscoveryAllOnce")
            sleep(0.2)

        # provide camera index or id
        camera = vmb.camera(0)
        print(camera)
