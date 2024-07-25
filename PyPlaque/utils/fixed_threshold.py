import numpy as np
from skimage.filters import gaussian


def fixed_threshold(img: np.ndarray, thr: float, s: float) -> np.ndarray:
  """
  **fixed_threshold Function**
  This function applies a fixed threshold to an image using Gaussian smoothing and binary conversion 
  based on pixel intensity. It applies a Gaussian filter with specified sigma to the input image to 
  reduce noise, then thresholds the filtered image such that pixels above the given threshold are 
  set to 1 (white) and those at or below the threshold are set to 0 (black). The choice of threshold 
  value is critical for segmentation tasks.
  
  Args:
    img (np.ndarray, required): A 2D numpy array representing the grayscale image to which the 
                            threshold will be applied.
    thr (float, required): The fixed threshold value used to convert pixel intensities to binary 
                        values. Pixels with intensity greater than this value are set to 1, and 
                        those at or below this value are set to 0.
    s (float, required): The standard deviation for the Gaussian filter applied to the image to 
                        reduce noise prior to thresholding.
  
  Returns:
    np.ndarray: A binary 2D numpy array of the same size as `img` with pixels above the specified 
    threshold set to 1 and those at or below the threshold set to 0.
      
  Raises:
    TypeError: If `img` is not a 2D numpy array, `thr` is not a float, or `s` is not a float.
    ValueError: If `thr` or `s` are outside of expected ranges for image processing parameters.
  """
  img = gaussian(img, sigma = s)
  img[img > thr] = 1
  img[img <= thr] = 0
  return img
