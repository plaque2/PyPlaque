import io
import numpy as np
import os
from pathlib import Path
import re
from skimage.exposure import adjust_gamma
from tqdm.auto import tqdm
import warnings

from PyPlaque.specimen import PlaquesWell, PlaquesImageGray
try:
  from PIL import Image as pil_image
except ImportError:
  pil_image = None

if pil_image is not None:
  _PIL_INTERPOLATION_METHODS = {
	"nearest": pil_image.NEAREST,
	"bilinear": pil_image.BILINEAR,
	"bicubic": pil_image.BICUBIC,
	"hamming": pil_image.HAMMING,
	"box": pil_image.BOX,
	"lanczos": pil_image.LANCZOS,
	}

class ExperimentCrystalVioletPlaque:
  """
	**Class ExperimentCrystalVioletPlaque** is aimed to contain metadata of
	multiple instances of a full well of a multititre plate of Crystal Violet
	Plaque.

	_Arguments_:

	plate_folder - (str, required) main directory containing subdirectories of
	the plates.

	plate_mask_folder - (str, required) main directory containing subdirectories
	of the plate masks.

  params -(dict, optional) dictionary of parameters for crystal violet plaques,
  thresholding etc.
	"""

  def __init__(self, plate_folder, plate_mask_folder, params=None):
    #check data types
    if not isinstance(plate_folder, str):
      raise TypeError("Expected plate_folder argument to be str")
    if not isinstance(plate_mask_folder, str):
      raise TypeError("Expected plate_mask_folder argument to be str")
    if params:
      if not isinstance(params, dict):
        raise TypeError("Expected params argument to be dict")

    self.plate_folder = plate_folder
    self.plate_mask_folder = plate_mask_folder

    if not params:
      params = {
        'crystal_violet': {
                'gain': 1,
                'gamma': 1.32,
                'nrows': 2,
                'ncols': 3,
                'min_area': 100,
                'max_area': 200,
                'sigma': 0.4,
                'threshold': 0.25,
        }
      }

    self.params = params
    self.plate_indiv_dir = []
    self.plate_mask_indiv_dir = []
    self.well_dict = {}
    self.full_plate_dict = {}

  def get_params(self):
    """
    **get_params method** returns the parameters currently saved in the 
    ExperimentCrystalVioletPlaque class
    """
    return self.params

  def get_individual_plates(self, whole_plate=False,folder_pattern=None):
    """
    **get_individual_wells method** returns the path of the directory of images
    and masks of individual plates.
    """

    if not os.path.isdir(self.plate_folder):
      raise ValueError("plate_folder argument is not a directory. \
			Please provide a valid directory.")
    if not os.path.isdir(self.plate_mask_folder):
      raise ValueError("plate_mask_folder argument is not a directory. \
			Please provide a valid directory.")
    if not whole_plate:
      if folder_pattern:
        self.plate_indiv_dir = [file for file in os.listdir(self.plate_folder)
        if (os.path.isdir(os.path.join(self.plate_folder, file)) and 
                                                      (len(re.findall(folder_pattern,file))>=1))]
        self.plate_mask_indiv_dir = [file for file in os.listdir(self.plate_mask_folder)
        if (os.path.isdir(os.path.join(self.plate_mask_folder, file)) and 
                                                      (len(re.findall(folder_pattern,file))>=1))] 
      else:
        self.plate_indiv_dir = [file for file in os.listdir(self.plate_folder)
            if os.path.isdir(os.path.join(self.plate_folder, file))]
        self.plate_mask_indiv_dir = [file for file in os.listdir(self.plate_mask_folder)
            if os.path.isdir(os.path.join(self.plate_mask_folder, file))]
      
    return self.plate_indiv_dir, self.plate_mask_indiv_dir
  

  def get_number_of_plates(self):
    """
    **get_number_of_plates method** returns the number of individual plates
    detected.
    """
    if len(self.plate_indiv_dir) != 0:
      return len(self.plate_indiv_dir)
    elif len(self.full_plate_dict['img']) != 0:
      return len(self.full_plate_dict['img'])
    else:
      raise ValueError("No plates found. Please check paths or folder/file patterns again.")


  def read_from_path(self,
						path,
						grayscale=False,
						color_mode="rgb",
						target_size=None,
						interpolation="nearest",
						keep_aspect_ratio=False,
					):
    """
    Loads an image into PIL format.

    Usage:

    ```
    image = pyplaque.ExperimentCrystalVioletPlaque.read_from_path(image_path)
    ```

    Args:
      path: Path to image file.
      grayscale: DEPRECATED use `color_mode="grayscale"`.
      color_mode: One of `"grayscale"`, `"rgb"`, `"rgba"`. Default: `"rgb"`.
      The desired image format.
      target_size: Either `None` (default to original size) or tuple of
      ints `(img_height, img_width)`.
      interpolation: Interpolation method used to resample the image if
      the target size is different from that of the loaded image. Supported
      methods are `"nearest"`, `"bilinear"`, and `"bicubic"`. If PIL version
      1.1.3 or newer is installed, `"lanczos"` is also supported. If PIL
      version 3.4.0 or newer is installed, `"box"` and `"hamming"` are also
      supported. By default, `"nearest"` is used.
      keep_aspect_ratio: Boolean, whether to resize images to a target
      size without aspect ratio distortion. The image is cropped in
      the center with target aspect ratio before resizing.

    Returns:
      A PIL Image instance.

    Raises:
      ImportError: if PIL is not available.
      ValueError: if interpolation method is not supported.
    """
    if grayscale:
      warnings.warn(
      "grayscale is deprecated. Please use " 'color_mode = "grayscale"'
      )
      color_mode = "grayscale"

    if pil_image is None:
      raise ImportError(
      "Could not import PIL.Image. " "The use of `load_img` requires PIL."
      )

    if isinstance(path, io.BytesIO):
      img = pil_image.open(path)
    elif isinstance(path, (Path, bytes, str)):
      if isinstance(path, Path):
        path = str(path)
        img = pil_image.open(path)
      elif isinstance(path, str):
        img = pil_image.open(path)
      else:
        with open(path, "rb") as f:
          img = pil_image.open(io.BytesIO(f.read()))
    else:
      raise TypeError(
      f"path should be path-like or io.BytesIO, not {type(path)}"
      )

    if color_mode == "grayscale":
      # if image is not already an 8-bit, 16-bit or 32-bit grayscale image
      # convert it to an 8-bit grayscale image.
      if img.mode not in ("L", "I;16", "I"):
        img = img.convert("L")
    elif color_mode == "rgba":
      if img.mode != "RGBA":
        img = img.convert("RGBA")
    elif color_mode == "rgb":
      if img.mode != "RGB":
        img = img.convert("RGB")
    else:
      raise ValueError('color_mode must be "grayscale", "rgb", \
      or "rgba"')

    if target_size is not None:
      width_height_tuple = (target_size[1], target_size[0])
      if img.size != width_height_tuple:
        if interpolation not in _PIL_INTERPOLATION_METHODS:
          raise ValueError(
            f"Invalid interpolation method {interpolation} \
            specified. Supported methods are \
            {','.join(_PIL_INTERPOLATION_METHODS.keys())}"
          )

        resample = _PIL_INTERPOLATION_METHODS[interpolation]

        if keep_aspect_ratio:
          width, height = img.size
          target_width, target_height = width_height_tuple

          crop_height = (width * target_height) // target_width
          crop_width = (height * target_width) // target_height

          # Set back to input height / width
          # if crop_height / crop_width is not smaller.
          crop_height = min(height, crop_height)
          crop_width = min(width, crop_width)

          crop_box_hstart = (height - crop_height) // 2
          crop_box_wstart = (width - crop_width) // 2
          crop_box_wend = crop_box_wstart + crop_width
          crop_box_hend = crop_box_hstart + crop_height
          crop_box = [
            crop_box_wstart,
            crop_box_hstart,
            crop_box_wend,
            crop_box_hend,
          ]
          img = img.resize(width_height_tuple, resample, box=crop_box)
        else:
          img = img.resize(width_height_tuple, resample)
    return img

  def load_well_images_and_masks_for_plate(self, 
                                plate_id=0, 
                                additional_subfolders=None, 
                                file_pattern=None, 
                                read_mask = True,
                                all_grayscale = False,
                                ext = '*.png'):

    d = self.plate_indiv_dir[plate_id]

    self.well_dict[d] = {}
    self.well_dict[d]['img'] = {}
    self.well_dict[d]['mask'] = {}
    self.well_dict[d]['image_name'] = {}

    if additional_subfolders:
      image_path = Path(self.plate_folder) / (d) / (additional_subfolders)
      mask_path = Path(self.plate_mask_folder) / (d) / (additional_subfolders)
    else:
      image_path = Path(self.plate_folder) / (d)
      mask_path = Path(self.plate_mask_folder) / (d)

    if file_pattern:
      image_files = [f for f in tqdm(image_path.glob(ext)) 
                                                    if len(re.findall(file_pattern,f.stem))>=1]
    else:
      image_files = list(tqdm(image_path.glob(ext)))
    image_files = sorted(image_files)
    if all_grayscale:
      img_list = [np.asarray(self.read_from_path(f,color_mode="grayscale")) 
                                                    for f in tqdm(image_files)]
    else:
      img_list = [self.read_from_path(f) for f in tqdm(image_files)]

    if read_mask:
      if file_pattern:
        mask_files = [f for f in tqdm(mask_path.glob(ext)) 
                                                    if len(re.findall(file_pattern,f.stem))>=1]
      else:
        mask_files = list(tqdm(mask_path.glob(ext)))
      mask_files = sorted(mask_files)
      if all_grayscale:
        mask_list = [np.asarray(self.read_from_path(f,color_mode="grayscale")) 
                                                    for f in tqdm(mask_files)]
      else:
        mask_list = [self.read_from_path(f,color_mode="grayscale") for f in tqdm(mask_files)]
    else:
      # generate masks at runtime from images using params
      img_gadjusted_list = [adjust_gamma(img, 
                                gamma=self.params['crystal_violet']['gamma'],
                                gain=self.params['crystal_violet']['gain']) 
                            for img in tqdm(img_list)]

      mask_list = [PlaquesImageGray(self.plate_indiv_dir[plate_id]+"-"+
                                    str(i//self.params['crystal_violet']['ncols'])+","+
                                    str(i%self.params['crystal_violet']['ncols']),
                                img_gadjusted_list[i],
                                threshold=self.params['crystal_violet']['threshold'],
                                sigma=self.params['crystal_violet']['sigma']).plaques_mask
                        for i in tqdm(range(len(img_list)))]

    self.well_dict[d]['img'] = img_list
    self.well_dict[d]['image_name'] = image_files
    self.well_dict[d]['mask'] = mask_list

    return self.well_dict

  def load_plate_images_and_masks(self,
                                  additional_subfolders=None,
                                  file_pattern=None,
                                  all_grayscale=True,
                                  ext="*.png"):
    if not os.path.isdir(self.plate_folder):
      raise ValueError("plate_folder argument is not a directory. \
			Please provide a valid directory.")
    if not os.path.isdir(self.plate_mask_folder):
      raise ValueError("plate_mask_folder argument is not a directory. \
			Please provide a valid directory.")

    if additional_subfolders:
      image_path = Path(self.plate_folder) / (additional_subfolders)
      mask_path = Path(self.plate_mask_folder) / (additional_subfolders)
    else:
      image_path = Path(self.plate_folder)
      mask_path = Path(self.plate_mask_folder)

    if file_pattern:
      image_files = [f for f in tqdm(image_path.glob(ext)) 
                                                  if len(re.findall(file_pattern,f.stem))>=1]
      mask_files = [f for f in tqdm(mask_path.glob(ext)) 
                                                  if len(re.findall(file_pattern,f.stem))>=1]
    else:
      image_files = list(tqdm(image_path.glob(ext)))
      mask_files = list(tqdm(mask_path.glob(ext)))
    image_files = sorted(image_files)
    mask_files = sorted(mask_files)

    self.plate_indiv_dir = [f.stem for f in image_files] 
    self.plate_mask_indiv_dir = [f.stem for f in mask_files]

    for f in image_files:
      self.full_plate_dict[f.stem] = {}
      self.full_plate_dict[f.stem]['img'] = {}
      self.full_plate_dict[f.stem]['mask'] = {}
      self.full_plate_dict[f.stem]['image_name'] = {}

    if all_grayscale:
      img_list = [np.asarray(self.read_from_path(f,color_mode="grayscale")) 
                                                                      for f in tqdm(image_files)]
      mask_list = [np.asarray(self.read_from_path(f,color_mode="grayscale")) 
                                                                      for f in tqdm(mask_files)]
    else:
      img_list = [self.read_from_path(f) for f in tqdm(image_files)]
      mask_list = [self.read_from_path(f,color_mode="grayscale") for f in tqdm(mask_files)]

    for i,f in tqdm(enumerate(image_files)):
      self.full_plate_dict[f.stem]['img'] = img_list[i]
      self.full_plate_dict[f.stem]['image_name'] = image_files[i]
      self.full_plate_dict[f.stem]['mask'] = (255-mask_list[i])/255

    return self.full_plate_dict

  def extract_masked_plates(self):
    plaques_well_list = [PlaquesWell(row = 0,
                              column = 0,
                              well_image = self.full_plate_dict[d]['img'],
                              well_mask = self.full_plate_dict[d]['mask']) 
                              for d in tqdm(self.full_plate_dict.keys())]
    masked_img_list = [plq_well.get_masked_image() for plq_well in tqdm(plaques_well_list)]
    for i,d in tqdm(enumerate(self.full_plate_dict.keys())):
      self.full_plate_dict[d]['masked_img'] = masked_img_list[i]

    return self.full_plate_dict     

  def extract_masked_wells(self,plate_id,row_pattern=None,col_pattern=None):
    d= self.plate_indiv_dir[plate_id]
    if row_pattern and col_pattern:
      plaques_well_list = [PlaquesWell(row = re.findall(row_pattern, 
                                      str(self.well_dict[d]['image_name'][i]))[0],
                                  column = re.findall(col_pattern, 
                                      str(self.well_dict[d]['image_name'][i]))[0],
                                  well_image = self.well_dict[d]['img'][i],
                                  well_mask = self.well_dict[d]['mask'][i]) 
                                  for i in tqdm(range(len(self.well_dict[d]['img'])))]
      masked_img_list = [plq_well.get_masked_image() for plq_well in tqdm(plaques_well_list)]
      self.well_dict[d]['masked_img'] = masked_img_list
    else:
      plaques_well_list = [PlaquesWell(row = i//self.params['crystal_violet']['ncols'],
                              column = i%self.params['crystal_violet']['ncols'],
                              well_image = self.well_dict[d]['img'][i],
                              well_mask = self.well_dict[d]['mask'][i]) 
                              for i in tqdm(range(len(self.well_dict[d]['img'])))]
      masked_img_list = [plq_well.get_masked_image() for plq_well in tqdm(plaques_well_list)]
      self.well_dict[d]['masked_img'] = masked_img_list

    return self.well_dict      
      

  