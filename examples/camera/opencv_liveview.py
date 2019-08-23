from pymba import Vimba
from pymba import VimbaException
from pymba import Frame

from typing import Optional
import cv2
import sys
import collections

# todo add more colours
PIXEL_FORMATS_CONVERSIONS = {
    'BayerRG8': cv2.COLOR_BAYER_RG2RGB,
}


class FrameObserver:
    def __init__(self, idx, camera):
        print("create FrameObserver class")
        self.idx = idx
        self.cam = camera

    def frame_callback(self, frame: Frame) -> None:
        # TODO: only support 8bit pixel format
        # Details can refer to .\examples\camera\opencv_display_various_image.py
        img = frame.buffer_data_numpy()
        # convert color space if desired
        if (frame.pixel_format == 'BayerRG8'):
            img = cv2.cvtColor(img, PIXEL_FORMATS_CONVERSIONS[frame.pixel_format])
            #img = cv2.resize(img, (400, 300))
            cv2.imshow("cam-{}".format(self.idx), img)
        else:
            #img = cv2.resize(img, (400, 300))
            cv2.imshow("cam-{}".format(self.idx), img)

        c = cv2.waitKey(5)
        if c == ord('q'):
            global flag
            flag = False

def init_cameras():
    # vimba object
    vimba = Vimba()
    # Start vimba system
    vimba.startup()
    vmFactory = vimba.camera_ids()
    # Get connected cameras
    cams = [vimba.camera(id) for id in vmFactory]
    if len(cams) == 0:
        raise OSError("No camera present.")
    for idx, device in enumerate(vmFactory):
        print("Device {} ID: {}".format(idx, device))

    observerList = []
    for idx, cam in enumerate(cams):
        observerList.append(FrameObserver(idx, cam))
        try:
            cam.open()
            cam.arm('Continuous', observerList[idx].frame_callback)
            cam.start_frame_acquisition()
        except VimbaException as e:
            if e.error_code == VimbaException.ERR_TIMEOUT:
                print(e)
                cam.disarm()
                cam.arm('Continuous', observerList[idx].frame_callback)
                cam.start_frame_acquisition()
            elif e.error_code == VimbaException.ERR_DEVICE_NOT_OPENED:
                print(e)
                cam.open()
                cam.arm('Continuous', observerList[idx].frame_callback)
                cam.start_frame_acquisition()
            else:
                print(e)
    return cams

flag = True  # global variable
def main():
    cams = init_cameras()
    global flag
    flag = True
    while flag:
        try:
            c = cv2.waitKey(5)
            if c == ord('q'):
                flag = False
        except KeyboardInterrupt:
            sys.exit(1)

    for cam in cams:
        cam.stop_frame_acquisition()
        cam.disarm()
        cam.close()
    cv2.destroyAllWindows()
    Vimba().shutdown()

if __name__ == '__main__':
    main()


