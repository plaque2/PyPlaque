from skimage import restoration
import numpy as np

def remove_background(img: np.array, radius: float) -> np.array:
    img = np.array(img).astype(np.uint16)

    background = restoration.rolling_ball(img, radius=radius)

    return background, img-background