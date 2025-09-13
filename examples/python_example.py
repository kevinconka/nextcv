import numpy as np

import nextcv


def main() -> None:
    print(nextcv.hello())

    # Example with numpy array (more realistic for computer vision)
    data = np.array([0, 64, 128, 192, 255], dtype=np.uint8)
    print("Original array:", data)

    inverted = nextcv.invert(data)
    print("Inverted array:", inverted)

    # Verify the inversion worked correctly
    expected = np.array([255, 191, 127, 63, 0], dtype=np.uint8)
    print("Expected:     ", expected)
    print("Match:", np.array_equal(inverted, expected))


if __name__ == "__main__":
    main()
