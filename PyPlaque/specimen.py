class PlaqueImage:
    """
    PlaqueImage class designed to hold versatile image data containing multiple
    plaque phenotypes.

    _Arguments_:
    name - (required) string, image sample name for identification

    grayscale - (required) numpy array containing masked grayscale image of
    a virological plaque object, respective to the mask. Used, in case of
    measuring properties of fluorescent plaque image.

    mask - (optional, default None) numpy array containing binary mask of a single
    virological plaque object.
    """

    def __init__(self, name, grayscale, mask = None):
        #super(, self).__init__()
        self.name = name
        self.image = image
        if mask:
            self.mask = mask

class PlaqueImageCV:
    """
    PlaqueImageCV class designed to hold versatile image data containing multiple
    plaque phenotypes.

    _Arguments_:
    name - (required) string, image sample name for identification

    rgb - (required) 3-D (red, green, blue) numpy array containing masked rgb image of
    a virological plaque object, respective to the mask. Used, e.g. in case of
    measuring properties of crystal violet plaque image.

    mask - (required) numpy array containing binary mask of a single
    virological plaque object.

    """
    def __init__(self, name, image, mask):
        #super(, self).__init__()
        self.name = name
        self.mask = mask
        self.image = image

class PlaqueWell(PlaqueImage):
    """
    Class inherits from PlaqueImage and contains a full well.

    _Additonal arguments_:
    row - (required) row id of the well.

    column - (required) column id of the well.
    """

    def __init__(self, row, column):
        #super(, self).__init__()
        self.row = row
        self.column = column

class PlateImage(PlaqueImage):
    """
    Class inherits from PlaqueImage and contains a full well.

    _Additonal arguments_:
    n_rows - (required) number of rows in the plate (usually lower than
    the number of rows).

    n_columns - (required) number of columns in the plate (usually higher than
    the number of rows).
    """

    def __init__(self, n_rows, n_columns):
        #super(, self).__init__()
        self.n_rows = n_rows
        self.n_columns = n_columns
