import numpy as np


def remove_artifacts(img: np.ndarray,artifact_threshold: float) -> np.ndarray:
  img[img > artifact_threshold] = 0
  return img
