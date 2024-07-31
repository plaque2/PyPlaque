import io
import functools
import numpy as np
import os
from pathlib import Path
import re
import tifffile as TIFF
from tqdm.auto import tqdm
import warnings

from PyPlaque.utils import get_plaque_mask, remove_artifacts, remove_background

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


class FluorescenceMicroscopy:
  """
	**FluorescenceMicroscopy Class** 
  It is aimed to contain metadata of multiple instances of a multititre plate of Fluorescence 
  plaques.
    
  Attributes:
    plate_folder (str, required): The main directory containing subdirectories of the plates.
    
    plate_mask_folder (str, required): The main directory containing subdirectories of the 
                                    plate masks.
    
    params (dict, optional): A dictionary of parameters for nuclei and virus channels to be used 
                            for generating masks and readouts. Default is an empty dictionary.

  Raises:
    TypeError: If the provided arguments are not of the expected type.
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
      if not isinstance(params.values()[0], dict):
        raise TypeError("Expected first nested object of params argument to be dict")
      if not isinstance(params.values()[1], dict):
        raise TypeError("Expected second nested object of params argument to be dict")

    self.plate_folder = plate_folder
    self.plate_mask_folder = plate_mask_folder
    if not params:
      params = {
        'nuclei': {
                'selected_channel': 'w1',
                'raw_artifactThreshold': 0.5,
                'selected_thresholding_method': 'manualThresholding',
                'raw_manualThreshold': 0.008,
                'min_cell_area': 80,
                'max_cell_area': 90,
                'illumination_correction_flag': False,
                'correction_ball_radius': 120,
                'use_picks': False,
                'image_bits': 16
        },
        'virus':  {'selected_channel': 'w2',
                'raw_virusThreshold': 0.032,
                'min_plaque_area': 2000,
                'plaque_connectivity': 6,
                'min_cell_area': 80,
                'max_cell_area': 90,
                'fine_plaque_detection_flag': True,
                'plaque_gaussian_filter_size': 200,
                'plaque_gaussian_filter_sigma': 100,
                'peak_region_size': 50,
                'correction_ball_radius': 120,
                'use_picks': False,
                'image_bits': 16
        }
      }
    params['nuclei']['manual_threshold'] = params['nuclei']['raw_manualThreshold'] \
                                                            *(2**params['nuclei']['image_bits']-1)
    params['nuclei']['artifact_threshold'] = params['nuclei']['raw_artifactThreshold'] \
                                                            *(2**params['nuclei']['image_bits']-1)
    params['virus']['virus_threshold'] = params['virus']['raw_virusThreshold'] \
                                                            *(2**params['virus']['image_bits']-1)
    self.params = params
    self.plate_indiv_dir = []
    self.plate_mask_indiv_dir = []
    self.plate_dict_w1 = {}
    self.plate_dict_w2 = {}

  def get_params(self):
    """
    **get_params Method** 
    Returns the parameters currently saved in the FluorescenceMicroscopy class.
    
    Args:
      self (required): The instance of the class containing the data.
    
    Returns:
      dict: A dictionary containing the current parameters set for the experiment.
    """
    return self.params

  def get_individual_plates(self, folder_pattern=None):
    """
    **get_individual_plates Method** 
    Retrieves the paths of directories containing images and masks for individual plates.
    
    Args:
      self (required): The instance of the class containing the data.
      folder_pattern (str, optional): A regex pattern to filter directory names by their stem.
  
    Returns:
      tuple: A tuple containing two lists - one with paths to image directories and another with 
      paths to mask directories.
  
    Raises:
      ValueError: If the provided plate or plate_mask folder is not a valid directory.
    """
    if not os.path.isdir(self.plate_folder):
      raise ValueError("plate_folder argument is not a directory. \
      Please provide a valid directory.")
    if not os.path.isdir(self.plate_mask_folder):
      raise ValueError("plate_mask_folder argument is not a directory. \
      Please provide a valid directory.")

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
    **get_number_of_plates Method** 
    Returns the number of individual plates detected in the experiment.
    
    Args:
      self (required): The instance of the class containing the data.
    
    Returns:
      int: The total number of plates present in the plate directory.
    """
    return len(self.plate_indiv_dir)

  def load_wells_for_plate_virus(self, 
                                plate_id=0, 
                                additional_subfolders=None, 
                                file_pattern=None, 
                                ext = '*.tif'):
    """
    **load_wells_for_plate_virus Method**
    Loads the images and masks for the virus channel from specified wells in a fluorescence plaque 
    experiment.
    
    Args:
      self (required): The instance of the class containing the data.
      plate_id (int, optional): The index of the plate to load. Default is 0.
      additional_subfolders (str, optional): Additional subfolder path within the plate directory.
      file_pattern (str, optional): A regex pattern to filter image files by their stem.
      ext (str, optional): The file extension to match for images. Default is '*.tif'.
  
    Returns:
      self: The instance of the class with loaded data stored in plate_dict_w2.
    
    Raises:
      FileNotFoundError: If the specified image path does not exist.
    """
    d = self.plate_indiv_dir[plate_id]

    self.plate_dict_w2[d] = {}
    self.plate_dict_w2[d]['img'] = {}
    self.plate_dict_w2[d]['mask'] = {}
    self.plate_dict_w2[d]['image_name'] = {}

    if additional_subfolders:
      image_path = Path(self.plate_folder) / (d) / (additional_subfolders)
    else:
      image_path = Path(self.plate_folder) / (d)

    if file_pattern:
      image_files_w2 = [f for f in tqdm(image_path.glob(ext)) 
                                                  if len(re.findall(file_pattern,f.stem))>=1]
    else:
      image_files_w2 = [f for f in tqdm(image_path.glob(ext))]
    image_files_w2 = sorted(image_files_w2)

    img_list_w2 = [TIFF.imread(f) for f in tqdm(image_files_w2)]
    mask_list_w2 = [get_plaque_mask(img,self.params['virus'])[0] for img in tqdm(img_list_w2)]

    self.plate_dict_w2[d]['img'] = img_list_w2
    self.plate_dict_w2[d]['image_name'] = image_files_w2
    self.plate_dict_w2[d]['mask'] = mask_list_w2

    return self.plate_dict_w2

  def load_wells_for_plate_nuclei(self, 
                                  plate_id=0, 
                                  additional_subfolders=None, 
                                  file_pattern=None,
                                  ext='*.tif'):
    """
    **load_wells_for_plate_nuclei Method**
    Loads the images and masks for the nuclei channel from specified wells in a fluorescence 
    plaque experiment.
    
    Args:
      self (required): The instance of the class containing the data.
      plate_id (int, optional): The index of the plate to load. Default is 0.
      additional_subfolders (str, optional): Additional subfolder path within the plate directory.
      file_pattern (str, optional): A regex pattern to filter image files by their stem.
      ext (str, optional): The file extension to match for images. Default is '*.tif'.
  
    Returns:
      self: The instance of the class with loaded data stored in plate_dict_w1.
    
    Raises:
      FileNotFoundError: If the specified image path does not exist.
    """
    d = self.plate_indiv_dir[plate_id]

    self.plate_dict_w1[d] = {}
    self.plate_dict_w1[d]['img'] = {}
    self.plate_dict_w1[d]['mask'] = {}
    self.plate_dict_w1[d]['image_name'] = {}

    if additional_subfolders:
      image_path = Path(self.plate_folder) / (d) / (additional_subfolders)
    else:
      image_path = Path(self.plate_folder) / (d)

    if file_pattern:
      image_files_w1 = [f for f in tqdm(image_path.glob(ext)) 
                                                      if len(re.findall(file_pattern,f.stem))>=1]
    else:
      image_files_w1 = [f for f in tqdm(image_path.glob(ext))]
    image_files_w1 = sorted(image_files_w1)

    img_list_w1 = [TIFF.imread(f) for f in tqdm(image_files_w1)]    

    artifact_removed_img_list_w1 = map(functools.partial(remove_artifacts,artifact_threshold=
                                    self.params['nuclei']['artifact_threshold']), tqdm(img_list_w1))
    bg_removed_img_list_w1 = map(functools.partial(remove_background,
                            radius=self.params['nuclei']['correction_ball_radius']), 
                            tqdm(artifact_removed_img_list_w1))   
    bg_removed_img_list_w1 = [b[1] for b in tqdm(bg_removed_img_list_w1)]

    def create_binary_img(bg_removed_img,thresh):
        return np.where(bg_removed_img > thresh,1,0)

    binary_img_list_w1 = map(functools.partial(create_binary_img, 
                                              thresh= self.params['nuclei']['manual_threshold']), 
                                              bg_removed_img_list_w1)

    self.plate_dict_w1[d]['img'] = img_list_w1
    self.plate_dict_w1[d]['image_name'] = image_files_w1
    self.plate_dict_w1[d]['mask'] = list(binary_img_list_w1)

    return self.plate_dict_w1

  def read_from_path(self,
						path,
						grayscale=False,
						color_mode="rgb",
						target_size=None,
						interpolation="nearest",
						keep_aspect_ratio=False,
					):
    """
    **read_from_path Method**
    Loads an image into PIL format.

    Usage:

    ```
    image = pyplaque.FluorescenceMicroscopy.read_from_path(image_path)
    ```

    Args:
      path (str or Path or io.BytesIO, required): The path to the image file, a `Path` object, or 
                                                  an in-memory binary stream.
      grayscale (bool, optional): Deprecated use `color_mode="grayscale"`. Defaults to False.
      color_mode (str, optional): One of `"grayscale"`, `"rgb"`, `"rgba"`. Default: `"rgb"`. 
                                  The desired image format.
      target_size (tuple or list, optional): Either `None` (default to original size) or a tuple of 
                                            ints `(img_height, img_width)`.
      interpolation (str, optional): Interpolation method used to resample the image if the target 
                                    size is different from that of the loaded image. Supported 
                                    methods are `"nearest"`, `"bilinear"`, `"bicubic"`. If PIL 
                                    version 1.1.3 or newer is installed, `"lanczos"` is also 
                                    supported. If PIL version 3.4.0 or newer is installed, `"box"` 
                                    and `"hamming"` are also supported. By default, `"nearest"` 
                                    is used.
      keep_aspect_ratio (bool, optional): Boolean, whether to resize images to a target size without 
                                          aspect ratio distortion. The image is cropped in the 
                                          center with target aspect ratio before resizing. 
                                          Defaults to False.


    Returns:
      PIL.Image.Image: A PIL Image instance.

    Raises:
      ImportError: if PIL is not available.
      ValueError: if interpolation method is not supported.
      TypeError: If the provided `path` argument is not of a supported type.
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

    print(type(path))
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
