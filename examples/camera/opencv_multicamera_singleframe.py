from pymba import Vimba
from pymba import VimbaException
import cv2
import sys

# only a demo to configure camera features
def cam_set_ROI(camera, width: int, height: int) -> None:
    feature_h = camera.feature("Height")
    feature_h.value = height
    feature_w = camera.feature("Width")
    feature_w.value = width

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
        # Open cameras and print information
        for idx, cam in enumerate(cams):
            try:
                cam.open()
                cam.arm('SingleFrame')
            except VimbaException as e:
                if e.error_code == VimbaException.ERR_TIMEOUT:
                    print(e)
                    cam.disarm()
                    cam.arm('SingleFrame')
                elif e.error_code == VimbaException.ERR_DEVICE_NOT_OPENED:
                    print(e)
                    cam.open()
                    cam.arm('SingleFrame')
        return cams

def main():
    PIXEL_FORMATS_CONVERSIONS = {'BayerRG8': cv2.COLOR_BAYER_RG2RGB}
    cams = init_cameras()
    flag = True
    while flag:
        try:
            for idx, cam in enumerate(cams):
                frame = cam.acquire_frame()
                img = frame.buffer_data_numpy()
                # convert color space if desired
                if(frame.pixel_format == 'BayerRG8'):
                    img = cv2.cvtColor(img, PIXEL_FORMATS_CONVERSIONS[frame.pixel_format])
                img = cv2.resize(img, (400, 300))
                cv2.imshow("Cam {} - {}".format(idx, ["cam{}". format(idx)]), img)
                c = cv2.waitKey(5)
                if c == ord('q'):
                    flag = False
        except KeyboardInterrupt:
            sys.exit(1)
    for cam in cams:
        cam.disarm()
        cam.close()
    cv2.destroyAllWindows()
    Vimba().shutdown()

if __name__ == '__main__':
    main()