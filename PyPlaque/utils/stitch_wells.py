import numpy as np


def stitch_wells(wells: list, nrows: int, ncols: int) -> np.ndarray :
  """
  **stitch_wells Function**
  This function stitches a list of well images into a larger image array based on specified number 
  of rows and columns. Ittakes a list of well images (each represented as a 2D numpy array), 
  combines them into a single large image using the `combine_img_blocks` utility function, which 
  arranges the images in a grid defined by `nrows` and `ncols`. The combined image is returned as a 
  numpy array.
  
  Args:
    wells (list, required): A list of 2D numpy arrays, each representing an individual well image.
    nrows (int, required): The number of rows in the final stitched image grid.
    ncols (int, required): The number of columns in the final stitched image grid.

  Returns:
    np.ndarray: A 2D numpy array representing the combined and stitched image of all wells, with 
    each element being of type float32 if precision is crucial for further processing.
      
  Raises:
    ValueError: If `wells` does not contain enough images to fill the specified number of rows and 
    columns in the grid.
  """
  combined_img = combine_img_blocks(wells, nrows, ncols)
  return combined_img

def combine_img_blocks(img_array: list, nrows: int, ncols: int) -> np.ndarray:
  """
  **combine_img_blocks Function**
  This function combines a list of image blocks into a single array with specified number of 
  rows and columns. It takes a list of images (represented as arrays), where each block is expected 
  to be squeezed before concatenation. It concatenates the first `ncols` images horizontally, 
  then stacks these horizontal combinations vertically (`nrows` times) to produce a larger image 
  array. The combined image is returned as a numpy array of type float32 for precision in further 
  processing if needed.
  
  Args:
    img_array (list, required): A list of image arrays to be combined. Each element should be a 
                            2D array representing an image block. 
    nrows (int, required): The number of rows in the final combined image.
    ncols (int, required): The number of columns in the final combined image.
  
  Returns:
    np.ndarray: A numpy array representing the combined image, with each element being of type 
    float32 for precision in further numerical operations if required.
      
  Raises:
    IndexError: If `img_array` does not contain enough elements to form the specified number of 
    rows and columns.
  """
  combined_img = np.array([])
  for _ in range(nrows):
    temp = np.concatenate([np.squeeze(img_array[i])
    for i in range(ncols)],axis=1).astype(np.float32)
    img_array = img_array[ncols:]
    combined_img = np.vstack([combined_img,temp]).astype(np.float32) \
    if combined_img.size else temp
  return combined_img
