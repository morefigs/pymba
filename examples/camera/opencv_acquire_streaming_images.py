from time import sleep
import cv2
from pymba import Vimba, Frame


def process_frame(frame: Frame):
    """
    Process the streaming frames. Consider sending the frame data to another thread/process if this is long running to
    avoid dropping frames.
    """
    print(f'frame {frame.data.frameID} callback')

    # get a copy of the frame data
    image = frame.buffer_data_numpy()

    # display image
    cv2.imshow('Image', image)
    cv2.waitKey(1)


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        # arm the camera and provide a function to be called upon frame ready
        camera.arm('Continuous', process_frame)
        camera.start_frame_acquisition()

        # stream images for a while...
        sleep(5)

        # stop frame acquisition
        # start_frame_acquisition can simply be called again if the camera is still armed
        camera.stop_frame_acquisition()
        camera.disarm()

        camera.close()
