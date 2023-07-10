import numpy as np

def remove_artifacts(img: np.array,artifact_threshold: float) -> np.array:
    img[img > artifact_threshold] = 0
    return img
