from time import sleep
import cv2
from pymba import Vimba
from pymba.frame import Frame


def on_callback(completed_frame: Frame):
    print('Callback called!')

    # get the image data as a numpy array
    image = completed_frame.image_numpy_array()

    # display image
    cv2.imshow(camera.camera_id, image)
    # waits for user to close image
    cv2.waitKey(0)


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        # setup camera and frame and capture a single image
        camera.AcquisitionMode = 'SingleFrame'
        frame = camera.create_frame()
        frame.announce()
        camera.start_capture()
        frame.queue_for_capture(on_callback)
        camera.run_feature_command('AcquisitionStart')
        camera.run_feature_command('AcquisitionStop')

        # wait long enough for the frame callback to be called
        for _ in range(100):
            sleep(0.1)
            print('.', end='')

        # stop capturing and clean up
        camera.end_capture()
        camera.flush_capture_queue()
        camera.revoke_all_frames()

        camera.close()
