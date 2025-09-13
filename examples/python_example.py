import numpy as np

import nextcv


def main() -> None:
    """Demonstrate NextCV functionality with various array dimensions."""
    print("=== NextCV Python Example ===")
    print(nextcv.hello())
    print(f"Version: {nextcv.get_version()}")
    print(f"Build info: {nextcv.get_build_info()}")

    # Example with 1D numpy array
    print("\n1D Array Example:")
    data_1d = np.array([0, 64, 128, 192, 255], dtype=np.uint8)
    print("Original 1D array:", data_1d)
    inverted_1d = nextcv.invert(data_1d)
    print("Inverted 1D array:", inverted_1d)
    expected_1d = np.array([255, 191, 127, 63, 0], dtype=np.uint8)
    print("Expected:         ", expected_1d)
    print("Match:", np.array_equal(inverted_1d, expected_1d))

    # Example with 2D numpy array (grayscale image)
    print("\n2D Array Example (Grayscale Image):")
    data_2d = np.array([[0, 128, 255], [64, 192, 32]], dtype=np.uint8)
    print("Original 2D array:")
    print(data_2d)
    inverted_2d = nextcv.invert(data_2d)
    print("Inverted 2D array:")
    print(inverted_2d)
    print("Shape preserved:", data_2d.shape == inverted_2d.shape)

    # Example with 3D numpy array (RGB image)
    print("\n3D Array Example (RGB Image):")
    # Create a small 2x2 RGB image
    data_3d = np.array(
        [[[255, 0, 128], [128, 128, 128]], [[0, 255, 0], [255, 255, 255]]], dtype=np.uint8
    )
    print("Original 3D array shape:", data_3d.shape)
    print("Original 3D array:")
    print(data_3d)
    inverted_3d = nextcv.invert(data_3d)
    print("Inverted 3D array:")
    print(inverted_3d)
    print("Shape preserved:", data_3d.shape == inverted_3d.shape)

    # Example with threshold operation
    print("\nThreshold Example:")
    data_thresh = np.array([50, 100, 150, 200, 250], dtype=np.uint8)
    print("Original array:", data_thresh)
    thresholded = nextcv.threshold(data_thresh, 128)
    print("Thresholded (128):", thresholded)
    expected_thresh = np.array([0, 0, 255, 255, 255], dtype=np.uint8)
    print("Expected:        ", expected_thresh)
    print("Match:", np.array_equal(thresholded, expected_thresh))


if __name__ == "__main__":
    main()
