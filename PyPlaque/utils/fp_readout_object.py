import numpy as np
import skimage


class PlaqueObjectReadout():
  """
  **Class PlaqueObjectReadout** is aimed to contain data of a single instance
  of a plaque/nuclei of a single well of a Fluorescence Plaque.

  _Arguments_:

  nuclei_image_name - (str, required) name of nuclei image plate.

  nuclei_object - (np.array, required) image of the nuclei plate.

  nuclei_object_mask - (np.array, required) image of the nuclei plate mask.

  plaque_image_name - (str, required) name of plaque image plate.

  plaque_object - (np.array, required) image of the plaque plate.

  plaque_object_mask - (np.array, required) image of the plaque plate mask.
  """
  def __init__(self,
                nuclei_image_name,
                plaque_image_name,
                nuclei_object,
                plaque_object,
                nuclei_object_mask,
                plaque_object_mask,
                plaque_object_properties,
                virus_params):

    #check data types
    if not isinstance(nuclei_image_name, str):
      raise TypeError('Expected nuclei_image_name argument to be str')
    if not isinstance(plaque_image_name, str):
      raise TypeError('Expected nuclei_image_name argument to be str')
    if (not isinstance(nuclei_object_mask, np.ndarray)) or (not
    nuclei_object_mask.ndim == 2):
      raise TypeError('Mask atribute of well must be a 2D numpy array')
    if (not isinstance(plaque_object_mask, np.ndarray)) or (not
    plaque_object_mask.ndim == 2):
      raise TypeError('Mask atribute of well must be a 2D numpy array')
    if (not isinstance(nuclei_object, np.ndarray)) or (not nuclei_object.ndim
    == 2):
      raise TypeError('Image atribute of well must be a 2D numpy array')
    if (not isinstance(plaque_object, np.ndarray)) or (not plaque_object.ndim
    == 2):
      raise TypeError('Image atribute of well must be a 2D numpy array')
    if not isinstance(virus_params, dict):
      raise TypeError('Virus params attribute must be a dictionary')

    self.nuclei_object_mask = nuclei_object_mask
    self.nuclei_object = nuclei_object
    self.nuclei_image_name = nuclei_image_name
    self.plaque_object_mask = plaque_object_mask
    self.plaque_object = plaque_object
    self.plaque_image_name = plaque_image_name
    self.params = virus_params
    self.plaque_object_properties = plaque_object_properties

  def get_row(self):
    return self.nuclei_image_name.split('_')[1][0]

  def get_column(self):
    return self.nuclei_image_name.split('_')[1][1:]

  def get_area(self):
    return np.sum(self.plaque_object_mask)

  def get_centroid(self):
    return self.plaque_object_properties.centroid

  def get_bbox(self):
    return (self.plaque_object_properties.bbox[0], \
            self.plaque_object_properties.bbox[3], \
            self.plaque_object_properties.bbox[2]
            - self.plaque_object_properties.bbox[0], \
            self.plaque_object_properties.bbox[3]
            - self.plaque_object_properties.bbox[1])

  def get_major_minor_axis_length(self):
    return self.plaque_object_properties.axis_major_length, \
            self.plaque_object_properties.axis_minor_length

  def get_eccentricity(self):
    return self.plaque_object_properties.eccentricity

  def get_convex_area(self):
    return self.plaque_object_properties.area_convex

  def roundness(self):
    point1 = np.array((self.plaque_object_properties.bbox[3],
                        self.plaque_object_properties.bbox[2]))
    point2 = np.array(((self.plaque_object_properties.bbox[3] \
                        +self.plaque_object_properties.bbox[1])/2,
                        (self.plaque_object_properties.bbox[2] \
                          +self.plaque_object_properties.bbox[0])/2))
    radius = np.linalg.norm(point1 - point2)
    perimeter = 2 * np.pi * radius
    ratio = 4 * np.pi * self.get_area() / ( perimeter ** 2 )
    return 1-ratio

  def get_number_of_peaks(self):
    globalPeakCoords=[]
    (x1,y1,_,_) = self.plaque_object_properties.bbox
    curPlqRegion= self.plaque_object * self.plaque_object_properties.image

    #fine detection
    blurredImage = skimage.filters.gaussian(curPlqRegion,
                        sigma=self.params['plaque_gaussian_filter_sigma'],
                        truncate = self.params['plaque_gaussian_filter_size']/
                            self.params['plaque_gaussian_filter_sigma'] )

    coordinates = skimage.feature.peak_local_max(blurredImage,
                                  min_distance=self.params['peak_region_size'],
                                  exclude_border = False)

    globalPeakCoords = np.array([coordinates[:, 0] + x1,
    coordinates[:, 1] + y1]).T

    return globalPeakCoords

  def get_nuclei_in_plaque(self):
    mask = self.plaque_object_properties.image_convex * self.nuclei_object_mask
    # labelImage = measure.label(mask)
    # labelImage[~mask] = 0
    # props = measure.regionprops(labelImage)
    # nuclei_area_sum = 0
    # for prop in props:
    #     if  self.params['minCellArea'] < prop.area:
    #         nuclei_area_sum+=np.sum(prop.image)
    nuclei_area_sum = np.sum(mask)
    return nuclei_area_sum/((self.params['minCellArea'] +
    self.params['maxCellArea'])/2)

  def get_infected_nuclei_in_plaque(self):
    mask = self.plaque_object_mask * self.nuclei_object_mask
    # labelImage = measure.label(mask)
    # labelImage[~mask] = 0
    # props = measure.regionprops(labelImage)
    # nuclei_area_sum = 0
    # for prop in props:
    #     if  self.params['minCellArea'] < prop.area:
    #         nuclei_area_sum+=np.sum(prop.image)
    nuclei_area_sum = np.sum(mask)
    return nuclei_area_sum/((self.params['minCellArea'] +
    self.params['maxCellArea'])/2)

  def get_max_intensity_GFP(self):
    return np.max(self.plaque_object*self.plaque_object_mask)
    #creating a masked image

  def get_total_intensity_GFP(self):
    return np.sum(self.plaque_object*self.plaque_object_mask)
    #creating a masked image

  def get_mean_intensity_GFP(self):
    if len(np.nonzero(self.plaque_object*self.plaque_object_mask)[0])==0:
      return 0
    else:
      return np.mean(np.nonzero(self.plaque_object*self.plaque_object_mask))
    #creating a masked image