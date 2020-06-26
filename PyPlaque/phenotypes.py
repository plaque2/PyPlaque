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
        self.image = image

    def find_peak(self):
        pass

class PlaqueCrystalViolet(Plaque):
    """
    Plaque obtain from fluorescence image. Class inherits from Plaque class and
    is also designed to hold a single virological plaque phenotype.

    _Additonal arguments_:
    image - (required) numpy array containing RGB or a graysacle image of a
    single virological plaque object.
    """
    def __init__(self, image):
        self.image = image
