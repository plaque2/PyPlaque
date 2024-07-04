import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label, regionprops
from skimage.segmentation import clear_border


class PlateImage:
  """
  **PlateImage Class** is aimed to contain a full multititre plate image and
  it's respective binary mask.

  _Arguments_:

  n_rows - (int, required) number of rows in the plate (usually lower than
  the number of rows).

  n_columns - (int, required) number of columns in the plate (usually higher
  than the number of rows).

  plate_image - (np.array, required) an image of individual wells of the
  plate.

  plate_mask - (np.array, required) a binary mask outlining individual wells of
  the plate.

  inverted - (bool, required) an indicator of whether the plate.

  It is advisable to have both dimensions of plate masks and images be 2 dim
  """
  def __init__(self,
                n_rows,
                n_columns,
                plate_image,
                plate_mask,
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
    self.inverted = inverted

  def get_wells(self, min_area = 100):
    """
    **get_wells method** returns a list of individual wells of the plate
    stored as binary numpy arrays.
    """
    well_crops = []
    for _,well in enumerate(regionprops(label(clear_border(self.plate_mask)))):
      if well.area >= min_area:
        minr, minc, maxr, maxc = well.bbox
        masked_img = self.plate_image ** self.plate_mask
        well_crops.append(masked_img[minr:maxr, minc:maxc])
    return well_crops

  def get_well_positions(self, min_area = 100):
    """
    **get_well_positions method** returns a list of individual wells of the
    plate stored as binary numpy arrays along with a number with rows numbered
    starting from 1 and columns numbered starting from 1.
    """
    well_dict = {}
    well_crops = []
    lc_zip = []
    for idx,well in enumerate(regionprops(label(clear_border(self.plate_mask)))
    ):
      if well.area >= min_area:
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
      r_no = 1
      c_no = 1
    else:
      r_no = 1
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
        r_no = 1
      else:
        for (maxr,minc) in y_sorted:
          temp  = [k for k,v in well_dict.items() if ((int(v['maxr'])
          == maxr) and (int(v['minc']) == minc))]
          well_dict[temp[0]]['nrow'] = r_no
          well_dict[temp[0]]['ncol'] = c_no
          r_no +=1

        c_no -=1
        r_no = 1

      l = x_sorted[self.n_rows:]


    return well_dict

  def plot_well_positions(self,save=True, folder_path = '../data/results'):
    """
    **plot_well_positions method** plot boxes around individual wells of
    the plate (inferred from plate mask), with rows numbered starting from 1
      and columns numbered starting from 1.
    """
    _, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(self.plate_mask)

    well_dict = self.get_well_positions()

    for _,v in well_dict.items():
      rect = mpatches.Rectangle((v['minc']-50,v['minr']-50), (v['maxc']+50) -
      (v['minc']-50),(v['maxr']+50) - (v['minr']-50),fill=False,
      edgecolor='white', linewidth=2)
      ax.add_patch(rect)

      ax.annotate(str(v['nrow'])+','+str(v['ncol']), xy =(v['minc'],v['maxr']),
      color='white')
    ax.set_axis_off()
    plt.title('Annotated Wells')
    plt.tight_layout()
    if save:
      plt.savefig(os.path.join(folder_path,'output.svg'),
      bbox_inches='tight', dpi=300)
    plt.show()
