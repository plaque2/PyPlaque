import numpy as np
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops, moments
from phenotypes import Plaque
from plq_utils import check_numbers, fixed_threshold


class PlaquesMask:
    """
    **PlaquesMask class** designed to hold binary mask of multiple
    plaque phenotypes.

    _Arguments_:

    name - (str, required) string, image sample name for identification

    plaques_mask - (np.array, required) numpy array containing
    binary mask of all virological plaque objects.
    """
    def __init__(self, name, plaques_mask):
        # check types
        if not type(name) is str:
            raise TypeError("Image name atribute must be a str")
        if (not type(plaques_mask) is np.ndarray) or (not plaques_mask.ndim == 2):
            raise TypeError("plaques_mask atribute must be a 2D numpy array")

        self.name = name
        self.plaques_mask = plaques_mask

    def get_plaques(self, min_area = 100):
        """
        **get_palques method** returns a list of individual plaques
        stored as binary numpy arrays.

        _Arguments_:

        min_area - (int, optional, default = 100) a cut-off value for plaque area
        in px.
        """
        if not type(min_area) is int:
            raise TypeError("minimum are paprameter must be int")
        
        plaques_list = []
        for idx,plaque in enumerate(regionprops(
                                    label(
                                    clear_border(self.plaques_mask)))):
            if plaque.area >= min_area:
                    minr, minc, maxr, maxc = plaque.bbox
                    plq = Plaque(self.plaques_mask[minr:maxr, minc:maxc], plaque.centroid,
                                        (minr, minc, maxr, maxc))
                    plaques_list.append(plq)
        return plaques_list