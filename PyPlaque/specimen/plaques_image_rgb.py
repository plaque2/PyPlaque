import numpy as np

from PyPlaque.specimen import PlaquesMask


class PlaquesImageRGB(PlaquesMask):
  """
  **PlaquesImageRGB Class** 
  The class is designed to hold RGB image data containing multiple plaque phenotypes with a 
  respective binary mask. The class inherits from PlaquesMask.
    
  Attributes:
    name (str, required): A string representing the name or identifier for the image sample. 
    
    image (np.ndarray, required): A 3D numpy array containing RGB image data of a virological 
                                plaque object, corresponding to the mask. 

    plaques_mask (np.ndarray, required): A 2D numpy array representing the binary mask of all 
                                      virological plaque objects. 

    use_picks (bool, optional): Indicates whether to use pick-based area calculation. 
                              Defaults to False.

  Raises:
    TypeError: If `name` is not a string, if `image` is not a 3D numpy array, or if `plaques_mask` 
    is not a 2D numpy array.
  """
  def __init__(self, name, image, plaques_mask, use_picks=False):
    # check types
    if not isinstance(name, str):
      raise TypeError("Image name atribute must be a str")
    if (not isinstance(image, np.ndarray)) or (not image.ndim == 3):
      raise TypeError("Image atribute must be a 3D (RGB) numpy array")
    if (not isinstance(plaques_mask, np.ndarray)) or (not plaques_mask.ndim
    == 2):
      raise TypeError("Mask atribute must be a 2D numpy array")

    super(PlaquesImageRGB, self).__init__(name, plaques_mask,use_picks)
    self.image = image
