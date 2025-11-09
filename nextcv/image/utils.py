"""Utility functions for image processing."""

from typing import Tuple, Union

import numpy as np


def largest_inscribed_rect(mask: np.ndarray) -> Tuple[int, int, int, int]:
    """Find the largest inscribed rectangle in a binary mask.

    Args:
        mask: uint8 (0/255) or bool, shape (H,W). Non-zero = inside.

    Returns:
    returns (top, left, height, width)
    """
    mask = (mask > 0).astype(np.uint8)
    H, W = mask.shape
    heights = np.zeros(W, dtype=int)
    best = (0, 0, 0, 0)  # top, left, h, w
    best_area = 0

    for i in range(H):
        heights += mask[i]
        heights[mask[i] == 0] = 0

        stack = []
        for j in range(W + 1):  # sentinel
            h = heights[j] if j < W else 0
            start = j
            while stack and heights[stack[-1]] > h:
                idx = stack.pop()
                start = stack[-1] + 1 if stack else 0
                w = j - start
                area = heights[idx] * w
                if area > best_area:
                    best_area = area
                    top = i - heights[idx] + 1
                    left = start
                    best = (top.item(), left, heights[idx].item(), w)
            stack.append(j)
    return best


def find_x_at_y(
    p1: np.ndarray, p2: np.ndarray, y: Union[float, np.ndarray]
) -> np.ndarray:
    """Find x-coordinate where line segment intersects horizontal line at y.

    Uses line equation: y = m*x + b, solving for x = (y - b) / m

    Args:
        p1: endpoint of a line
        p2: endpoint of a line
        y: Height(s) to find x at (scalar or array)
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]

    # y = m*x + b where m = dy/dx
    m = dy / dx
    b = p1[1] - m * p1[0]

    # x = (y - b) / m, but for horizontal lines (m=0) return midpoint
    x = np.where(m == 0, p1[0] + dx / 2, (y - b) / m)
    return x


def bounds_from_lr_corners(
    roi_left: np.ndarray, roi_right: np.ndarray
) -> tuple[float, float, float, float]:
    """Returns (top, bottom, left, right) bounds.

    Args:
        roi_left: (4, 2) array: [top_left, top_right, bottom_right, bottom_left]
        roi_right: (4, 2) array: [top_left, top_right, bottom_right, bottom_left]
        resolution: (width, height)
        symmetric: whether to make the left and right margins symmetric

    Returns:
        (top, bottom, left, right) margins
    """
    # Vertical bounds
    top_bound = np.vstack([roi_left[:2], roi_right[:2]])[:, 1].max()
    bottom_bound = np.vstack([roi_left[2:], roi_right[2:]])[:, 1].min()

    # Horizontal bounds via line intersection at top and bottom
    bounds = np.array([top_bound, bottom_bound])
    left_bound = find_x_at_y(roi_left[0], roi_left[3], bounds).max()
    right_bound = find_x_at_y(roi_right[1], roi_right[2], bounds).min()

    return (
        top_bound.item(),
        bottom_bound.item(),
        left_bound.item(),
        right_bound.item(),
    )
