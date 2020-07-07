class PlaqueImage:
    """
    PlaqueImage class designed to hold versatile image data containing multiple
    plaque phenotypes.

    _Arguments_:
    name - (str, required) string, image sample name for identification

    image - (np.array, required) numpy array containing 2D grayscale image of
    a virological plaque object, respective to the mask. Used, in case of
    measuring properties of fluorescent plaque image.

    plaques_mask - (np.array, optional, default None) numpy array containing
    binary mask of all virological plaque objects.
    """

    def __init__(self, name, image, plaques_mask = None):
        # check types
        if not type(name) is str:
            raise TypeError("Image name atribute must be a str")
        if (not type(image) is np.ndarray) or (not image.ndim == 2):
            raise TypeError("Image atribute must be a 2D numpy array")

        self.name = name
        self.image = image
        if plaques_mask:
            if (not type(plaques_mask) is np.ndarray) or (not plaques_mask.ndim == 2):
                raise TypeError("Mask atribute must be a 2D numpy array")
            self.plaques_mask = plaques_mask

class PlaqueImageRGB:
    """
    PlaqueImageCV class designed to hold versatile image data containing
    multiple plaque phenotypes.

    _Arguments_:
    name - (str, required) image sample name for identification

    image - (np.array, required) 3D (red, green, blue) numpy array
    containing image of a virological plaque object, respective to the mask.
    Used, e.g. in case of measuring properties of crystal violet plaque image.

    mask - (np.array, required) numpy array containing binary mask of a single
    virological plaque object.
    """
    def __init__(self, name, image, plaques_mask):
        # check types
        if not type(name) is str:
            raise TypeError("Image name atribute must be a str")
        if (not type(image) is np.ndarray) or (not image.ndim == 2):
            raise TypeError("Image atribute must be a 2D numpy array")
        if (not type(plaques_mask) is np.ndarray) or (not plaques_mask.ndim == 2):
            raise TypeError("Mask atribute must be a 2D numpy array")

        self.name = name
        self.image = image
        self.plaques_mask = plaques_mask

class PlaqueWell(PlaqueImage):
    """
    Class inherits from PlaqueImage and contains a full well.

    _Additonal arguments_:
    row - (int or str, required) row id of the well.

    column - (int or str, required) column id of the well.
    """

    def __init__(self, row, column, well_mask = None):
        super(PlaqueWell, self).__init__()
        #check data types
        if (not type(row) is int) or (not type(row) is str):
            raise TypeError("Expected n_rows argument to be int or str")
        if (not type(column) is int) or (not type(column) is str):
            raise TypeError("Expected n_columns argument to be int or str")
        self.row = row
        self.column = column
        if well_mask:
            if (not type(well_mask) is np.ndarray) or (not well_mask.ndim == 2):
                raise TypeError("Mask atribute of the plate must be a 2D numpy array")
            self.well_mask = well_mask

class PlateImage(PlaqueImage):
    """
    Class inherits from PlaqueImage and contains a full well.

    _Additonal arguments_:
    n_rows - (int, required) number of rows in the plate (usually lower than
    the number of rows).

    n_columns - (int, required) number of columns in the plate (usually higher than
    the number of rows).

    plate_mask - (np.array, required) a binary mask outlining individual wells of the
    plate.
    """

    def __init__(self, n_rows, n_columns, plate_mask):
        super(PlateImage, self).__init__()
        #check data types
        if not type(n_rows) is int:
            raise TypeError("Expected n_rows argument to be int")
        if not type(n_columns) is int:
            raise TypeError("Expected n_columns argument to be int")
        if (not type(plate_mask) is np.ndarray) or (not plate_mask.ndim == 2):
            raise TypeError("Mask atribute of the plate must be a 2D numpy array")
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.plate_mask = plate_mask
