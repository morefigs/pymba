import cv2
from pymba import Vimba


if __name__ == '__main__':

    with Vimba() as vimba:
        camera = vimba.camera(0)
        camera.open()

        # setup camera and frame and capture a single image
        camera.AcquisitionMode = 'SingleFrame'
        frame = camera.create_frame()
        frame.announce()
        camera.start_capture()
        frame.queue_for_capture()
        camera.run_feature_command('AcquisitionStart')
        camera.run_feature_command('AcquisitionStop')
        frame.wait_for_capture()

        # get the image data as a numpy array
        image = frame.image_numpy_array()

        # display image
        cv2.imshow(camera.camera_id, image)
        # waits for user to close image
        cv2.waitKey(0)

        # stop capturing and clean up
        camera.end_capture()
        camera.flush_capture_queue()
        camera.revoke_all_frames()

        camera.close()
