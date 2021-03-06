import numpy as np
from skimage.measure import label, regionprops, moments
from PyPlaque.phenotypes import Plaque
from PyPlaque.utils import check_numbers


class CrystalVioletPlaque(Plaque):
    """
    **CrystalVioletPlaque** plaque obtained from crystal violet image. Class
    inherits from Plaque class and is also designed to hold a single virological
    plaque phenotype.

    _Additonal arguments_:

    image - (required) numpy array containing RGB or a graysacle image of a
    single virological plaque object.
    """
    def __init__(self, mask, image, centroid = None, bbox = None):
        #check data types
        if (not type(mask) is np.ndarray) or (not mask.ndim == 2):
            raise TypeError("Mask atribute of Plaque must be a 2D numpy array")
        if centroid:
            if (not type(centroid) is tuple) or check_numbers(centroid):
                raise TypeError("centroid must be a tuple of coordinates")
            self.centroid = centroid
        if bbox:
            if (not type(bbox) is tuple) or check_numbers(bbox):
                raise TypeError("Bounding box must be a tuple of limits")
            self.bbox = bbox

        super(CrystalVioletPlaque, self).__init__(mask, centroid, bbox)
        
        #check data types
        if (not type(image) is np.ndarray) or (not 2 == mask.ndim <= 3):
            raise TypeError("Image atribute of Crystal Violet Plaque must be a 2D or 3D numpy array")
        self.image = image
