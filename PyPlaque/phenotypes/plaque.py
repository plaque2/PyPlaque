import cv2
import numpy as np
from skimage.measure import label, regionprops


from PyPlaque.utils import check_numbers, picks_area, picks_perimeter


class Plaque:
  """
  **Plaque Class** 
  The Plaque class is designed to hold a single virological plaque phenotype as an object. It 
  encapsulates the properties and behaviors related to a specific plaque, including its mask, 
  centroid coordinates, bounding box, and usage preference for pick measurements.
    
  Args:
      mask (2D numpy array, required): A binary mask representing a single virological plaque 
      object.
      
      centroid (float tuple, optional): A tuple containing the x and y coordinates of the centroid 
      of the plaque.
      
      bbox (float tuple, optional): A tuple containing the minr, minc, maxr, maxc limits of the 
      bounding box surrounding the plaque.
      
      use_picks (bool, optional): A boolean flag indicating whether to use pick measurements or not. 
      Defaults to False.
  
  Raises:
      TypeError: If the mask is not a 2D numpy array, if centroid is not a tuple of coordinates, 
      or if bbox is not a tuple of limits.
  """

  def __init__(self, mask, centroid = None, bbox = None, use_picks=False):
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
    **measure Method** 
    Computes and returns the bounding box area (in pixels) of a plaque object, as well as an 
    approximation of its actual area based on the proportion of white pixels in the mask. The 
    method uses either the pre-computed `self.area` if available or calculates it from the binary 
    mask (`self.mask`) if not.
    
    Args:
      None: The method operates directly on the instance's attributes (`self.bbox`, 
      `self.use_picks`, `self.mask`, `self.area`).
        
    Returns:
      tuple: A tuple containing two elements, the first is the area of the bounding box 
      surrounding the plaque (in pixels), and the second is an approximation of the actual area 
      based on the mask (also in pixels).
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
    **eccentricity Method** 
    Calculates and returns the eccentricity of an individual plaque object. The eccentricity is 
    determined by fitting an ellipse to the plaque's boundary contour and using the formula 
    sqrt(1 - (b^2 / a^2)), where b represents the length of the semi-minor axis, and a represents 
    the length of the semi-major axis.
    
    Args:
      None: The method operates directly on the instance's attributes (`self.mask`).
        
    Returns:
      float: The calculated eccentricity value of the plaque.
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
    **roundness Method** 
    Calculates and returns the roundness of an individual plaque object. The roundness is calculated 
    using the formula 4 * pi * Area / (Perimeter^2), where Area is estimated as pi * radius^2, 
    and Perimeter is calculated as 2 * pi * radius. This method uses either Pick's measured area and 
    perimeter or estimates them based on bounding box coordinates if not already computed.
    
    Args:
      None: The method operates directly on the instance's attributes (`self.use_picks`, 
      `self.perimeter`, `self.bbox`).
      
    Returns:
      float: The calculated roundness value of the plaque.
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
