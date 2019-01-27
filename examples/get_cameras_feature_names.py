from pymba import Vimba
from time import sleep


if __name__ == '__main__':

    with Vimba() as vmb:

        # required for discovering GigE cameras
        if vmb.system().GeVTLIsPresent:
            vmb.system().run_feature_command("GeVDiscoveryAllOnce")
            sleep(0.2)

        camera = vmb.camera(0)
        camera.open()
        for feature_name in camera.feature_names():
            print(feature_name)
        camera.close()
