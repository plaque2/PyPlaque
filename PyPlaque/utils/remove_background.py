
import cv2
import numpy as np
from skimage import io, restoration
from skimage.morphology import disk, opening



def remove_background(img: np.ndarray, radius: float) -> tuple[np.ndarray,
np.ndarray]:
  img = np.array(img).astype(np.uint16)

    selem = disk(radius)

    selem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*radius + 1, 2*radius + 1))

    # Perform morphological opening
    background =  cv2.morphologyEx(img, cv2.MORPH_OPEN, selem)

    return background, img-background