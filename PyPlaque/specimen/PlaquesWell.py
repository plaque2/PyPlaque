import numpy as np


class PlaquesWell:
  """
  **Class PlaquesWell** is aimed to contain a full well of a multititre plate.

  _Arguments_:

  row - (int or str, required) row id of the well.

  column - (int or str, required) column id of the well.

  well_image - (np.array, required) numpy array containing image of
  the well.

  well_mask  - (np.array, required) numpy array containing binary mask of
  the well.
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

  def get_image(self):
    """
    **get_image method** returns masked image of the well.
    """

    return self.well_image ** self.well_mask
