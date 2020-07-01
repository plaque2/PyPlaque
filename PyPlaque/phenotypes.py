import numpy as np

class Plaque:
    """
    Plaque object class is designed to hold a single virological plaque
    phenotype.

    _Arguments_:
    mask - (required) numpy array containing binary mask of a single
    virological plaque object.
    """

    def __init__(self, mask):
        #super(, self).__init__()

        #check data types
        if not type(mask) is np.ndarray:
            raise TypeError("Mask atribute of Plaque must be a numpy array")
        self.mask = mask


    def measure(self):
        pass

class PlaqueFluorescence(Plaque):
    """
    Plaque obtain from fluorescence image. Class inherits from Plaque class and
    is also designed to hold a single virological plaque phenotype.

    _Additonal arguments_:
    image - (required) numpy array containing grayscale image of a single
    virological plaque object.
    """
    def __init__(self, image):
        #check data types
        if not type(image) is np.ndarray:
            raise TypeError("Image atribute of Plaque must be a numpy array")
        self.image = image

    def find_peak(self):
        pass

class PlaqueCrystalViolet(Plaque):
    """
    Plaque obtained from crystal violet image. Class inherits from Plaque class and
    is also designed to hold a single virological plaque phenotype.

    _Additonal arguments_:
    image - (required) numpy array containing RGB or a graysacle image of a
    single virological plaque object.
    """
    def __init__(self, image):
        #check data types
        if not type(mask) is np.ndarray:
            raise TypeError("Image atribute of Plaque must be a numpy array")
        self.image = image
