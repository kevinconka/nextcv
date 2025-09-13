import nextcv
import numpy as np


def test_hello():
    msg = nextcv.hello()
    assert isinstance(msg, str)
    assert msg.startswith("Hello")


def test_invert_numpy():
    # Test with a simple array
    data = np.array([0, 64, 128, 192, 255], dtype=np.uint8)
    inverted = nextcv.invert_numpy(data)
    
    # Check that the result is a numpy array
    assert isinstance(inverted, np.ndarray)
    assert inverted.dtype == np.uint8
    
    # Check that the inversion is correct
    expected = np.array([255, 191, 127, 63, 0], dtype=np.uint8)
    assert np.array_equal(inverted, expected)
    
    # Test with a single value
    single = np.array([100], dtype=np.uint8)
    single_inverted = nextcv.invert_numpy(single)
    assert single_inverted[0] == 155  # 255 - 100


def test_invert_numpy_edge_cases():
    # Test with empty array
    empty = np.array([], dtype=np.uint8)
    empty_inverted = nextcv.invert_numpy(empty)
    assert len(empty_inverted) == 0
    
    # Test with all zeros
    zeros = np.zeros(5, dtype=np.uint8)
    zeros_inverted = nextcv.invert_numpy(zeros)
    assert np.all(zeros_inverted == 255)
    
    # Test with all 255s
    max_vals = np.full(5, 255, dtype=np.uint8)
    max_inverted = nextcv.invert_numpy(max_vals)
    assert np.all(max_inverted == 0)
