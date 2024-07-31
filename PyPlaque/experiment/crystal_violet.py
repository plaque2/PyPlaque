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

class CrystalViolet:
  """
	**Class CrystalViolet** 
  This class is designed to contain metadata of multiple instances of a multititre plate of 
  Crystal Violet plaques.
    
  Attributes:
    plate_folder (str, required): The main directory containing subdirectories of the plates.

    plate_mask_folder (str, required): The main directory containing subdirectories of the 
                                      plate masks.

    params (dict, optional): A dictionary of parameters for crystal violet plaques, thresholding, 
                            etc. Default is an empty dictionary with default values set.
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
    **get_params Method** 
    Returns the parameters currently saved in the CrystalViolet class.
    
    Args:
      self (required): The instance of the class containing the data.
    
    Returns:
      dict: A dictionary containing the current parameters set for the experiment.
    """
    return self.params

  def get_individual_plates(self, whole_plate=False,folder_pattern=None):
    """
    **get_individual_wells Method** 
    This method retrieves the paths of directories containing images and masks for individual 
    plates. If `whole_plate` is False, it filters the directories based on a given pattern or 
    lists all directories if no pattern is provided.
    
    Args:
      whole_plate (bool, optional): A flag to determine whether to consider that folders 
                                    have whole plate images or not (wells images of a plate 
                                    instead). Default is False.
      folder_pattern (str, optional): A regular expression pattern used to filter directory names.
    
    Returns:
      tuple of lists: The first list contains the paths to directories with images of individual 
      plates, and the second list contains the paths to directories with masks for these 
      plates.
    
    Raises:
      ValueError: If `plate_folder` or `plate_mask_folder` is not a valid directory.
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
    **get_number_of_plates Method** 
    This method returns the number of individual plates detected. It checks both the instance 
    variable `plate_indiv_dir` and `full_plate_dict['img']` for the presence of plate directories or 
    images, respectively. If no plates are found, it raises a ValueError indicating that the paths
    should be checked again.
    
    Args:

    Returns:
        int: The number of individual plates detected in the instance's directory structure.
    
    Raises:
       ValueError: If no plates are found in the directory or file structures.
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
    **read_from_path Method**
    Loads an image into PIL format.

    Usage:

    ```
    image = pyplaque.ExperimentCrystalViolet.read_from_path(image_path)
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
    """
    **load_well_images_and_masks_for_plate Method**
    This method loads images and masks for a specified plate. It supports loading from both image 
    and mask folders or generating masks at runtime using specific parameters.
    
    Args:
      self: The instance of the class containing the method.
      plate_id (int, optional): The index of the plate to load images and masks for. Default is 0.
      additional_subfolders (str, optional): Additional subfolders within the image and mask 
                                            folders to consider. Defaults to None.
      file_pattern (str, optional): A regex pattern to filter files by their stem. If provided,
                                    only files matching this pattern will be loaded. Defaults to 
                                    None.
      read_mask (bool, optional): Whether to read masks from disk. If False, masks are generated 
                                  at runtime using image processing parameters. Defaults to True.
      all_grayscale (bool, optional): Whether to convert all images and masks to grayscale. 
                                      Defaults to False.
      ext (str, optional): The file extension pattern used to match files. Defaults to '*.png'.
    
    Returns:
      dict: A dictionary containing the loaded images and masks for each well in the specified plate.
    """
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
    """
    **load_plate_images_and_masks Method**
    Loads images and masks for plates from specified directories. This method reads image and mask 
    files from the `plate_folder` and `plate_mask_folder`, applying optional additional subfolders 
    and file patterns to narrow down the search. It supports grayscale conversion if requested, and 
    organizes the loaded data into a dictionary for each plate.

    Args:
      self (object): The instance of the class where this method is called.
      additional_subfolders (str, optional): Additional subdirectories within the main folders to 
                                            search for images and masks. Defaults to None.
      file_pattern (str, optional): A regex pattern to filter filenames. If provided, only files 
                                    matching the pattern will be loaded. Defaults to None.
      all_grayscale (bool, optional): Flag indicating whether all images should be converted to 
                                      grayscale. Defaults to True.
      ext (str, optional): The file extension to search for when loading images and masks. 
                            Default is "*.png".

    Returns:
      dict: A dictionary containing the loaded images and masks for each plate, indexed by 
      `plate_id`.

    Raises:
      ValueError: If either `plate_folder` or `plate_mask_folder` is not a valid directory.
    """
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
    """
    **extract_masked_plates Method**
    Extracts masked plate images from the full plate dictionary. This function iterates through each 
    plate in the `full_plate_dict`, extracts the plate images, and applies a mask to create masked 
    images for each plate.

    Args:

    Returns:
      dict: The updated `full_plate_dict` containing the masked images for each well in all 
      plates.
    """
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
    """
    **extract_masked_wells Method**
    Extracts masked well images from the specified plate.

    Args:
      plate_id (int, required): The index of the plate for which to extract masked wells.
      row_pattern (re.Pattern, optional): A regular expression pattern to match well rows. 
                                          Defaults to None.
      col_pattern (re.Pattern, optional): A regular expression pattern to match well columns. 
                                          Defaults to None.

    Returns:
      dict: The updated dictionary containing the masked images for each well.

    Raises:
      KeyError: If the specified plate ID does not exist in the `plate_indiv_dir` dictionary.
      ValueError: If both `row_pattern` and `col_pattern` are provided, but they do not match any 
      well indices.
    """
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
      

  