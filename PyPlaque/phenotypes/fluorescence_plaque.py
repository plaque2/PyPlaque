import numpy as np

from PyPlaque.phenotypes import Plaque
from PyPlaque.utils import check_numbers


class FluorescencePlaque(Plaque):
  """
  **FluorescencePlaque** conains plaque obtained from fluorescence image.
  Class inherits from Plaque class and is also designed to hold a single
  virological plaque phenotype.

  _Additonal arguments_:

  image - (required) numpy array containing grayscale image of a single
  virological plaque object.
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

    super(FluorescencePlaque, self).__init__(mask, centroid, bbox)

    if (not isinstance(image, np.ndarray)) or (not image.ndim == 2):
      raise TypeError("Image atribute of Plaque must be a 2D numpy array")
    self.image = image
