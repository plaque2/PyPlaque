import numpy as np
from skimage import filters
import pytest

from PyPlaque.utils import remove_artifacts, remove_background
from PyPlaque.utils import centroid, check_numbers, fixed_threshold
from PyPlaque.utils import get_plaque_mask

@pytest.fixture()
def utils_remove_artifacts_input():
  return np.array([0, 0.25, 0, 0.9, 0]), 0.24

@pytest.fixture()
def utils_remove_artifacts_res():
  return np.array([0, 0, 0, 0, 0])

def test_utils_remove_artifacts(utils_remove_artifacts_input,
                                utils_remove_artifacts_res):
  assert (utils_remove_artifacts_res ==
  remove_artifacts(*utils_remove_artifacts_input)).all

@pytest.fixture()
def inputImage():
  return np.array([[0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 1, 4, 1, 0],
                    [0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0]])

@pytest.fixture()
def expected_finalPlqRegImage():
    return np.array([[0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 1, 1, 1, 0],
                    [0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0]])

@pytest.fixture()
def expected_globalPeakCoords():
  return np.array([[2, 2]])

@pytest.fixture()
def virus_params():
  return {
    'virus_threshold': 0.5,
    'plaque_connectivity': 2,
    'min_plaque_area': 3,
    'plaque_gaussian_filter_sigma': 1.0,
    'plaque_gaussian_filter_size': 3,
    'peak_region_size': 1
  }

def test_centroid():
    # Test with a valid 2D numpy array
    arr = np.array([[1, 2], [3, 4], [5, 6]])

    # Average of x values is (1+3+5)/3 = 3, average of y values is (2+4+6)/3 = 4
    expected_x, expected_y = 3, 4  
    
    result = centroid(arr)
    
    assert np.isclose(result[0], 
                      expected_x), f"X coordinate {result[0]} does not match the expected value {expected_x}"
    assert np.isclose(result[1], 
                      expected_y), f"Y coordinate {result[1]} does not match the expected value {expected_y}"
    
    # Test with an invalid array (should raise ValueError)
    # ToDo: centroid should be updated to handle this case
    #arr_invalid = np.array([[1, 2, 3], [4, 5, 6]])
    #result_invalid = centroid(arr_invalid)
    
    #assert result_invalid == (0, 0), "Invalid input should return (0, 0)"

def test_check_numbers():
    # Test with a valid tuple of integers and floats, both are OK
    tup_valid = (1, 2.0, 3)
    assert check_numbers(tup_valid) is False, "Tuple should contain only integers or floats"
    
    # Test with an invalid tuple containing non-numeric types
    tup_invalid = (1, 'a', 3)
    assert check_numbers(tup_invalid) is False, "Tuple should not contain string values"
    
    # Test with an empty tuple
    tup_empty = ()
    assert check_numbers(tup_empty) is True, "Empty tuple should be considered valid"

def test_fixed_threshold():
    # Create a sample image (5x5 array with random values between 0 and 1)
    np.random.seed(0)
    img = np.random.rand(5, 5)
    
    # Define threshold value and sigma for Gaussian filter
    thr = 0.5
    s = 1.0
    
    # Call the function
    result = fixed_threshold(img, thr, s)
    
    # Apply the same logic manually to compare results
    filtered_img = filters.gaussian(img, sigma=s)
    expected_result = np.zeros_like(filtered_img)
    expected_result[filtered_img > thr] = 1
    
    # Assert that the result matches the expected outcome
    assert np.array_equal(result, 
                          expected_result), "Thresholding result does not match the expected output"

def test_get_plaque_mask(inputImage,
                          expected_finalPlqRegImage,
                          expected_globalPeakCoords,
                          virus_params):
  # Call the function
  finalPlqRegImage, globalPeakCoords = get_plaque_mask(inputImage, virus_params)

  # Perform assertions
  assert np.array_equal(finalPlqRegImage, expected_finalPlqRegImage)
  assert np.array_equal(globalPeakCoords, expected_globalPeakCoords)

def test_remove_artifacts():
    # Create a sample image with random values and an artifact threshold
    img = np.random.randint(0, 256, size=(10, 10))
    artifact_threshold = 127
    
    # Call the function
    result = remove_artifacts(img, artifact_threshold)
    
    # Assert that pixels above the threshold are set to zero
    assert np.all(result[img > artifact_threshold] == 0), "Artifacts were not removed correctly"

def test_remove_background():
    # Create a sample image (5x5 array with random values)
    img = np.random.randint(0, 65535, size=(5, 5), dtype=np.uint16)
    
    # Define a radius for the morphological operation
    radius = 2
    
    # Call the function
    background, foreground = remove_background(img, radius)
    
    # Assert shapes are correct
    assert background.shape == img.shape, "Background shape is incorrect"
    assert foreground.shape == img.shape, "Foreground shape is incorrect"
    
    # Assert pixel values are non-negative (foreground should not have negative values)
    assert np.all(foreground >= 0), "Foreground has negative values"
    
    # Add assertion to check that the background is correctly subtracted
    assert np.allclose(img, background + foreground), "Background subtraction is incorrect"

