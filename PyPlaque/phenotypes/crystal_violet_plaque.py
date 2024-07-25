import numpy as np

from PyPlaque.phenotypes import Plaque
from PyPlaque.utils import check_numbers


class CrystalVioletPlaque(Plaque):
  """
  **CrystalVioletPlaque Class**
  This class contains a plaque obtained from crystal violet image. Class inherits from Plaque class 
  and is also designed to hold a single virological plaque phenotype.
    
  Args:
    mask (2D numpy array, required): A binary mask representing a single virological plaque 
                                    object.
    
    image (numpy array, required): A numpy array containing either an RGB or grayscale image of 
                                  a single virological plaque object. The array should have 
                                  dimensions between 2 and 3 inclusive.
    
    centroid (float tuple, optional): A tuple containing the x and y coordinates of the centroid 
                                    of the plaque.
    
    bbox (float tuple, optional): A tuple containing the minr, minc, maxr, maxc limits of the 
                                bounding box surrounding the plaque.

  Raises:
    TypeError: If the mask is not a 2D numpy array, if image is not a 2D or 3D numpy array with 
    dimensions between 2 and 3 inclusive, if centroid is not a tuple of coordinates, or if bbox 
    is not a tuple of limits.
  """
  def __init__(self, mask, image, centroid = None, bbox = None):
    #check data types
    if (not isinstance(mask, np.ndarray)) or (not mask.ndim == 2):
      raise TypeError("Mask atribute of Plaque must be a 2D numpy array")
    if centroid:
      if (not isinstance(centroid, tuple)) or check_numbers(centroid):
        raise TypeError("centroid must be a tuple of coordinates")
      self.centroid = centroid
    if bbox:
      if (not isinstance(bbox, tuple)) or check_numbers(bbox):
        raise TypeError("Bounding box must be a tuple of limits")
      self.bbox = bbox

    super(CrystalVioletPlaque, self).__init__(mask, centroid, bbox)

    #check data types
    if (not isinstance(image, np.ndarray)) or ( not
    (mask.ndim >=2 and mask.ndim <= 3)):
      raise TypeError("Image atribute of Crystal Violet Plaque must be a 2D or \
      3D numpy array")
    self.image = image
