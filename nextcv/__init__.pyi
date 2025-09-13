import numpy as np
from numpy.typing import NDArray

def hello() -> str: ...
def invert(pixels: NDArray[np.uint8]) -> NDArray[np.uint8]: ...

__all__ = ["hello", "invert"]
