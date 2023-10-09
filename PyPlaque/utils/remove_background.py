import cv2
import numpy as np
from skimage import io, restoration
from skimage.morphology import disk, opening


def remove_background(img: np.array, radius: float) -> np.array:
    img = np.array(img).astype(np.uint16)


    selem = disk(radius)

    selem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*radius + 1, 2*radius + 1))

    # Perform morphological opening
    # bcg = cv2.morphologyEx(inputImage, cv2.MORPH_OPEN, kernel)
    # background = restoration.rolling_ball(img, radius=radius)
    # background = opening(img,selem)
    background =  cv2.morphologyEx(img, cv2.MORPH_OPEN, selem)



    return background, img-background
