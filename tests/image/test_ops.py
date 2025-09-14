"""Test image operations."""

import numpy as np
import pytest

import nextcv.image as cvi


@pytest.mark.parametrize(
    "input_array,expected",
    [
        (
            np.array([0, 128, 255], dtype=np.uint8),
            np.array([255, 127, 0], dtype=np.uint8),
        ),
        (
            np.array([[0, 128], [255, 64]], dtype=np.uint8),
            np.array([[255, 127], [0, 191]], dtype=np.uint8),
        ),
        (
            np.zeros(5, dtype=np.uint8),
            np.full(5, 255, dtype=np.uint8),
        ),
        (
            np.full(5, 255, dtype=np.uint8),
            np.zeros(5, dtype=np.uint8),
        ),
    ],
)
def test_invert(input_array: np.ndarray, expected: np.ndarray):
    """Test image inversion with various inputs."""
    result = cvi.invert(input_array)
    np.testing.assert_array_equal(result, expected)


def test_invert_preserves_shape():
    """Test that inversion preserves input shape."""
    # Test with 3D array (H, W, C)
    rng = np.random.Generator(np.random.PCG64())
    input_array = rng.integers(0, 256, (10, 20, 3), dtype=np.uint8)

    result = cvi.invert(input_array)

    assert result.shape == input_array.shape
    assert result.dtype == input_array.dtype
