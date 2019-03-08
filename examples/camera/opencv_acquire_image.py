from pymba import Vimba
from examples.camera.display_frame import display_frame


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        camera.arm('SingleFrame')

        # capture a single frame, more than once if desired
        for i in range(1):
            frame = camera.acquire_frame()
            display_frame(frame, 0)

        camera.disarm()

        camera.close()
