import numpy as np
import pytest

from PyPlaque.utils import remove_artifacts

@pytest.fixture()
def utils_remove_artifacts_input():
    return np.array([0, 0.25, 0, 0.9, 0]), 0.24

@pytest.fixture()
def utils_remove_artifacts_res():
    return np.array([0, 0, 0, 0, 0])

def test_utils_remove_artifacts(utils_remove_artifacts_input,utils_remove_artifacts_res):
    assert (utils_remove_artifacts_res == remove_artifacts(*utils_remove_artifacts_input)).all