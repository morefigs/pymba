import cv2
from pymba import Vimba, Frame


def process_frame(frame: Frame):
    """
    Processes the acquired frame.
    """
    print(f'frame {frame.data.frameID} callback')

    # get a copy of the frame data
    image = frame.buffer_data_numpy()

    # display image
    cv2.imshow('Image', image)

    # wait for user to close window
    cv2.waitKey(0)


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        camera.arm('SingleFrame')

        # capture a single frame, more than once if desired
        for i in range(1):
            frame_ = camera.acquire_frame()
            process_frame(frame_)

        camera.disarm()

        camera.close()
