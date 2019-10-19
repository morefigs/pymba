from time import sleep
from pymba import Vimba
from examples.camera._display_frame import display_frame


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        # arm the camera and provide a function to be called upon frame ready
        camera.arm('Continuous', display_frame)
        camera.start_frame_acquisition()

        # stream images for a while...
        sleep(5)

        # stop frame acquisition
        # start_frame_acquisition can simply be called again if the camera is still armed
        camera.stop_frame_acquisition()
        camera.disarm()

        camera.close()
