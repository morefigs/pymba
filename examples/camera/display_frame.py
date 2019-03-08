from typing import Optional
import cv2
from pymba import Frame


# todo add more colours
PIXEL_FORMAT_MAPPING = {
    'BayerRG8': cv2.COLOR_BAYER_RG2RGB,
}


def display_frame(frame: Frame, delay: Optional[int] = 1) -> None:
    """
    Processes the acquired frame.
    :param frame: The frame object to process.
    :param delay: Image display delay in milliseconds, use 0 for indefinite.
    """
    print(f'frame {frame.data.frameID}')

    # get a copy of the frame data
    image = frame.buffer_data_numpy()

    # convert colour space if desired
    try:
        image = cv2.cvtColor(image, PIXEL_FORMAT_MAPPING[frame.pixel_format])
    except KeyError:
        pass

    # display image
    cv2.imshow('Image', image)

    # wait for user to close window
    cv2.waitKey(delay)
