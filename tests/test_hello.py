import numpy as np

import nextcv


def test_hello():
    """Test the hello function returns a valid greeting."""
    msg = nextcv.hello()
    assert isinstance(msg, str)
    assert msg.startswith("Hello")


def test_invert():
    """Test basic invert function with 1D arrays."""
    # Test with a simple array
    data = np.array([0, 64, 128, 192, 255], dtype=np.uint8)
    inverted = nextcv.invert(data)

    # Check that the result is a numpy array
    assert isinstance(inverted, np.ndarray)
    assert inverted.dtype == np.uint8

    # Check that the inversion is correct
    expected = np.array([255, 191, 127, 63, 0], dtype=np.uint8)
    assert np.array_equal(inverted, expected)

    # Test with a single value
    single = np.array([100], dtype=np.uint8)
    single_inverted = nextcv.invert(single)
    assert single_inverted[0] == 155  # 255 - 100


def test_invert_edge_cases():
    """Test invert function with edge cases like empty arrays."""
    # Test with empty array
    empty = np.array([], dtype=np.uint8)
    empty_inverted = nextcv.invert(empty)
    assert len(empty_inverted) == 0

    # Test with all zeros
    zeros = np.zeros(5, dtype=np.uint8)
    zeros_inverted = nextcv.invert(zeros)
    assert np.all(zeros_inverted == 255)

    # Test with all 255s
    max_vals = np.full(5, 255, dtype=np.uint8)
    max_inverted = nextcv.invert(max_vals)
    assert np.all(max_inverted == 0)


def test_invert_2d():
    """Test invert function with 2D arrays (e.g., grayscale images)."""
    # Test with a simple 2D array
    data_2d = np.array([[0, 64, 128], [192, 255, 32]], dtype=np.uint8)
    inverted_2d = nextcv.invert(data_2d)
    
    # Check shape is preserved
    assert inverted_2d.shape == data_2d.shape
    assert inverted_2d.dtype == np.uint8
    
    # Check inversion is correct
    expected_2d = np.array([[255, 191, 127], [63, 0, 223]], dtype=np.uint8)
    assert np.array_equal(inverted_2d, expected_2d)


def test_invert_3d():
    """Test invert function with 3D arrays (e.g., RGB images)."""
    # Test with a simple 3D array (2x2x3 RGB image)
    data_3d = np.array([[[0, 128, 255], [64, 192, 32]], 
                        [[255, 0, 128], [96, 160, 224]]], dtype=np.uint8)
    inverted_3d = nextcv.invert(data_3d)
    
    # Check shape is preserved
    assert inverted_3d.shape == data_3d.shape
    assert inverted_3d.dtype == np.uint8
    
    # Check inversion is correct
    expected_3d = np.array([[[255, 127, 0], [191, 63, 223]], 
                            [[0, 255, 127], [159, 95, 31]]], dtype=np.uint8)
    assert np.array_equal(inverted_3d, expected_3d)


def test_invert_4d():
    """Test invert function with 4D arrays (e.g., batch of RGB images)."""
    # Test with a 4D array (batch_size=2, height=2, width=2, channels=2)
    data_4d = np.random.randint(0, 256, size=(2, 2, 2, 2), dtype=np.uint8)
    inverted_4d = nextcv.invert(data_4d)
    
    # Check shape is preserved
    assert inverted_4d.shape == data_4d.shape
    assert inverted_4d.dtype == np.uint8
    
    # Check inversion is correct element-wise
    expected_4d = 255 - data_4d
    assert np.array_equal(inverted_4d, expected_4d)
