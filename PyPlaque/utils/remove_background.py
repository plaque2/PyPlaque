import numpy as np
from skimage import restoration


def remove_background(img: np.ndarray, radius: float) -> tuple(np.ndarray,
np.ndarray):
  img = np.array(img).astype(np.uint16)

  background = restoration.rolling_ball(img, radius=radius)

  return background, img-background
