import numpy as np
from PyPlaque.specimen import PlaquesMask


class PlaquesImageRGB(PlaquesMask):
    """
    **PlaquesImageRGB class** designed to hold RGB image data containing
    multiple plaque phenotypes with a respective binary mask.The class inherits
    from PlaquesMask.

    _Additonal arguments_:

    name - (str, required) image sample name for identification

    image - (np.array, required) 3D (red, green, blue) numpy array
    containing image of a virological plaque object, respective to the mask.
    Used, e.g. in case of measuring properties of crystal violet plaque image.

    plaques_mask - (np.array, required) numpy array containing binary mask of all
    virological plaque objects.
    """
    def __init__(self, name, image, plaques_mask):
        # check types
        if not type(name) is str:
            raise TypeError("Image name atribute must be a str")
        if (not type(image) is np.ndarray) or (not image.ndim == 3):
            raise TypeError("Image atribute must be a 3D (RGB) numpy array")
        if (not type(plaques_mask) is np.ndarray) or (not plaques_mask.ndim == 2):
            raise TypeError("Mask atribute must be a 2D numpy array")
        
        super(PlaquesImageRGB, self).__init__(name, plaques_mask)
        self.image = image