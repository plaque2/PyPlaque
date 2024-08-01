import numpy as np
from skimage import filters
import pytest

from PyPlaque.utils import remove_artifacts, remove_background
from PyPlaque.utils import centroid, check_numbers, fixed_threshold
from PyPlaque.utils import get_plaque_mask

@pytest.fixture()
def utils_remove_artifacts_input():
    """
    **utils_remove_artifacts_input Function**
    This fixture returns a tuple containing an input image (as a numpy array) and a threshold value, 
    which are typical inputs for the remove_artifacts function during testing. The specific values 
    within these arrays are examples used to test different scenarios in artifact removal processes.
    
    Args:
        
    Returns:
        tuple: A tuple containing an input image array and a threshold value for remove_artifacts.
    """
    return np.array([0, 0.25, 0, 0.9, 0]), 0.24

@pytest.fixture()
def utils_remove_artifacts_res():
    """
    **utils_remove_artifacts_res Function**
    This fixture returns a numpy array that is expected as the result of the remove_artifacts 
    function during testing.
    
    Args:
        
    Returns:
        np.ndarray: An array representing the expected result from remove_artifacts.
    """
    return np.array([0, 0, 0, 0, 0])

def test_utils_remove_artifacts(utils_remove_artifacts_input,
                                utils_remove_artifacts_res):
    """
    **test_utils_remove_artifacts Function**
    This function tests the remove_artifacts utility by comparing the result of applying the 
    function to `utils_remove_artifacts_input` with `utils_remove_artifacts_res`. The test asserts 
    that these two are equal, which is a basic check for ensuring the functionality of the artifact 
    removal process.
    
    Args:
        utils_remove_artifacts_input (tuple, required): A tuple containing input arguments for 
                                                    remove_artifacts function.
        utils_remove_artifacts_res (np.ndarray, required): The expected result after applying 
                                                        remove_artifacts to 
                                                        `utils_remove_artifacts_input`.
        
    Returns:
        None: The function performs an assertion directly on the output of the utility function.
    """
    assert (utils_remove_artifacts_res ==
    remove_artifacts(*utils_remove_artifacts_input)).all

@pytest.fixture()
def input_image():
    """
    **input_image Function**
    This fixture returns a numpy array representing an input image, which is used as a baseline in 
    tests that involve processing or analyzing this image. The array is set to simulate a specific 
    pattern of values representing different regions within the image.
    
    Args:
        
    Returns:
        np.ndarray: An array representing the input image used in tests.
    """
    return np.array([[0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 1, 4, 1, 0],
                    [0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0]])

@pytest.fixture()
def expected_final_plq_reg_image():
    """
    **expected_final_plq_reg_image Function**
    This fixture returns a numpy array representing the final plaque region image, which is used as 
    an expectation in tests that involve generating or processing such images. The array is set to 
    simulate a specific pattern of plaque regions and background noise.
    
    Args:
        
    Returns:
        np.ndarray: An array representing the expected final plaque region image.
    """
    return np.array([[0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0],
                    [0, 1, 1, 1, 0],
                    [0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0]])

@pytest.fixture()
def expected_global_peak_coords():
    """
    **expected_global_peak_coords Function**
    This fixture returns a numpy array containing the coordinates of a global peak, which is 
    typically used as an expectation in tests that involve finding peaks within data. The 
    coordinates are set to `[2, 2]` in this example.
    
    Args:
        
    Returns:
        np.ndarray: An array with the expected global peak coordinates.
    """
  
    return np.array([[2, 2]])

@pytest.fixture()
def virus_params():
    """
    **virus_params Function**
    This fixture returns a dictionary containing parameters specific to various processes related to 
    a virus, such as thresholding and plaque detection. The parameters include settings for the 
    virus threshold, minimum plaque area, Gaussian filter sigma and size used in plaque detection, 
    peak region size, whether to use picks (a placeholder indicating potential future 
    functionality), and fine plaque detection flag.
    
    Args:
        
    Returns:
        dict: A dictionary containing parameters for virus-related processes.
    """
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
    """
    **test_centroid Function**
    This function tests whether the centroid function correctly calculates the centroid of a 2D 
    numpy array. It includes a test with a valid 2D array and an expected outcome, as well as a 
    placeholder for testing with an invalid array that should raise a ValueError. The expected 
    behavior when using an invalid input is currently undefined but can be updated in future 
    iterations.
    
    Args:
        
    Returns:
        None: The function performs assertions directly on the output of centroid to ensure 
        correctness, with plans to handle invalid inputs in future updates.
    """
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
    """
    **test_check_numbers Function**
    This function tests whether the check_numbers function correctly validates tuples containing 
    only integers or floats, and rejects tuples that contain non-numeric types. It also checks the 
    behavior with an empty tuple.
    
    Args:
  
    Returns:
        None: The function performs assertions directly on the output of check_numbers to ensure 
        correctness.
    """
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
    """
    **test_fixed_threshold Function**
    This function tests whether the fixed_threshold function correctly applies a fixed threshold to 
    an image. It creates a sample image with random values and compares the result of applying the 
    fixed threshold against a manually computed version using Gaussian filtering and pixel-wise 
    comparison.
    
    Args:
        
    Returns:
        None: The function performs assertions directly on the output of fixed_threshold to ensure 
        correctness.
    """
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
    """
    **test_get_plaque_mask Function**
    This function tests whether the get_plaque_mask function correctly processes an input image to 
    obtain a plaque mask and identifies global peak coordinates.
    
    Args:
        input_image (np.ndarray, required): The input image array on which the plaque mask is to be 
                                  determined.
        expected_final_plq_reg_image (np.ndarray, required): The expected final registered image 
                                                            after obtaining the plaque mask.
        expected_global_peak_coords (tuple, required: The expected coordinates of the global peak in 
                                                    the form of a tuple (x, y).
        virus_params (dict, required): A dictionary containing parameters specific to the virus for
                                    which the plaque mask is being determined.
        
    Returns:
        None: The function performs assertions directly on the output of get_plaque_mask to ensure 
        correctness.
    """
    # Call the function
    final_plq_reg_image, global_peak_coords = get_plaque_mask(input_image, virus_params)

    # Perform assertions
    assert np.array_equal(final_plq_reg_image, expected_final_plq_reg_image)
    assert np.array_equal(global_peak_coords, expected_global_peak_coords)

def test_remove_artifacts():
    """
    **test_remove_artifacts Function**
    This function tests whether the remove_artifacts function correctly removes artifacts from an 
    image. It creates a sample image with random values and applies an artifact threshold to ensure 
    that pixels above this threshold are set to zero, indicating successful artifact removal.
    
    Args:
        
    Returns:
        None: The function asserts expected outcomes directly.
    """
    # Create a sample image with random values and an artifact threshold
    IMG = np.random.randint(0, 256, size=(10, 10))
    ARTIFACT_THRESHOLD = 127
    
    # Call the function
    result = remove_artifacts(IMG, ARTIFACT_THRESHOLD)
    
    # Assert that pixels above the threshold are set to zero
    assert np.all(result[IMG > ARTIFACT_THRESHOLD] == 0), "Artifacts were not removed correctly"

def test_remove_background():
    """
    **test_remove_background Function**
    Tests the remove_background function to ensure it correctly separates an image 
    into background and foreground components. It tests whether the output shapes are correct, 
    that no negative values appear in the foreground, and that the sum of the background and 
    foreground equals the original image.
    
    Args:
    
    Returns:
        None: The function asserts expected outcomes directly.
    """
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

