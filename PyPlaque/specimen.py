from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from phenotypes import Plaque

class PlaquesMask:
    """
    *PlaquesMask class* designed to hold binary mask of multiple
    plaque phenotypes.

    __Arguments__:

    name - (str, required) string, image sample name for identification

    plaques_mask - (np.array, required) numpy array containing
    binary mask of all virological plaque objects.
    """
    def __init__(self, name, plaques_mask):
        # check types
        if not type(name) is str:
            raise TypeError("Image name atribute must be a str")
        if (not type(plaques_mask) is np.ndarray) or (not image.ndim == 2):
            raise TypeError("plaques_mask atribute must be a 2D numpy array")

        self.name = name
        self.plaques_mask = plaques_mask

    def iterate_plaques(self, min_area = 100):
        """
        *iterate_palques method* returns a list of individual plaques
        stored as binary numpy arrays.

        __Arguments__:

        min_are - (int, optional, default = 100) a cut-off value for plaque area
        in px.
        """
        plaques_list = []
        for idx,plaque in enumerate(regionprops(
                                    label(
                                    clear_border(self.plaques_mask)))):
            if plaque.area >= min_area:
                    minr, minc, maxr, maxc = plaque.bbox
                    plq = Plaque(plaque[minr:maxr, minc:maxc],
                                        (minr, minc, maxr, maxc))
                    plaques_crops.append(plq)
        return plaques_list

class PlaquesImageGray(PlaquesMask):
    """
    *PlaqueImageGray class* designed to hold grayscale image data containing
    multiple plaque phenotypes with a respective binary mask. The class inherits
    from PlaquesMask.

    __Additonal arguments__:

    name - (str, required) string, image sample name for identification

    image - (np.array, required) numpy array containing 2D grayscale image of
    a virological plaque object, respective to the mask. Used, in case of
    measuring properties of fluorescent plaque image.

    plaques_mask - (np.array, optional, default None) numpy array containing
    binary mask of all virological plaque objects.


    """

    def __init__(self, name, image, plaques_mask = None, threshold = None):
        super(PlaquesImageGray, self).__init__()
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
        else

class PlaquesImageRGB(PlaquesMask):
    """
    *PlaquesImageRGB class* designed to hold RGB image data containing
    multiple plaque phenotypes with a respective binary mask.The class inherits
    from PlaquesMask.

    __Additonal arguments__:

    name - (str, required) image sample name for identification

    image - (np.array, required) 3D (red, green, blue) numpy array
    containing image of a virological plaque object, respective to the mask.
    Used, e.g. in case of measuring properties of crystal violet plaque image.

    plaques_mask - (np.array, required) numpy array containing binary mask of all
    virological plaque objects.
    """
    def __init__(self, name, image, plaques_mask):
        super(PlaquesImageRGB, self).__init__()
        # check types
        if not type(name) is str:
            raise TypeError("Image name atribute must be a str")
        if (not type(image) is np.ndarray) or (not image.ndim == 3):
            raise TypeError("Image atribute must be a 3D (RGB) numpy array")
        if (not type(plaques_mask) is np.ndarray) or (not plaques_mask.ndim == 2):
            raise TypeError("Mask atribute must be a 2D numpy array")

        self.name = name
        self.image = image
        self.plaques_mask = plaques_mask

class PlaquesWell():
    """
    *Class PlaquesWell* is aimed to contain a full well of a multititre plate.

    __Arguments__:

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

    """

        return self * self.well_mask

class PlateImage():
    """
    *PlateImage Class* is aimed to contain a full multititre plate image and
    it's respective binary mask.

    __Arguments__:

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

    def iterate_wells(self, min_area = 100):
        """
        *Iterate_wells method* returns a list of individual wells of the plate
        stored as binary numpy arrays.
        """
        well_crops = []
        for idx,well in enumerate(regionprops(label(clear_border(img)))):
            if well.area >= min_area:
                    minr, minc, maxr, maxc = well.bbox
                    masked_img = self.image * well
                    well_crops.append(masked_img[minr:maxr, minc:maxc])
        return well_crops
