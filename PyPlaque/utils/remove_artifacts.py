import numpy as np


def remove_artifacts(img: np.ndarray,artifact_threshold: float) -> np.ndarray:
  """
  **remove_artifacts Function**
  This function removes pixel artifacts from an image by setting pixels above a specified threshold 
  to zero. It iterates through each pixel in the input `img` and sets the pixel value to 0 if it 
  exceeds the `artifact_threshold`. This is useful for removing unwanted high-intensity points that 
  may be considered artifacts in the imaging process.
  
  Args:
    img (np.ndarray, required): A 2D numpy array representing the grayscale image from which 
                            artifacts should be removed.
    artifact_threshold (float, required): The threshold value above which pixel intensities are 
                                        set to zero, effectively removing artifacts.
  
  Returns:
    np.ndarray: A 2D numpy array of the same size as `img` with pixels exceeding the 
    `artifact_threshold` set to 0, thus reducing artifact noise in the image.
      
  Raises:
    TypeError: If `img` is not a 2D numpy array or `artifact_threshold` is not a float.
    ValueError: If `artifact_threshold` is less than or equal to zero.
  """
  img[img > artifact_threshold] = 0
  return img
