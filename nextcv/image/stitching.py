"""Image stitching utilities for left-right camera pairs.

This module provides clean, extensible classes for stitching images from
left and right cameras with proper geometric alignment and blending.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Literal, Optional, Tuple

import cv2
import numpy as np
from pydantic import BaseModel, Field

from nextcv.sensors.camera import Camera

logger = logging.getLogger(__name__)
POINT_2D_LENGTH = 2


class StitchingConfig(BaseModel):
    """Configuration for image stitching operations."""

    transition_mode: Literal["linear", "cosine"] = Field(
        default="linear",
        description="Type of blending transition ('linear' or 'cosine')",
    )
    lower_threshold: int = Field(
        default=0, description="Minimum pixel value for contrast clipping"
    )
    upper_threshold: int = Field(
        default=255, description="Maximum pixel value for contrast clipping"
    )
    enable_brightness_correction: bool = Field(
        default=True, description="Whether to apply brightness correction"
    )


class VirtualCamera:
    """Represents a virtual camera for stitching operations."""

    def __init__(self, left_camera: Camera, right_camera: Camera) -> None:
        """Create a virtual camera from left and right cameras.

        Args:
            left_camera: Left camera configuration
            right_camera: Right camera configuration
        """
        self.left_camera = left_camera
        self.right_camera = right_camera
        self._compute_virtual_camera()

    def _compute_virtual_camera(self) -> None:
        """Compute virtual camera parameters for stitching."""
        # Average focal lengths
        self.fx = 0.5 * (self.left_camera.fx + self.right_camera.fx)
        self.fy = 0.5 * (self.left_camera.fy + self.right_camera.fy)

        # Average pitch (assuming cameras are roughly aligned)
        self.pitch = 0.5 * (self.left_camera.pitch + self.right_camera.pitch)

        # Virtual camera has no roll or yaw (aligned)
        self.roll = 0.0
        self.yaw = 0.0

        # Compute virtual resolution (side-by-side)
        # For 640x512 input images, we expect ~1280x512 output
        # Use the principal points to estimate the original image dimensions
        # Assuming principal point is roughly at center of original image
        estimated_width = int(
            2 * self.left_camera.cx
        )  # This should be ~640 for 640x512
        estimated_height = int(
            2 * self.left_camera.cy
        )  # This should be ~512 for 640x512

        # For side-by-side stitching, double the width
        self.width = estimated_width * 2  # Should be ~1280
        self.height = estimated_height  # Should be ~512

        # Principal point at center of virtual image
        self.cx = self.width / 2
        self.cy = self.height / 2

        # Create virtual camera object
        self.camera = Camera(
            fx=self.fx,
            fy=self.fy,
            cx=self.cx,
            cy=self.cy,
            roll=self.roll,
            pitch=self.pitch,
            yaw=self.yaw,
        )


class BaseStitcher(ABC):
    """Abstract base class for image stitchers."""

    def __init__(
        self,
        left_camera: Camera,
        right_camera: Camera,
        config: Optional[StitchingConfig] = None,
    ) -> None:
        """Initialize the stitcher.

        Args:
            left_camera: Left camera configuration
            right_camera: Right camera configuration
            config: Stitching configuration
        """
        self.left_camera = left_camera
        self.right_camera = right_camera
        self.config = config or StitchingConfig()

        self._setup_stitching()

    @abstractmethod
    def _setup_stitching(self) -> None:
        """Setup stitching parameters. Must be implemented by subclasses."""

    @abstractmethod
    def stitch(self, left_image: np.ndarray, right_image: np.ndarray) -> np.ndarray:
        """Stitch two images together. Must be implemented by subclasses."""

    def __call__(self, left_image: np.ndarray, right_image: np.ndarray) -> np.ndarray:
        """Allow stitcher to be called as a function."""
        return self.stitch(left_image, right_image)


class LRStitcher(BaseStitcher):
    """Left-Right image stitcher for camera pairs.

    This class provides a clean interface for stitching images from left and right
    cameras with proper geometric alignment and seamless blending.
    """

    def _setup_stitching(self) -> None:
        """Setup stitching parameters following the original approach."""
        logger.info("Setting up LR stitcher...")

        # Create raw virtual camera (full size)
        self.raw_virtual_camera = VirtualCamera(self.left_camera, self.right_camera)

        # Project corners and compute margins for cropping
        projected_corners = self._project_camera_corners()
        margins = self._compute_margins(projected_corners)

        # Create cropped virtual camera (only overlapping region)
        self.virtual_camera = self._create_cropped_virtual_camera(margins)

        # Compute homographies from cropped virtual camera to input cameras
        self.homography_virtual_to_left = (
            self.virtual_camera.camera.compute_homography_to(self.left_camera)
        )
        self.homography_virtual_to_right = (
            self.virtual_camera.camera.compute_homography_to(self.right_camera)
        )

        # Compute intersection polygon for proper blending
        self.intersection_polygon = self._compute_intersection_polygon()

        # Compute transition mask
        self.transition_mask = self._compute_transition_mask()

        # Split mask for left and right regions
        self.left_mask, self.right_mask = self._split_mask()

        logger.info(
            f"LR stitcher setup complete. Output size: "
            f"{self.virtual_camera.width}x{self.virtual_camera.height}"
        )

    def stitch(self, left_image: np.ndarray, right_image: np.ndarray) -> np.ndarray:
        """Stitch left and right images together using proper geometric warping.

        Args:
            left_image: Left camera image
            right_image: Right camera image

        Returns:
            Stitched image with proper geometric alignment
        """
        # Clip values for contrast control
        left_image = np.clip(
            left_image, self.config.lower_threshold, self.config.upper_threshold
        )
        right_image = np.clip(
            right_image, self.config.lower_threshold, self.config.upper_threshold
        )

        # Warp images to virtual camera space using the correct homography direction
        left_warped = self._warp_image(left_image, self.homography_virtual_to_left)
        right_warped = self._warp_image(right_image, self.homography_virtual_to_right)

        # Apply brightness correction if enabled
        if self.config.enable_brightness_correction:
            left_warped, right_warped = self._apply_brightness_correction(
                left_warped, right_warped, left_image, right_image
            )

        # Blend images using the proper mask approach
        stitched = self._blend_images_with_masks(left_warped, right_warped)

        return stitched

    def _compute_intersection_polygon(self) -> Dict[str, np.ndarray]:
        """Compute intersection polygon for blending regions using corner projection.

        Returns:
            Dictionary with intersection polygon corners
        """
        # Project corners of both cameras to raw virtual camera space
        projected_corners = self._project_camera_corners()

        # Calculate margins based on projected corners
        margins = self._compute_margins(projected_corners)

        # Create intersection polygon using projected corners and margins
        intersection_polygon = {
            "top_left": np.array(projected_corners["corner_r_top_left"])
            - np.array([margins["left"], margins["top"]]),
            "top_right": np.array(projected_corners["corner_l_top_right"])
            - np.array([margins["left"], margins["top"]]),
            "bottom_left": np.array(projected_corners["corner_r_bottom_left"])
            - np.array([margins["left"], margins["top"]]),
            "bottom_right": np.array(projected_corners["corner_l_bottom_right"])
            - np.array([margins["left"], margins["top"]]),
        }

        return intersection_polygon

    def _project_camera_corners(self) -> Dict[str, np.ndarray]:
        """Project corners of both input cameras to raw virtual camera space.

        Returns:
            Dictionary with projected corner coordinates
        """
        # Get homographies from raw virtual camera to input cameras
        hom_raw_to_left = self.raw_virtual_camera.camera.compute_homography_to(
            self.left_camera
        )
        hom_raw_to_right = self.raw_virtual_camera.camera.compute_homography_to(
            self.right_camera
        )

        # Invert to get homographies from input cameras to raw virtual camera
        hom_left_to_raw = np.linalg.inv(hom_raw_to_left)
        hom_right_to_raw = np.linalg.inv(hom_raw_to_right)

        # Define corner coordinates of input images (assuming 640x512)
        input_width = int(2 * self.left_camera.cx)  # Should be ~640
        input_height = int(2 * self.left_camera.cy)  # Should be ~512

        corner_top_left = [0, 0]
        corner_top_right = [input_width, 0]
        corner_bottom_left = [0, input_height]
        corner_bottom_right = [input_width, input_height]

        # Project corners of left camera to raw virtual camera
        corner_l_top_left = self._apply_homography(corner_top_left, hom_left_to_raw)
        corner_l_top_right = self._apply_homography(corner_top_right, hom_left_to_raw)
        corner_l_bottom_left = self._apply_homography(
            corner_bottom_left, hom_left_to_raw
        )
        corner_l_bottom_right = self._apply_homography(
            corner_bottom_right, hom_left_to_raw
        )

        # Project corners of right camera to raw virtual camera
        corner_r_top_left = self._apply_homography(corner_top_left, hom_right_to_raw)
        corner_r_top_right = self._apply_homography(corner_top_right, hom_right_to_raw)
        corner_r_bottom_left = self._apply_homography(
            corner_bottom_left, hom_right_to_raw
        )
        corner_r_bottom_right = self._apply_homography(
            corner_bottom_right, hom_right_to_raw
        )

        return {
            "corner_l_top_left": corner_l_top_left,
            "corner_l_top_right": corner_l_top_right,
            "corner_l_bottom_left": corner_l_bottom_left,
            "corner_l_bottom_right": corner_l_bottom_right,
            "corner_r_top_left": corner_r_top_left,
            "corner_r_top_right": corner_r_top_right,
            "corner_r_bottom_left": corner_r_bottom_left,
            "corner_r_bottom_right": corner_r_bottom_right,
        }

    def _apply_homography(
        self, point: List[float], homography: np.ndarray
    ) -> np.ndarray:
        """Apply homography transformation to a point.

        Args:
            point: [x, y] coordinates
            homography: 3x3 homography matrix

        Returns:
            Transformed point [x, y]
        """
        pt = (
            np.array([point[0], point[1], 1])
            if len(point) == POINT_2D_LENGTH
            else np.array(point)
        )

        pt_trans = homography @ pt
        pt_trans = pt_trans / pt_trans[2]  # normalize
        return pt_trans[:2]

    def _compute_margins(
        self, projected_corners: Dict[str, np.ndarray]
    ) -> Dict[str, float]:
        """Compute margins for cropping the virtual camera based on projected corners.

        Args:
            projected_corners: Dictionary with projected corner coordinates

        Returns:
            Dictionary with margin values
        """
        # Get all projected corners
        all_corners = [
            projected_corners["corner_l_top_left"],
            projected_corners["corner_l_top_right"],
            projected_corners["corner_l_bottom_left"],
            projected_corners["corner_l_bottom_right"],
            projected_corners["corner_r_top_left"],
            projected_corners["corner_r_top_right"],
            projected_corners["corner_r_bottom_left"],
            projected_corners["corner_r_bottom_right"],
        ]

        # Calculate bounds
        x_coords = [corner[0] for corner in all_corners]
        y_coords = [corner[1] for corner in all_corners]

        # Find the bounding box of all projected corners
        min_x = min(x_coords)
        max_x = max(x_coords)
        min_y = min(y_coords)
        max_y = max(y_coords)

        # Calculate margins to crop to the overlapping region
        left_margin = max(0, -min_x)
        right_margin = max(0, max_x - self.raw_virtual_camera.width)
        top_margin = max(0, -min_y)
        bottom_margin = max(0, max_y - self.raw_virtual_camera.height)

        # Make margins symmetric for left-right
        symmetric_margin = max(left_margin, right_margin)

        return {
            "top": top_margin,
            "bottom": bottom_margin,
            "left": symmetric_margin,
            "right": symmetric_margin,
        }

    def _create_cropped_virtual_camera(
        self, margins: Dict[str, float]
    ) -> "VirtualCamera":
        """Create a cropped virtual camera with only the overlapping region.

        Args:
            margins: Dictionary with margin values

        Returns:
            Cropped virtual camera
        """
        # Calculate cropped dimensions
        cropped_width = int(
            self.raw_virtual_camera.width - margins["left"] - margins["right"]
        )
        cropped_height = int(
            self.raw_virtual_camera.height - margins["top"] - margins["bottom"]
        )

        # Create cropped virtual camera
        cropped_camera = Camera(
            fx=self.raw_virtual_camera.fx,
            fy=self.raw_virtual_camera.fy,
            cx=self.raw_virtual_camera.cx - margins["left"],
            cy=self.raw_virtual_camera.cy - margins["top"],
            roll=self.raw_virtual_camera.roll,
            pitch=self.raw_virtual_camera.pitch,
            yaw=self.raw_virtual_camera.yaw,
        )

        # Create virtual camera object with cropped dimensions
        cropped_virtual = VirtualCamera.__new__(VirtualCamera)
        cropped_virtual.camera = cropped_camera
        cropped_virtual.width = cropped_width
        cropped_virtual.height = cropped_height
        cropped_virtual.fx = self.raw_virtual_camera.fx
        cropped_virtual.fy = self.raw_virtual_camera.fy
        cropped_virtual.cx = self.raw_virtual_camera.cx - margins["left"]
        cropped_virtual.cy = self.raw_virtual_camera.cy - margins["top"]
        cropped_virtual.roll = self.raw_virtual_camera.roll
        cropped_virtual.pitch = self.raw_virtual_camera.pitch
        cropped_virtual.yaw = self.raw_virtual_camera.yaw

        return cropped_virtual

    def _split_mask(self) -> Tuple[np.ndarray, np.ndarray]:
        """Split the transition mask into left and right masks.

        Returns:
            Tuple of (left_mask, right_mask)
        """
        # Calculate left and right rectangle widths based on intersection polygon
        left_rect_width = self._get_left_rect_width()
        right_rect_width = self._get_right_rect_width()

        # Split mask using calculated widths (following original approach)
        left_mask = self.transition_mask[:, :left_rect_width]
        right_mask = 1.0 - self.transition_mask[:, -right_rect_width:]

        return left_mask, right_mask

    def _get_left_rect_width(self) -> int:
        """Get the width of the left rectangle (following original approach)."""
        w = round(
            max(
                self.intersection_polygon["top_right"][0],
                self.intersection_polygon["bottom_right"][0],
            )
        )
        return int(w)

    def _get_right_rect_width(self) -> int:
        """Get the width of the right rectangle (following original approach)."""
        w = self.virtual_camera.width - round(
            min(
                self.intersection_polygon["top_left"][0],
                self.intersection_polygon["bottom_left"][0],
            )
        )
        return int(w)

    def _blend_images_with_masks(
        self, left_warped: np.ndarray, right_warped: np.ndarray
    ) -> np.ndarray:
        """Blend warped images using the proper mask approach from the original.

        Args:
            left_warped: Warped left image
            right_warped: Warped right image

        Returns:
            Blended stitched image
        """
        height, width = self.virtual_camera.height, self.virtual_camera.width

        # Get rectangle widths
        left_rect_width = self._get_left_rect_width()
        right_rect_width = self._get_right_rect_width()

        # Initialize output image
        stitched = np.zeros((height, width), dtype=left_warped.dtype)

        # Apply left mask to left region (following original approach)
        stitched[:, :left_rect_width] = (
            left_warped[:, :left_rect_width] * self.left_mask
        ).astype(stitched.dtype)

        # Apply right mask to right region (following original approach)
        stitched[:, -right_rect_width:] += (
            right_warped[:, -right_rect_width:] * self.right_mask
        ).astype(stitched.dtype)

        return stitched

    def _warp_image(self, image: np.ndarray, homography: np.ndarray) -> np.ndarray:
        """Warp an image using homography transformation.

        Args:
            image: Input image to warp
            homography: 3x3 homography matrix

        Returns:
            Warped image
        """
        height, width = self.virtual_camera.height, self.virtual_camera.width

        # Create coordinate grids for the virtual camera
        y_coords, x_coords = np.mgrid[0:height, 0:width]
        coords = np.stack([x_coords, y_coords, np.ones_like(x_coords)], axis=0)

        # Transform coordinates using homography
        transformed_coords = np.einsum("ij,jkl->ikl", homography, coords)

        # Normalize homogeneous coordinates
        x_warped = (transformed_coords[0] / transformed_coords[2]).astype(np.float32)
        y_warped = (transformed_coords[1] / transformed_coords[2]).astype(np.float32)

        # Use OpenCV remap for efficient warping
        warped = cv2.remap(
            image,
            x_warped,
            y_warped,
            cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_CONSTANT,
            borderValue=0,
        )

        return warped

    def _apply_brightness_correction(
        self,
        left_warped: np.ndarray,
        right_warped: np.ndarray,
        left_original: np.ndarray,
        right_original: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Apply brightness correction to reduce seam artifacts.

        Args:
            left_warped: Warped left image
            right_warped: Warped right image
            left_original: Original left image
            right_original: Original right image

        Returns:
            Brightness-corrected warped images
        """
        # Sample overlapping regions for brightness matching
        height_offset = left_original.shape[0] // 4
        width_offset = left_original.shape[1] // 8

        # Calculate mean brightness in overlapping regions
        mean_left = np.mean(left_original[height_offset:-height_offset, -width_offset:])
        mean_right = np.mean(
            right_original[height_offset:-height_offset, :width_offset]
        )
        mean_diff = mean_left - mean_right

        # Apply correction with proper bounds checking
        correction = int(round(mean_diff / 2))

        # Convert to float for safe arithmetic, then clip to valid range
        left_corrected = left_warped.astype(np.float32) - correction
        right_corrected = right_warped.astype(np.float32) + correction

        # Get the original dtype bounds
        min_val, max_val = (
            np.iinfo(left_warped.dtype).min,
            np.iinfo(left_warped.dtype).max,
        )

        # Clip to valid range and convert back to original dtype
        left_corrected = np.clip(left_corrected, min_val, max_val).astype(
            left_warped.dtype
        )
        right_corrected = np.clip(right_corrected, min_val, max_val).astype(
            right_warped.dtype
        )

        return left_corrected, right_corrected

    def _compute_transition_mask(self) -> np.ndarray:
        """Compute transition mask for blending using intersection polygon.

        Returns:
            Transition mask array
        """
        height, width = self.virtual_camera.height, self.virtual_camera.width
        mask = np.zeros((height, width), dtype=float)

        # Use the original approach: row-by-row intersection calculation
        for row in range(height):
            # Calculate intersection points for this row using the original method
            x1 = self._intersect_with_horizontal_line(
                [
                    self.intersection_polygon["top_left"],
                    self.intersection_polygon["bottom_left"],
                ],
                float(row),
            )
            x2 = self._intersect_with_horizontal_line(
                [
                    self.intersection_polygon["top_right"],
                    self.intersection_polygon["bottom_right"],
                ],
                float(row),
            )

            if x1 is not None and x2 is not None:
                # Create transition using the original transition function
                mask[row] = self._transition_function(
                    0, width, int(x1), int(x2), self.config.transition_mode
                )
            else:
                # Fallback: simple split if no intersection
                mask[row, : width // 2] = 1.0
                mask[row, width // 2 :] = 0.0

        return mask

    def _intersect_with_horizontal_line(
        self, points_on_line: List[np.ndarray], height: float
    ) -> Optional[float]:
        """Calculate intersection of a line with a horizontal line (from original code).

        Args:
            points_on_line: List of two points defining the line [(x1, y1), (x2, y2)]
            height: y-coordinate of the horizontal line

        Returns:
            x-coordinate of intersection point, or None if no intersection
        """
        p1, p2 = points_on_line
        if p1[1] == p2[1]:
            return None
        return p1[0] + (height - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1])

    def _transition_function(
        self,
        range_min: int,
        range_max: int,
        transition_start: int,
        transition_end: int,
        transition_type: str,
    ) -> np.ndarray:
        """Compute a transition from 1 to 0 (from original code).

        Args:
            range_min: Minimum range value
            range_max: Maximum range value
            transition_start: Start of transition region
            transition_end: End of transition region
            transition_type: Type of transition ("linear" or "cosine")

        Returns:
            Transition array
        """
        transition = np.zeros(range_max - range_min)
        transition[:transition_start] = 1

        if transition_type == "linear":
            transition[transition_start:transition_end] = np.linspace(
                1, 0, num=transition_end - transition_start, endpoint=True
            )
        elif transition_type == "cosine":
            transition[transition_start:transition_end] = (
                np.cos(
                    np.linspace(
                        0,
                        np.pi / 2,
                        num=transition_end - transition_start,
                        endpoint=True,
                    )
                )
                ** 2
            )

        return transition
