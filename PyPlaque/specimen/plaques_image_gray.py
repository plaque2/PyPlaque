import numpy as np

from PyPlaque.specimen import PlaquesMask
from PyPlaque.utils import fixed_threshold


class PlaquesImageGray(PlaquesMask):
  """
  **PlaqueImageGray Class** 
  This class is designed to hold grayscale image data containing multiple plaque phenotypes with a 
  respective binary mask. The class inherits from PlaquesMask.
    
  Args:
    name (str, required): A string representing the name or identifier for the image sample. 

    image (np.ndarray,  required): A 2D numpy array containing grayscale image data of a 
                                  virological plaque object, corresponding to the mask. 

    plaques_mask (np.ndarray, optional): A 2D numpy array representing the binary mask of all 
                                        virological plaque objects. Defaults to None.

    threshold (float, optional): A float between 0 and 1 representing a fixed threshold value for 
                              creating the binary mask. Defaults to None.

    sigma (int, optional): An integer representing the Gaussian blur sigma in pixels used by the 
                        fixed thresholding approach. Defaults to 5.

    use_picks (bool, optional): Indicates whether to use pick-based area calculation. 
                              Defaults to False.

  Raises:
    TypeError: If `name` is not a string, if `image` is not a 2D numpy array, or if `plaques_mask` 
    is not provided and neither `threshold` nor `sigma` are specified.
    ValueError: If both `plaques_mask` and either `threshold` or `sigma` are not provided.
  """

  def __init__(self,
                name,
                image,
                plaques_mask = None,
                threshold = None,
                sigma = 5,
                use_picks = False):
    # check types
    if not isinstance(name, str):
      raise TypeError("Image name atribute must be a str")
    if (not isinstance(image, np.ndarray)) or (not image.ndim == 2):
      raise TypeError("Image atribute must be a 2D numpy array")

    if plaques_mask:
      if (not isinstance(plaques_mask, np.ndarray)) or (not plaques_mask.ndim
      == 2):
        raise TypeError("Mask atribute must be a 2D numpy array")
      self.plaques_mask = plaques_mask
    elif threshold and sigma:
      plaques_mask = fixed_threshold(image, threshold, sigma)
      self.plaques_mask = plaques_mask
    else:
      raise ValueError("Either mask or fixed threshold must be provided")

    super(PlaquesImageGray, self).__init__(name, plaques_mask,use_picks)
    self.image = image
    
