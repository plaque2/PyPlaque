import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.segmentation import clear_border

from PyPlaque.utils import picks_area


class PlateImage:
  """
  **PlateImage Class**

  The PlateImage class is designed to encapsulate a full multi-title plate image and 
  its corresponding binary mask. It provides methods to extract individual well images 
  from the plate based on specified criteria, visualize these wells annotated with their positions, 
  and more.

  Attributes:
    n_rows (int, required): The number of rows in the plate. This should be less than the number 
                          of columns.

    n_columns (int, required): The number of columns in the plate. This should be greater than the 
                            number of rows.

    plate_image (np.ndarray, required): A 2D or 3D numpy array representing the image of 
                                      individual wells on the plate.

    plate_mask (np.ndarray, required): A binary 2D numpy array that outlines the regions 
                                    corresponding to each well.

    use_picks (bool, optional): An indicator for whether to use pick area calculations during 
                              analysis. Defaults to False.

    inverted (bool, optional): A boolean flag indicating whether the plate image is inverted 
                            or not.

  """
  def __init__(self,
                  n_rows,
                  n_columns,
                  plate_image,
                  plate_mask,
                  use_picks = False,
                  inverted = False):
      #check data types
      if not isinstance(n_rows, int):
        raise TypeError('Expected n_rows argument to be int')
      if not isinstance(n_columns, int):
        raise TypeError('Expected n_columns argument to be int')
      if (not isinstance(plate_image, np.ndarray)) or (not (plate_image.ndim >=2
      and plate_image.ndim <= 3)):
        raise TypeError('Image atribute of the plate must be a 2D numpy array')
      if (not isinstance(plate_mask, np.ndarray)) or (not plate_mask.ndim == 2):
        raise TypeError('Mask atribute of the plate must be a 2D numpy array')
      if not isinstance(inverted, bool):
        raise TypeError('inverted atribute of the plate must be of type bool')

      self.n_rows = n_rows
      self.n_columns = n_columns
      self.plate_image = plate_image
      self.plate_mask = plate_mask
      self.use_picks = use_picks
      self.inverted = inverted

  def get_wells(self, min_area = 100):
    """
    **get_wells Method**
    
    This method identifies and returns individual wells from a plate image as binary numpy arrays. 
    Each well is represented by its masked image within the bounding box derived from regionprops 
    analysis after clearing border artifacts from the plate mask.
    
    Args:
      min_area (int, optional): The minimum area in pixels for a well to be considered. 
                                Default is 100.
        
    Returns:
      list: A list of numpy arrays, where each array represents a well cropped from the 
      plate image.
    
    Notes:
      Wells are identified based on their area threshold and are extracted using bounding boxes 
      derived from regionprops analysis after clearing border artifacts from the plate mask.
    """
    well_crops = []
    for _,well in enumerate(regionprops(label(clear_border(self.plate_mask)))):
      if self.use_picks:
        well_area = picks_area(well.image)
      else:
        well_area = well.area
      if well_area >= min_area:
        minr, minc, maxr, maxc = well.bbox
        masked_img = self.plate_image ** self.plate_mask
        well_crops.append(masked_img[minr:maxr, minc:maxc])
    return well_crops

  def get_well_positions(self, min_area = 100):
    """
    **get_well_positions Method**
    
    This method identifies and returns individual wells from a plate image as binary numpy arrays. 
    Each well is represented by its masked image, mask, cropped image, and bounding box coordinates 
    along with row (nrow) and column (ncol) numbers.
    
    Args:
      min_area (int, optional): The minimum area in pixels for a well to be considered. 
                                Default is 100.
        
    Returns:
      dict: A dictionary where each key corresponds to an individual well, 
      containing the following items:
          - 'masked_img' (numpy array): Binary mask of the well.
          - 'mask' (numpy array): Binary mask of the plate region occupied by the well.
          - 'img' (numpy array): Image cropped from the plate corresponding to the well.
          - 'maxr' (int): Maximum row index of the bounding box for the well.
          - 'minc' (int): Minimum column index of the bounding box for the well.
          - 'minr' (int): Minimum row index of the bounding box for the well.
          - 'maxc' (int): Maximum column index of the bounding box for the well.
          - 'nrow' (int): Row number of the well, starting from 0.
          - 'ncol' (int): Column number of the well, starting from 0.
    
    Notes:
      The method processes the plate mask to identify and extract individual wells 
      based on area threshold.Wells are identified using bounding boxes derived from regionprops 
      analysis after clearing border artifacts. The returned dictionary is ordered by column 
      unless the plate is inverted (in which case it orders by columns in reverse).
    """
    well_dict = {}
    well_crops = []
    lc_zip = []
    for idx,well in enumerate(regionprops(label(clear_border(self.plate_mask)))
    ):
      if self.use_picks:
        well_area = picks_area(well.image)
      else:
        well_area = well.area
      if well_area >= min_area:
        minr, minc, maxr, maxc = well.bbox
        masked_img = self.plate_image ** self.plate_mask
        well_crops.append(masked_img[minr:maxr, minc:maxc])
        lc_zip.append((maxr,minc))
        # minc, maxr make up the top right corner of the bounding box that
        # encloses the well
        # We order by minc and maxr together

        well_dict[idx] = {}
        well_dict[idx]['masked_img'] = masked_img[minr:maxr, minc:maxc]
        well_dict[idx]['mask'] = self.plate_mask[minr:maxr, minc:maxc]
        well_dict[idx]['img'] = self.plate_image[minr:maxr, minc:maxc]
        well_dict[idx]['maxr'] = maxr
        well_dict[idx]['minc'] = minc
        well_dict[idx]['minr'] = minr
        well_dict[idx]['maxc'] = maxc

    l = lc_zip
    if not self.inverted:
      r_no = 0
      c_no = 0
    else:
      r_no = 0
      c_no = self.n_columns

    while len(l)>0:
      x_sorted = sorted(l, key=lambda tup: tup[1]) 
      column = x_sorted[:self.n_rows]
      y_sorted = sorted(column, key=lambda tup: tup[0])

      if not self.inverted:
        for (maxr,minc) in y_sorted:
          temp  = [k for k,v in well_dict.items() if ((int(v['maxr'])
          == maxr) and (int(v['minc']) == minc))]
          well_dict[temp[0]]['nrow'] = r_no
          well_dict[temp[0]]['ncol'] = c_no
          r_no +=1

        c_no +=1
        r_no = 0
      else:
        for (maxr,minc) in y_sorted:
          temp  = [k for k,v in well_dict.items() if ((int(v['maxr'])
          == maxr) and (int(v['minc']) == minc))]
          well_dict[temp[0]]['nrow'] = r_no
          well_dict[temp[0]]['ncol'] = c_no
          r_no +=1

        c_no -=1
        r_no = 0

      l = x_sorted[self.n_rows:]


    return well_dict

  def plot_well_positions(self,save_path = None):
    """
    **plot_well_positions Method**

    Plots boxes around individual wells of the plate using the mask. 
    Wells are annotated with their row and column positions.
    
    This method visualizes the well locations on a plate by drawing white rectangles around each 
    well inferred from the plate mask. The rows and columns are numbered starting from 0, and 
    annotations indicate both the column and row numbers for each well.

    Args:
      save_path (str, optional): File path where the plot image will be saved. If None (default), 
      the figure is shown but not saved.

    Returns:
      None
    
    Example:
      To visualize and save the well positions on a plate with a specific mask, use:
      
      >>> instance_of_plate.plot_well_positions(save_path='path/to/save/figure.png')
    """
    _, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(self.plate_mask, cmap='gray')

    well_dict = self.get_well_positions()

    PAD = 50
    for _,v in well_dict.items():
      rect = mpatches.Rectangle((v['minc']-PAD,v['minr']-PAD), (v['maxc']+PAD) -
      (v['minc']-PAD),(v['maxr']+PAD) - (v['minr']-PAD),fill=False,
      edgecolor='white', linewidth=2)
      ax.add_patch(rect)

      ax.annotate(str(v['nrow'])+','+str(v['ncol']), xy =(v['minc'],v['maxr']),
      color='white')
    ax.set_axis_off()
    plt.title('Annotated Wells')
    plt.tight_layout()
    if save_path:
      plt.savefig(save_path,bbox_inches='tight', dpi=300)
    plt.show()
    return
