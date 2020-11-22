import numpy as np
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops, moments
from PyPlaque.phenotypes import Plaque
from PyPlaque.utils import check_numbers, fixed_threshold


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
        if (not type(row) is int) or (not type(row) is str):
            raise TypeError("Expected n_rows argument to be int or str")
        if (not type(column) is int) or (not type(column) is str):
            raise TypeError("Expected n_columns argument to be int or str")
        if (not type(well_image) is np.ndarray) or (not 2 >= well_image.ndim <= 3):
            raise TypeError("Image atribute of the plate must be a 2D or 3D numpy array")
        if (not type(well_mask) is np.ndarray) or (not well_mask.ndim == 2):
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