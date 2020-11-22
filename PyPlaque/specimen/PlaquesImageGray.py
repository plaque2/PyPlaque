import numpy as np
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops, moments
from PyPlaque.phenotypes import Plaque
from PyPlaque.specimen import PlaquesMask
from PyPlaque.utils import check_numbers, fixed_threshold


class PlaquesImageGray(PlaquesMask):
    """
    **PlaqueImageGray class** designed to hold grayscale image data containing
    multiple plaque phenotypes with a respective binary mask. The class inherits
    from PlaquesMask.

    _Additonal arguments_:

    name - (str, required) string, image sample name for identification

    image - (np.array, required) numpy array containing 2D grayscale image of
    a virological plaque object, respective to the mask. Used, in case of
    measuring properties of fluorescent plaque image.

    plaques_mask - (np.array, optional, default None) numpy array containing
    binary mask of all virological plaque objects.

    threshold - (float between 0 and 1, optional, default None) fixed threshold
    value for creating the binary mask.

    sigma - (int, optional, default = 5) guassian blur sigma in pixels used by
    the fixed thresholding approach.

    Either mask or fixed threshold must be provided
    """

    def __init__(self, name, image, plaques_mask = None, threshold = None, sigma = 5):
         # check types
        if not type(name) is str:
            raise TypeError("Image name atribute must be a str")
        if (not type(image) is np.ndarray) or (not image.ndim == 2):
            raise TypeError("Image atribute must be a 2D numpy array")
        
        if plaques_mask:
            if (not type(plaques_mask) is np.ndarray) or (not plaques_mask.ndim == 2):
                raise TypeError("Mask atribute must be a 2D numpy array")
        elif threshold and sigma:
            plaques_mask = fixed_threshold(image, threshold, sigma)
        else:
            raise ValueError("Either mask or fixed threshold must be provided")
        
        super(PlaquesImageGray, self).__init__(name, plaques_mask)
        self.image = image
