import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from skimage.measure import label, regionprops
from skimage.segmentation import clear_border

from PyPlaque.phenotypes import Plaque
from PyPlaque.utils import centroid


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
    if not isinstance(name, str):
      raise TypeError('Image name atribute must be a str')
    if (not isinstance(plaques_mask, np.ndarray)) or (not plaques_mask.ndim
    == 2):
      raise TypeError('plaques_mask atribute must be a 2D numpy array')

    self.name = name
    self.plaques_mask = plaques_mask

  def get_plaques(self, min_area = 100, max_area = 200):
    """
    **get_plaques method** returns a list of individual plaques
    stored as binary numpy arrays.

    _Arguments_:

    min_area - (int, optional, default = 100) a cut-off value for plaque area
    in px.

    max_area - (int, optional, default = 200) a cut-off value for plaque area
    in px.
    """
    if not isinstance(min_area, int):
      raise TypeError('minimum area parameter must be int')
    if not isinstance(max_area, int):
      raise TypeError('minimum area parameter must be int')

    plaques_list = []
    for _, plaque in enumerate(regionprops(
                                label(
                                clear_border(self.plaques_mask)))):
      if plaque.area >= min_area and plaque.area <= max_area:
        minr, minc, maxr, maxc = plaque.bbox
        plq = Plaque(self.plaques_mask[minr:maxr, minc:maxc], plaque.centroid,
                            (minr, minc, maxr, maxc))
        plaques_list.append(plq)
    return plaques_list


  def get_measure(self, plaques_list):
    """
    **get_measure method** returns a list of measurements based on the input of
    list of plaques as a dictionary. For cumulative measurements as compared to
    the measure method under class PyPlaque.phenotypes.Plaque that gives
    granular measurements based on each plaque.

    _Arguments_:

    plaques_list - (list, required) a list of object of type
    PyPlaque.phenotypes.Plaque from which several measures can be calculated.
    """
    plq_area_ls = []
    plq_ecc_ls = []
    plq_round_ls = []
    measure_dict = {}
    centre_ls = []

    cent0 = 0
    cent1 = 0

    mean_plq_size = 0
    med_plq_size = 0

    for plq in plaques_list:
      _, plq_area = plq.measure()
      plq_area_ls.append(plq_area)
      plq_ecc_ls.append(plq.eccentricity())
      plq_round_ls.append(plq.roundness())

      mean_plq_size = np.mean(plq_area_ls)
      med_plq_size = np.median(plq_area_ls)

      centre_ls.append([(plq.bbox[3]+plq.bbox[1])/2,
      (plq.bbox[2]+plq.bbox[0])/2])

    cent0, cent1 = centroid(np.array(centre_ls))

    measure_dict['mean_plq_size'] = mean_plq_size
    measure_dict['med_plq_size'] = med_plq_size
    measure_dict['centroid'] = [cent0,cent1]
    measure_dict['mean_plq_ecc'] = np.mean(plq_ecc_ls)
    measure_dict['mean_roundness'] = np.mean(plq_round_ls)

    self.plaques_list = plaques_list
    self.measure_dict = measure_dict

    return measure_dict

  def plot_centroid(self):
    """
    **plot_centroid method** plots a dotted ring around all the plaques that
    are found in the mask. This ring is centred at the centroid of all the
    centres of individual plaques found.

    _Arguments_:

    plaques_list - (list, required) a list of object of type
    PyPlaque.phenotypes.Plaque from which several measures can be calculated.
    """

    # Create a figure. Equal aspect so circles look circular
    _, ax = plt.subplots(1, figsize = (40,8))
    ax.set_aspect('equal')

    # Show the image
    ax.imshow(self.plaques_mask)

    max_margin = 0
    radius = 0
    point3 = np.array((self.measure_dict['centroid'][0],
    self.measure_dict['centroid'][1]))
    # Now, loop through coord arrays, and create a circle at each x,y pair
    for plq in self.plaques_list:
      point1 = np.array((plq.bbox[3],plq.bbox[2]))
      point2 = np.array(((plq.bbox[3]+plq.bbox[1])/2,
      (plq.bbox[2]+plq.bbox[0])/2))
      circ = Circle(((plq.bbox[3]+plq.bbox[1])/2,
      (plq.bbox[2]+plq.bbox[0])/2),np.linalg.norm(point1 - point2),
      fill = False, color = 'white')
      if np.linalg.norm(point1-point2) > max_margin :
        # measuring the max distance of plaque centre from their bbox corner
        max_margin = np.linalg.norm(point1-point2)

      if np.linalg.norm(point3 - point2) > radius:
        # measuring the max distance of plaque centres from centroid
        radius = np.linalg.norm(point3 - point2)
      ax.add_patch(circ)

    #This gives the maximum distance of a plaque bbox corner from the centroid
    # so that a circle can be drawn around the cluster of plaques
    main_circle = Circle((self.measure_dict['centroid'][0],
    self.measure_dict['centroid'][1]),radius+max_margin,
    fill = False, color = 'white')
    ax.add_patch(main_circle)

    # Show the image
    plt.show()
