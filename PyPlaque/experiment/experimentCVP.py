import io
import os
import pathlib
import warnings

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
	"""

  def __init__(self, plate_folder, plate_mask_folder):
    #check data types
    if not isinstance(plate_folder, str):
      raise TypeError("Expected plate_folder argument to be str")
    if not isinstance(plate_mask_folder, str):
      raise TypeError("Expected plate_mask_folder argument to be str")

    self.plate_folder = plate_folder
    self.plate_mask_folder = plate_mask_folder

  def get_individual_plates(self):
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

    plate_indiv_dir = [file for file in os.listdir(self.plate_folder)
				 if os.path.isdir(os.path.join(self.plate_folder, file))]
    plate_masks_indiv_dir = [file for file in os.listdir(self.plate_mask_folder)
				 if os.path.isdir(os.path.join(self.plate_mask_folder, file))]

    self.plate_indiv_dir = plate_indiv_dir
    self.plate_masks_indiv_dir = plate_masks_indiv_dir

    return self.plate_indiv_dir, self.plate_masks_indiv_dir


  def get_number_of_plates(self):
    """
    **get_number_of_plates method** returns the number of individual plates
    detected.
    """

    return len(self.plate_indiv_dir)


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
    elif isinstance(path, (pathlib.Path, bytes, str)):
      if isinstance(path, pathlib.Path):
        path = str(path.resolve())
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
