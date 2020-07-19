import numpy as np

class Plaque:
    """
    Plaque object class is designed to hold a single virological plaque
    phenotype.

    __Arguments__:

    mask - (required, 2D numpy array) containing binary mask of a single
    virological plaque object.

    centroid - (float tuple, optional) contains x and y of the centroid of the 
    plaque object

    bbox - (float tuple, optional) contains minr, minc, maxr, maxc of the
    plaque object


    """

    def __init__(self, mask, centroid = None, bbox = None):
        #check data types
        if (not type(mask) is np.ndarray) or (not mask.ndim == 2):
            raise TypeError("Mask atribute of Plaque must be a 2D numpy array")
        self.mask = mask
        if centroid:
            self.centroid = centroid
        if bbox:
            self.bbox = bbox


    def measure(self):
        pass

class PlaqueFluorescence(Plaque):
    """
    Plaque obtain from fluorescence image. Class inherits from Plaque class and
    is also designed to hold a single virological plaque phenotype.

    __Additonal arguments__:
    image - (required) numpy array containing grayscale image of a single
    virological plaque object.
    """
    def __init__(self, mask, image):
        super(PlaqueFluorescence, self).__init__(mask)
        #check data types
        if (not type(mask) is np.ndarray) or (not mask.ndim == 2):
            raise TypeError("Mask atribute of Plaque must be a 2D numpy array")
        if (not type(image) is np.ndarray) or (not image.ndim == 2):
            raise TypeError("Image atribute of Plaque must be a 2D numpy array")
        self.image = image

    def find_peak(self):
        pass

class PlaqueCrystalViolet(Plaque):
    """
    Plaque obtained from crystal violet image. Class inherits from Plaque class and
    is also designed to hold a single virological plaque phenotype.

    __Additonal arguments__:
    image - (required) numpy array containing RGB or a graysacle image of a
    single virological plaque object.
    """
    def __init__(self, mask, image):
        super(PlaqueCrystalViolet, self).__init__(mask)
        #check data types
        if (not type(image) is np.ndarray) or (not 2 == mask.ndim <= 3):
            raise TypeError("Image atribute of Crystal Violet Plaque must be a 2D or 3D numpy array")
        self.image = image
