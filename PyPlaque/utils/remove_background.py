
import cv2
import numpy as np
from skimage import io, restoration
from skimage.morphology import disk, opening



def remove_background(img: np.ndarray, radius: float) -> tuple[np.ndarray,
np.ndarray]:
  """
  **remove_background Function**
  This function removes the background from an image by performing a morphological opening 
  operation. It converts the input `img` to uint16 format and then applies a morphological opening 
  with a disk-shaped structuring element of specified radius to suppress the background noise. 
  The resulting background is subtracted from the original image to obtain a foreground mask that 
  represents the main objects in the image.
  
  Args:
    img (np.ndarray, required): A 2D numpy array representing the grayscale or colored image from 
                            which the background should be removed.
    radius (float, required): The radius of the disk-shaped structuring element used for 
                            morphological opening, controlling the size of the neighborhood over 
                            which the operation is applied.
  
  Returns:
    tuple[np.ndarray, np.ndarray]: A tuple containing two elements:
        - background (np.ndarray): A 2D numpy array representing the result of applying a 
        morphological opening to `img` with a disk-shaped structuring element of size determined 
        by `radius`.
        - img_without_background (np.ndarray): A 2D numpy array representing the original image 
        with the background removed, obtained by subtracting `background` from `img`.
      
  Raises:
    TypeError: If `img` is not a 2D numpy array or `radius` is not a float.
    ValueError: If `radius` is less than or equal to zero.
  """
  img = np.array(img).astype(np.uint16)

  selem = disk(radius)

  selem = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2*radius + 1, 2*radius + 1))

  # Perform morphological opening
  background =  cv2.morphologyEx(img, cv2.MORPH_OPEN, selem)

  return background, img-background