import numpy as np
from skimage.filters import gaussian


def fixed_threshold(img: np.ndarray, thr: float, s: float) -> np.ndarray:
  img = gaussian(img, sigma = s)
  img[img > thr] = 1
  img[img <= thr] = 0
  return img
