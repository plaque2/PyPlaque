import cv2
import numpy as np
from skimage.measure import label, regionprops


from PyPlaque.utils import check_numbers, picks_area, picks_perimeter


class Plaque:
  """
  **Plaque** class is designed to hold a single virological plaque
  phenotype as an object.

  _Arguments_:

  mask - (required, 2D numpy array) containing binary mask of a single
  virological plaque object.

  centroid - (float tuple, optional) contains x and y of the centroid of the
  plaque object

  bbox - (float tuple, optional) contains minr, minc, maxr, maxc of the
  plaque object
  """

  def __init__(self, mask, centroid = None, bbox = None, use_picks=True):
    #check data types
    if (not isinstance(mask, np.ndarray)) or (not mask.ndim == 2):
      raise TypeError("Mask atribute of Plaque must be a 2D numpy array")

    self.mask = mask
    self.use_picks = use_picks

    if self.use_picks:
      self.area = picks_area(mask)
      self.perimeter = picks_perimeter(mask)
    else:
      self.area = regionprops(label(mask))[0].area
      self.perimeter = regionprops(label(mask))[0].perimeter

    if centroid:
      if (not isinstance(centroid, tuple)) or check_numbers(centroid):
        raise TypeError("centroid must be a tuple of coordinates")
      self.centroid = centroid
    if bbox:
      if (not isinstance(bbox, tuple)) or check_numbers(bbox):
        raise TypeError("Bounding box must be a tuple of limits")
      self.bbox = bbox


  def measure(self):
    """
    **measure method** returns for an individual plaque object,the area of the
    bbox surrounding a plaque, and an approximation of the actual area based on
    the proportion of white pixels in the mask.

    _Arguments_:
    """
    plq_bbox_area = (self.bbox[3] - self.bbox[1]) * (self.bbox[2]
    - self.bbox[0]) # assuming bbox = (minr, minc, maxr, maxc)

    if self.use_picks:
      plq_area = self.area
    else:
      plq_area = np.sum(self.mask > 0)  # extracting non-white pixels

    return plq_bbox_area, plq_area

  def eccentricity(self):
    """
    **eccentricity method** returns for an individual plaque object,the eccentricity of the 
    plaque which is found by fitting an ellipse to the plaque boundary and finding the eccentricity 
    given by sqrt(1-(b^2/a^2)) where b is the length of the semi-minor axis and a is the length of 
    the semi-major axis.

    _Arguments_:
    """
    # find the contours
    contours,_ = cv2.findContours(self.mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    ecc = 0
    # select the first contour that has more than 5 points and fit an ellipse based on that
    if len(contours) != 0:
        for i in range(len(contours)):
            if len(contours[i]) >= 5:
                # fit the ellipse
                ellipse=cv2.fitEllipse(contours[i])
                if ellipse[2] == 0: #if rotation angle is zero results are not reliable
                    ecc = 0
                else:
                    semi_major_axis = ellipse[1][0]/2
                    semi_minor_axis = ellipse[1][1]/2

                    if semi_minor_axis > semi_major_axis:
                        temp = semi_minor_axis
                        semi_minor_axis = semi_major_axis
                        semi_major_axis = temp

                    if semi_minor_axis == 0:
                        semi_minor_axis = 0.1
                    if semi_major_axis == 0:
                        semi_major_axis = 0.1
                    ecc = np.sqrt(1-(semi_minor_axis**2/semi_major_axis**2))
                    break
    else:
        ecc = 0
    return ecc

  def roundness(self):
    """
    **roundness method** returns for an individual plaque object,the roundness of the plaque 
    which is found by the following ratio given by 4 * pi * Area / ( Perimeter^2 ) where 
    Area is 4 * pi * radius^2 and Perimeter is 2 * pi * radius.

    _Arguments_:
    """
    _, plq_area = self.measure()

    if self.use_picks:
      if self.perimeter != 0:
        roundness = 4 * np.pi * plq_area / (self.perimeter ** 2 )
      else:
        roundness = 0
    else:
      point1 = np.array((self.bbox[3],self.bbox[2])) #top right corner
      point2 = np.array(((self.bbox[3]+self.bbox[1])/2,(self.bbox[2]+self.bbox[0])/2)) #centre
      radius = np.linalg.norm(point1 - point2) #distance between top right corner and centre
      perimeter = 2 * np.pi * radius
      if perimeter != 0:
        roundness = 4 * np.pi * plq_area / ( perimeter ** 2 )
      else:
        roundness = 0
    return roundness
