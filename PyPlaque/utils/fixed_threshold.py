import numpy as np
from skimage.filters import gaussian

def fixed_threshold(img: np.array, thr: float, s: float) -> np.array:
    img = gaussian(img, sigma = s)
    img[img > thr] = 1
    img[img <= thr] = 0
    return img