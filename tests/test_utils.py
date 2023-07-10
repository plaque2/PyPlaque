import numpy as np
import pytest
from skimage import measure
import skimage.filters
import skimage.feature

from PyPlaque.utils import remove_artifacts, get_plaque_mask

@pytest.fixture()
def utils_remove_artifacts_input():
    return np.array([0, 0.25, 0, 0.9, 0]), 0.24

@pytest.fixture()
def utils_remove_artifacts_res():
    return np.array([0, 0, 0, 0, 0])

def test_utils_remove_artifacts(utils_remove_artifacts_input, utils_remove_artifacts_res):
    assert (utils_remove_artifacts_res == remove_artifacts(*utils_remove_artifacts_input)).all

@pytest.fixture()
def inputImage():
    return np.array([[0, 0, 0, 0, 0],
                     [0, 0, 1, 0, 0],
                     [0, 1, 4, 1, 0],
                     [0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0]])

@pytest.fixture()
def expected_finalPlqRegImage():
    return np.array([[0, 1, 1, 1, 0],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1],
                     [0, 1, 1, 1, 0]])

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

def test_get_plaque_mask(inputImage, expected_finalPlqRegImage, expected_globalPeakCoords, virus_params):
    # Call the function
    finalPlqRegImage, globalPeakCoords = get_plaque_mask(inputImage, virus_params)

    # Perform assertions
    assert np.array_equal(finalPlqRegImage, expected_finalPlqRegImage)
    assert np.array_equal(globalPeakCoords, expected_globalPeakCoords)