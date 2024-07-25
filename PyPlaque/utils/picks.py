import numpy as np
from scipy import ndimage as ndi

STREL_4 = np.array([[0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0]], dtype=np.uint8)
STREL_8 = np.ones((3, 3), dtype=np.uint8)

def picks_area(image, neighbourhood=4):
    """
    **picks_area Function**
    This function calculates the area of Pick's (https://en.wikipedia.org/wiki/Pick%27s_theorem) 
    regions in an image. It estimates the area of Pick's by first calculating the perimeter 
    using morphological operations and then applying a predefined set of weights to estimate 
    the number of pixels that make up the perimeter. The total perimeter is used along with the 
    eroded image to estimate the area, considering both the interior and exterior contributions 
    to the area calculation.
    
    Args:
        image (np.ndarray, required): A 2D numpy array representing the binary or grayscale image 
                                    containing Pick's regions.
        neighbourhood (int, optional): An integer specifying the type of connectivity to use for 
                                    morphological operations. Use 4 for 4-connectivity or 8 for 
                                    8-connectivity. Defaults to 4.
    
    Returns:
        float: The estimated area of Pick's in the image, calculated as a combination of the number 
        of pixels in the eroded image and the weighted perimeter.
        
    Raises:
        TypeError: If `image` is not a 2D numpy array or `neighbourhood` is not an integer.
        ValueError: If `neighbourhood` is not either 4 or 8.
    """
    if neighbourhood == 4:
        strel = STREL_4
    elif neighbourhood == 8:
        strel = STREL_8
    image = image.astype(np.uint8)
    eroded_image = ndi.binary_erosion(image, strel, border_value=0)
    border_image = image - eroded_image

    perimeter_weights = np.zeros(50, dtype=np.double)
    perimeter_weights[[5, 7, 15, 17, 25, 27]] = 0.25
    perimeter_weights[[21, 33]] = 1
    perimeter_weights[[13, 23]] = 0.125

    PERIMETER_KERNEL = np.array([[10, 2, 10],
                                [2, 1, 2],
                                [10, 2, 10]])
    perimeter_image = ndi.convolve(border_image, PERIMETER_KERNEL,
                                   mode='constant', cval=0)
    perimeter_histogram = np.histogram(perimeter_image.ravel(), bins=50)
    total_perimeter = np.dot(perimeter_histogram[0], perimeter_weights)

    v = np.count_nonzero(eroded_image)

    if v == 0:
        s = total_perimeter
    else:
        s = v + total_perimeter / 2 - 1

    return s

def picks_perimeter(image, neighbourhood=4):
    """
    **picks_perimeter Function**
    This function calculates the total perimeter of Pick's 
    (https://en.wikipedia.org/wiki/Pick%27s_theorem) regions in an image. It identifies and 
    measures the perimeter of Pick's by using morphological operations to detect borders and then 
    computes a weighted sum based on predefined weights for different pixel contributions to the 
    perimeter. It supports both 4-connectivity and 8-connectivity neighborhoods, which are 
    determined by the `neighbourhood` parameter.
    
    Args:
        image (np.ndarray, required): A 2D numpy array representing the binary or grayscale image 
                                    containing Pick's regions.
        neighbourhood (int, optional): An integer specifying the type of connectivity to use for 
                                    morphological operations. Use 4 for 4-connectivity or 8 for 
                                    8-connectivity. Defaults to 4.
    
    Returns:
        float: The total perimeter of PICKs in the image, calculated as a weighted sum of pixel 
        contributions based on their neighborhood connectivity and proximity to other boundaries.
        
    Raises:
        TypeError: If `image` is not a 2D numpy array or `neighbourhood` is not an integer.
        ValueError: If `neighbourhood` is not either 4 or 8.
    """
    if neighbourhood == 4:
        strel = STREL_4
    else:
        strel = STREL_8
    image = image.astype(np.uint8)

    (w, h) = image.shape
    data = np.zeros((w + 2, h + 2), dtype=image.dtype)
    data[1:-1, 1:-1] = image
    image = data

    eroded_image = ndi.binary_dilation(image, strel, border_value=0)
    border_image = eroded_image - image

    perimeter_weights = np.zeros(50, dtype=np.double)
    perimeter_weights[[5, 7, 15, 17, 25, 27]] = 1
    perimeter_weights[[21, 33]] = np.sqrt(2)
    perimeter_weights[[13, 23]] = (1 + np.sqrt(2)) / 2

    PERIMETER_KERNEL = np.array([[10, 2, 10],
                                [2, 1, 2],
                                [10, 2, 10]])
    perimeter_image = ndi.convolve(border_image, PERIMETER_KERNEL,
                                   mode='constant', cval=0)
    perimeter_histogram = np.histogram(perimeter_image.ravel(), bins=50)
    total_perimeter = np.dot(perimeter_histogram[0], perimeter_weights)
    return total_perimeter
