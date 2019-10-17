
from __future__ import absolute_import, print_function, division
from pymba import *
import numpy as np
import cv2
import time

Vimba().startup()
camera = Vimba().camera(0)
camera.open()
print("Camera List ID is %s", Vimba.camera_ids())

pixel_format = camera.feature("PixelFormat")
pixel_format.value = "BayerRG8"
# Note: Tested with at "Mono8" "BayerRG8" "BayerRG12" "BayerRG12Packed" "RGB8Packed" pixel format

camera.arm('SingleFrame')
image_Height = camera.feature("Height")
image_Width = camera.feature("Width")
Height = image_Height.value
Width = image_Width.value

# capture a single frame, more than once if desired
for i in range(1):
    frame = camera.acquire_frame()
    print('frame No.{}'.format(frame.data.frameID))
    camera_frame_size = len(frame.buffer_data())
    frame_pixel_format = frame.pixel_format
    print("Frame size: %d,  Image Resolution: %dx%d,  pixel_format: %s " % (camera_frame_size, Width, Height, frame_pixel_format))
    data_bytes = frame.buffer_data()

    if (frame_pixel_format == "Mono8" or frame_pixel_format == "BayerRG8" or frame_pixel_format == "BayerGR8"):
        frame_8bits = np.ndarray(buffer=data_bytes, dtype=np.uint8, shape=(Height, Width))

    elif (frame_pixel_format == "BayerRG12" or frame_pixel_format == "Mono10" or frame_pixel_format == "Mono12" or frame_pixel_format == "Mono14"):
        data_bytes = np.frombuffer(data_bytes, dtype=np.uint8)
        pixel_even = data_bytes[0::2]
        pixel_odd = data_bytes[1::2]

        # Convert bayer16 to bayer8 / Convert Mono12/Mono14 to Mono8
        if (frame_pixel_format == "Mono14"):
            pixel_even = np.right_shift(pixel_even, 6)
            pixel_odd = np.left_shift(pixel_odd, 2)
        elif (frame_pixel_format == "Mono10"):
            pixel_even = np.right_shift(pixel_even, 2)
            pixel_odd = np.left_shift(pixel_odd, 6)
        else:
            pixel_even = np.right_shift(pixel_even, 4)
            pixel_odd = np.left_shift(pixel_odd, 4)
        frame_8bits = np.bitwise_or(pixel_even, pixel_odd).reshape(Height, Width)

    elif (frame_pixel_format == "BayerRG12Packed" or frame_pixel_format == "Mono12Packed" or frame_pixel_format == "BayerGR12Packed"):
        data_bytes = np.frombuffer(data_bytes, dtype=np.uint8)
        size = len(data_bytes)
        index = []
        for i in range(0, size, 3):
            index.append(i+1)

        data_bytes = np.delete(data_bytes, index)
        frame_8bits = data_bytes.reshape(Height, Width)

    elif (frame_pixel_format == "RGB8Packed" or frame_pixel_format == "BGR8Packed"):
        frame_8bits = np.ndarray(buffer=frame.buffer_data(), dtype=np.uint8, shape=(Height, Width*3))

    else:
        # Note: wait to do -- other format, such as YUV411Packed, YUV422Packed, YUV444Packed
        frame_8bits = np.ndarray(buffer=frame.buffer_data(), dtype=np.uint8, shape=(Height, Width))


    cv2.imshow("Frame_8bits", frame_8bits)
    k = cv2.waitKey(100)

    if (frame_pixel_format == "BayerRG8" or frame_pixel_format == "BayerRG12" or frame_pixel_format == "BayerRG12Packed"):
        colorImg = cv2.cvtColor(frame_8bits, cv2.COLOR_BAYER_RG2RGB )
        cv2.imshow("Color_Image", colorImg)
    elif (frame_pixel_format == "BayerGR8" or frame_pixel_format == "BayerGR12" or frame_pixel_format == "BayerGR12Packed"):
        colorImg = cv2.cvtColor(frame_8bits, cv2.COLOR_BAYER_GR2RGB )
        cv2.imshow("Color_Image", colorImg)
    elif (frame_pixel_format == "RGB8Packed" or frame_pixel_format == "BGR8Packed"):
        RGBImg = frame_8bits.reshape(Height, Width, 3)
        colorImg = cv2.cvtColor(RGBImg, cv2.COLOR_BGR2RGB)
        cv2.imshow("Color_Image", colorImg)

    k = cv2.waitKey(0)


camera.disarm()
camera.close()
Vimba.shutdown()
