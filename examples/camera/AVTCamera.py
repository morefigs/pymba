from pymba import vimba
from pymba import Frame
from time import sleep
import cv2

PIXEL_FORMATS_CONVERSIONS = {
    'BayerRG8': cv2.COLOR_BAYER_RG2RGB,
}

class AVTCamera:

    vimba=None
    camFactory=None

    def __init__(self,capture_device=0):
        # vimba object
        if AVTCamera.vimba == None:
            AVTCamera.vimba = vimba.Vimba()
            # Start vimba system
            AVTCamera.vimba.startup()
            AVTCamera.camFactory = vimba.camera_ids()
        self.cam_open=False

        cams = [AVTCamera.vimba.camera(id) for id in AVTCamera.camFactory]
        if len(cams) == 0 or len(cams) < capture_device:
            print("No AVT camera found")
            self.cam=None
        else:
            self.cam=cams[capture_device]

    def read(self):
        self.open()
        self.singleframe = 0
        self.cam.start_frame_acquisition()
        while self.singleframe == 0 :
            sleep(0.05)
        self.cam.stop_frame_acquisition()
        return self.image

    def convert_frame(self, frame: Frame )->None:
        #print('frame {}'.format(frame.data.frameID))
        self.singleframe += 1
        self.image = frame.buffer_data_numpy()
        try:
            self.image = cv2.cvtColor(self.image, PIXEL_FORMATS_CONVERSIONS[frame.pixel_format])
        except KeyError:
            pass

    def release(self):
        self.cam.disarm()
        self.cam.close()
        self.cam_open = False

    def preview(self):
        while True:
            img=self.read()
            cv2.imshow('xc', img)
            c=cv2.waitKey(10)
            if c==ord ('q') :
                cv2.destroyWindow('xc')
                return img;

    def open(self):
        if self.cam == None:
            self.image=None
            return self.image
        if self.cam_open == False :
            self.cam.open()
            self.cam_open = True
            self.cam.arm('Continuous', self.convert_frame)


def cam_test():
    camera=AVTCamera(0)
    while True:
        image=camera.read()
        cv2.imshow('Image', image)
        c=cv2.waitKey(10)
        if c==ord ('q') :
            camera.release()
            break;

def cam_test_preview():
    camera=AVTCamera(0)
    camera.preview()
    camera.release()

if __name__=='__main__':
    cam_test_preview()
