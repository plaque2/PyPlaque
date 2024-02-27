import numpy as np


def centroid(arr: np.ndarray) -> tuple:
  try:
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length
  except ValueError:
    print('Array should be 2D Numpy array of (x,y) values. Check again!')
    return 0, 0
