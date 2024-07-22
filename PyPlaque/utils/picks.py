import numpy as np
from scipy import ndimage as ndi

STREL_4 = np.array([[0, 1, 0],
                    [1, 1, 1],
                    [0, 1, 0]], dtype=np.uint8)
STREL_8 = np.ones((3, 3), dtype=np.uint8)

def picks_area(image, neighbourhood=4):
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

    perimeter_image = ndi.convolve(border_image, np.array([[10, 2, 10],
                                                           [2, 1, 2],
                                                           [10, 2, 10]]),
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

    perimeter_image = ndi.convolve(border_image, np.array([[10, 2, 10],
                                                           [2, 1, 2],
                                                           [10, 2, 10]]),
                                   mode='constant', cval=0)
    perimeter_histogram = np.histogram(perimeter_image.ravel(), bins=50)
    total_perimeter = np.dot(perimeter_histogram[0], perimeter_weights)
    return total_perimeter
