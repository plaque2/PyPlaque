import numpy as np


class PlaquesWell:
  """
  **PlaquesWell Class** is aimed to contain a full well of a multititre plate.
  
  This class encapsulates methods to handle and manipulate images related to the plaques 
  within the well.
  
  Attributes:
    row (int or str): The identifier for the row where the well is located in the plate.

    column (int or str): The identifier for the column where the well is located in the plate.

    well_image (np.ndarray): A 2D or 3D numpy array representing the image of the well.

    well_mask (np.ndarray): A 2D numpy array representing a binary mask of the well, used for 
                          various purposes such as highlighting specific areas in the image.

  Raises:
    TypeError: If `row` or `column` is not an integer or string; if `well_image` is not a 2D or 
    3D numpy array; if `well_mask` is not a 2D numpy array.
  """

  def __init__(self, row, column, well_image, well_mask):
    #check data types
    if not (isinstance(row, int) or isinstance(row, str)):
      raise TypeError("Expected row argument to be int or str")
    if not (isinstance(column, int) or isinstance(column, str)):
      raise TypeError("Expected column argument to be int or str")
    if not isinstance(well_image, np.ndarray) or (not (well_image.ndim >=2
    and well_image.ndim <= 3)):
      raise TypeError("Image atribute of the plate must be a 2D or 3D \
      numpy array")
    if not isinstance(well_mask, np.ndarray) or (not well_mask.ndim == 2):
      raise TypeError("Mask atribute of the plate must be a 2D numpy array")
    self.row = row
    self.column = column
    self.well_image = well_image
    self.well_mask = well_mask

  def get_masked_image(self):
    """
    **get_masked_image Method** 
    The method returns the masked image of the well. It applies a mask to the well image by 
    element-wise multiplication between `well_image` and `well_mask`. This is typically used for 
    visualizations or further processing where specific regions are highlighted or removed based 
    on the mask.

    Args:
    
    Returns:
      np.ndarray: A masked version of the well image, where each pixel value is a result of 
      multiplying corresponding pixels in `well_image` and `well_mask`.
    """

    return self.well_image ** self.well_mask
