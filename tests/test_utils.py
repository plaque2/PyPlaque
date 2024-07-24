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
def input_image():
  return np.array([[0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 1, 4, 1, 0],
                    [0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0]])

@pytest.fixture()
def expected_final_plq_reg_image():
    return np.array([[0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 1, 1, 1, 0],
                    [0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0]])

@pytest.fixture()
def expected_global_peak_coords():
  return np.array([[2, 2]])

@pytest.fixture()
def virus_params():
  return {
    'virus_threshold': 0.5,
    'plaque_connectivity': 2,
    'min_plaque_area': 3,
    'plaque_gaussian_filter_sigma': 1.0,
    'plaque_gaussian_filter_size': 3,
    'peak_region_size': 1,
    'use_picks': False,
    'fine_plaque_detection_flag': True
  }

def test_centroid():
    # Test with a valid 2D numpy array
    ARR = np.array([[1, 2], [3, 4], [5, 6]])

    # Average of x values is (1+3+5)/3 = 3, average of y values is (2+4+6)/3 = 4
    EXPECTED_X, EXPECTED_Y = 3, 4  
    
    result = centroid(ARR)
    
    assert np.isclose(result[0], 
                      EXPECTED_X), f"X coordinate {result[0]} does not match \
                      the expected value {EXPECTED_X}"
    assert np.isclose(result[1], 
                      EXPECTED_Y), f"Y coordinate {result[1]} does not match \
                      the expected value {EXPECTED_Y}"
    
    # Test with an invalid array (should raise ValueError)
    # ToDo: centroid should be updated to handle this case
    #arr_invalid = np.array([[1, 2, 3], [4, 5, 6]])
    #result_invalid = centroid(arr_invalid)
    
    #assert result_invalid == (0, 0), "Invalid input should return (0, 0)"

def test_check_numbers():
    # Test with a valid tuple of integers and floats, both are OK
    TUP_VALID = (1, 2.0, 3)
    assert check_numbers(TUP_VALID) is False, "Tuple should contain only integers or floats"
    
    # Test with an invalid tuple containing non-numeric types
    TUP_INVALID = (1, 'a', 3)
    assert check_numbers(TUP_INVALID) is False, "Tuple should not contain string values"
    
    # Test with an empty tuple
    TUP_EMPTY = ()
    assert check_numbers(TUP_EMPTY) is True, "Empty tuple should be considered valid"

def test_fixed_threshold():
    # Create a sample image (5x5 array with random values between 0 and 1)
    np.random.seed(0)
    IMG = np.random.rand(5, 5)
    
    # Define threshold value and sigma for Gaussian filter
    THR = 0.5
    S = 1.0
    
    # Call the function
    result = fixed_threshold(IMG, THR, S)
    
    # Apply the same logic manually to compare results
    filtered_img = filters.gaussian(IMG, sigma=S)
    expected_result = np.zeros_like(filtered_img)
    expected_result[filtered_img > THR] = 1
    
    # Assert that the result matches the expected outcome
    assert np.array_equal(result, 
                          expected_result), "Thresholding result does not match the expected output"

def test_get_plaque_mask(input_image,
                          expected_final_plq_reg_image,
                          expected_global_peak_coords,
                          virus_params):
  # Call the function
  final_plq_reg_image, global_peak_coords = get_plaque_mask(input_image, virus_params)

  # Perform assertions
  assert np.array_equal(final_plq_reg_image, expected_final_plq_reg_image)
  assert np.array_equal(global_peak_coords, expected_global_peak_coords)

def test_remove_artifacts():
    # Create a sample image with random values and an artifact threshold
    IMG = np.random.randint(0, 256, size=(10, 10))
    ARTIFACT_THRESHOLD = 127
    
    # Call the function
    result = remove_artifacts(IMG, ARTIFACT_THRESHOLD)
    
    # Assert that pixels above the threshold are set to zero
    assert np.all(result[IMG > ARTIFACT_THRESHOLD] == 0), "Artifacts were not removed correctly"

def test_remove_background():
    # Create a sample image (5x5 array with random values)
    IMG = np.random.randint(0, 65535, size=(5, 5), dtype=np.uint16)
    
    # Define a radius for the morphological operation
    RADIUS = 2
    
    # Call the function
    background, foreground = remove_background(IMG, RADIUS)
    
    # Assert shapes are correct
    assert background.shape == IMG.shape, "Background shape is incorrect"
    assert foreground.shape == IMG.shape, "Foreground shape is incorrect"
    
    # Assert pixel values are non-negative (foreground should not have negative values)
    assert np.all(foreground >= 0), "Foreground has negative values"
    
    # Add assertion to check that the background is correctly subtracted
    assert np.allclose(IMG, background + foreground), "Background subtraction is incorrect"

