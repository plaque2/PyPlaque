import numpy as np
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops, moments
from phenotypes import Plaque
from plq_utils import check_numbers, fixed_threshold


class PlateImage:
    """
    **PlateImage Class** is aimed to contain a full multititre plate image and
    it's respective binary mask.

    _Arguments_:

    n_rows - (int, required) number of rows in the plate (usually lower than
    the number of rows).

    n_columns - (int, required) number of columns in the plate (usually higher than
    the number of rows).

    plate_image - (np.array, required) an image of individual wells of the
    plate.

    plate_mask - (np.array, required) a binary mask outlining individual wells of the
    plate.
    """
    def __init__(self, n_rows, n_columns, plate_image, plate_mask):
        #check data types
        if not type(n_rows) is int:
            raise TypeError("Expected n_rows argument to be int")
        if not type(n_columns) is int:
            raise TypeError("Expected n_columns argument to be int")
        if (not type(plate_image) is np.ndarray) or (not 2 >= plate_image.ndim <= 3):
            raise TypeError("Image atribute of the plate must be a 2D or 3D numpy array")
        if (not type(plate_mask) is np.ndarray) or (not plate_mask.ndim == 2):
            raise TypeError("Mask atribute of the plate must be a 2D numpy array")
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.plate_image = plate_image
        self.plate_mask = plate_mask

    def get_wells(self, min_area = 100):
        """
        **get_wells method** returns a list of individual wells of the plate
        stored as binary numpy arrays.
        """
    # ToDo: automated calculation of well row and col from x,y position
        well_crops = []
        for idx,well in enumerate(regionprops(label(clear_border(self.image)))):
            if well.area >= min_area:
                minr, minc, maxr, maxc = well.bbox
                masked_img = self.image ** well
                well_crops.append(masked_img[minr:maxr, minc:maxc])
        return well_crops