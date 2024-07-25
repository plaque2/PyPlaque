import numpy as np


def centroid(arr: np.ndarray) -> tuple:
  """
  **centroid Function**
  This function calculates the centroid (average of x and y coordinates) from a 2D Numpy array of 
  (x,y) values. It computes the centroid by averaging the x-coordinates and y-coordinates separately 
  from a provided 2D numpy array where each row represents a point in space with its x and y 
  coordinates. It handles exceptions by returning (0, 0) if an error occurs due to 
  incorrect input format.
  
  Args:
    arr (np.ndarray, required): A 2D Numpy array of shape (n_points, 2), where each row contains 
                                the x and y coordinates of a point.
  
  Returns:
    tuple: A tuple containing the average x-coordinate and the average y-coordinate as floats, 
    representing the centroid of the provided points.
      
  Raises:
    TypeError: If `arr` is not a 2D Numpy array or does not have the correct shape for 
    calculating centroids.
  """
  try:
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length
  except ValueError:
    print('Array should be 2D Numpy array of (x,y) values. Check again!')
    return 0, 0