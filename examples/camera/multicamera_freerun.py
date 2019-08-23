from __future__ import print_function
from typing import Optional
from time import sleep
from pymba import Vimba
from pymba import Frame

def FrameCallback(frame: Frame, delay: Optional[int] = 10) -> None:
    bShowFrameInfos = True
    if bShowFrameInfos == True:
        print('Frame ID:%d' %(frame.data.frameID), end=" ")
        print('Size: %d' %(len(frame.buffer_data())), end=" " )
        print("Format:%s" %(frame.pixel_format))
        # print('Status: %s' % (frame.receiveStatus)) -- no such feature up to now
    print(".", end="")


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
            cam.arm(mode='Continuous', callback=FrameCallback)
            cam.start_frame_acquisition()
        except VimbaException as e:
            if e.error_code == VimbaException.ERR_TIMEOUT:
                print(e)
                cam.disarm()
                cam.arm('Continuous')
            elif e.error_code == VimbaException.ERR_DEVICE_NOT_OPENED:
                print(e)
                cam.open()
                cam.arm('Continuous', display_frame_count)
    return cams

def main():
    cams = init_cameras()
    sleep(2)
    for cam in cams:
        cam.disarm()
        cam.close()
    Vimba().shutdown()

if __name__ == '__main__':
    main()
