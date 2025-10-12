"""Generalized image stitching framework.

Simple, extensible architecture for stitching images from multiple cameras.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, Optional, Tuple, TypeVar

import cv2
import numpy as np

from nextcv.sensors.camera import Camera, PinholeCamera

CameraType = TypeVar("CameraType", bound=Camera)


# ============================================================================
# Rect and Tile Classes
# ============================================================================


@dataclass(frozen=True)
class Rect:
    """Image region defined by top-left corner and dimensions."""

    x: int
    y: int
    w: int
    h: int

    def numpy_slices(self, offset_x: int = 0, offset_y: int = 0) -> Tuple[slice, slice]:
        """Return (y_slice, x_slice) for numpy indexing with optional offset."""
        return (
            slice(self.y - offset_y, self.y - offset_y + self.h),
            slice(self.x - offset_x, self.x - offset_x + self.w),
        )

    @property
    def s(self) -> Tuple[slice, slice]:
        """Shorthand for numpy_slices() - returns (y_slice, x_slice).

        Usage:
            arr[rect.s] = value
        """
        return self.numpy_slices()

    def clamp_to(self, max_w: int, max_h: int) -> Optional["Rect"]:
        """Clamp region to bounds, return None if no overlap."""
        x = max(0, self.x)
        y = max(0, self.y)
        w = min(self.w, max_w - x)
        h = min(self.h, max_h - y)
        return Rect(x, y, w, h) if w > 0 and h > 0 else None

    def intersect(self, other: "Rect") -> Optional["Rect"]:
        """Compute intersection with another rectangle."""
        x = max(self.x, other.x)
        y = max(self.y, other.y)
        x_max = min(self.x + self.w, other.x + other.w)
        y_max = min(self.y + self.h, other.y + other.h)
        w = x_max - x
        h = y_max - y
        return Rect(x, y, w, h) if w > 0 and h > 0 else None


@dataclass
class Tile:
    """A tile within a canvas for image stitching."""

    rect: Rect
    maps: tuple[np.ndarray, np.ndarray]  # source -> tile transform
    mask: np.ndarray  # (h,w) binary mask
    weights: np.ndarray  # (h,w) normalized blending weights

    def update_weights(self, weights: np.ndarray) -> "Tile":
        """Update the weights."""
        self.weights = weights
        return self

    def warp_image(self, src_img: np.ndarray) -> np.ndarray:
        """Warp source image to this tile."""
        return cv2.remap(
            src_img,
            self.maps[0],
            self.maps[1],
            cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REPLICATE,
        )

    @classmethod
    def from_camera_pair(
        cls, camera: CameraType, canvas: CameraType
    ) -> Optional["Tile"]:
        """Create a warp tile from a camera."""
        # Get remapping maps from camera to target
        mapx, mapy = canvas.maps_from(camera)

        # Find bounding region in target coordinates using OpenCV
        # mapx, mapy are source coordinates for each target pixel
        valid_mask = (
            (mapx >= 0) & (mapx < camera.width) & (mapy >= 0) & (mapy < camera.height)
        ).astype(np.uint8)

        # Use OpenCV to find bounding rectangle of valid region
        points = cv2.findNonZero(valid_mask)
        if points is None:
            return None

        roi = Rect(*cv2.boundingRect(points)).clamp_to(*canvas.size)
        if not roi:
            return None

        # Extract maps for this region
        y_slice, x_slice = roi.numpy_slices()
        roi_mapx = mapx[y_slice, x_slice]
        roi_mapy = mapy[y_slice, x_slice]

        # Create mask for valid pixels in this region
        mask = valid_mask[y_slice, x_slice].astype(np.uint8)

        # Generate raw weights using distance transform
        weights = cv2.distanceTransform(mask, cv2.DIST_L2, 3).astype(np.float32)

        return Tile(rect=roi, maps=(roi_mapx, roi_mapy), mask=mask, weights=weights)


# ============================================================================
# Exposure Compensators
# ============================================================================


class ExposureCompensator(ABC):
    """Abstract base class for exposure compensation strategies.

    Compensators compute and apply corrections to warped images to minimize
    intensity differences in overlap regions.
    """

    @abstractmethod
    def __call__(
        self, tiles: List[Tile], warped_images: List[np.ndarray]
    ) -> List[np.ndarray]:
        """Compute and apply corrections to warped images.

        Args:
            tiles: List of tiles with rect, mask, and weights
            warped_images: List of warped images (one per tile)

        Returns:
            List of corrected images
        """


class NoOpCompensator(ExposureCompensator):
    """No compensation - returns images unchanged.

    Fastest option. Use when images are already well-balanced or when
    exposure differences are negligible.
    """

    def __call__(
        self, tiles: List[Tile], warped_images: List[np.ndarray]
    ) -> List[np.ndarray]:
        """Return images unchanged."""
        return warped_images


class AdditiveCompensator(ExposureCompensator):
    """Sequential additive bias correction.

    Computes median intensity difference in overlap regions and applies
    additive corrections. First image is used as reference. Each subsequent
    image is corrected to match the already-corrected previous image.

    Good for small-to-medium brightness differences in thermal cameras.
    """

    def __call__(self, tiles: List[Tile], images: List[np.ndarray]) -> List[np.ndarray]:
        """Compute and apply additive bias corrections."""
        corrected_images = [images[0]] * len(images)  # use first image as reference

        for i in range(1, len(images)):
            # Compute bias relative to corrected previous image
            bias = self._compute_bias_between_tiles(
                tiles[i - 1],
                tiles[i],
                corrected_images[i - 1],
                images[i],
            )

            # Apply correction
            corrected_images[i] = images[i] + bias

        return corrected_images

    @staticmethod
    def _compute_bias_between_tiles(
        tile_i: Tile,
        tile_j: Tile,
        img_i: np.ndarray,
        img_j: np.ndarray,
    ) -> float:
        """Compute intensity bias between two overlapping tiles.

        Args:
            tile_i: First tile (reference)
            tile_j: Second tile (to be corrected)
            img_i: Warped image from tile_i
            img_j: Warped image from tile_j

        Returns:
            Bias to add to img_j to match img_i (float scalar)
        """
        # 1. Compute overlap in canvas space
        overlap_canvas = tile_i.rect.intersect(tile_j.rect)
        if overlap_canvas is None:
            return 0.0

        # 2. Convert to LOCAL tile coordinates for extraction
        overlap_in_i = Rect(
            x=overlap_canvas.x - tile_i.rect.x,
            y=overlap_canvas.y - tile_i.rect.y,
            w=overlap_canvas.w,
            h=overlap_canvas.h,
        )
        overlap_in_j = Rect(
            x=overlap_canvas.x - tile_j.rect.x,
            y=overlap_canvas.y - tile_j.rect.y,
            w=overlap_canvas.w,
            h=overlap_canvas.h,
        )

        # 3. Extract overlap regions from warped tile images
        overlap_i = img_i[overlap_in_i.s]
        overlap_j = img_j[overlap_in_j.s]

        # 4. Apply masks to get valid pixels only
        mask_i = tile_i.mask[overlap_in_i.s] > 0
        mask_j = tile_j.mask[overlap_in_j.s] > 0
        mask_both = mask_i & mask_j

        if not np.any(mask_both):
            return 0.0

        # 5. Compute bias (difference in medians)
        median_i = np.median(overlap_i[mask_both])
        median_j = np.median(overlap_j[mask_both])
        bias = median_i - median_j

        return float(bias)


# ============================================================================
# Image Stitchers
# ============================================================================


class ImageStitcher(ABC, Generic[CameraType]):
    """Abstract base class for image stitching."""

    def __init__(
        self,
        cameras: List[CameraType],
        compensator: Optional[ExposureCompensator] = None,
    ) -> None:
        """Create an image stitcher.

        Args:
            cameras: List of cameras to stitch
            compensator: Exposure compensator to use. Defaults to NoOpCompensator()
        """
        if not cameras:
            raise ValueError("At least one camera required")

        self.cameras = cameras
        self.virtual_camera = self._create_virtual_cam()
        self.tiles = self.create_warp_tiles(cameras, self.virtual_camera)
        self.compensator = compensator or NoOpCompensator()

    @abstractmethod
    def _create_virtual_cam(self) -> CameraType:
        """Create virtual camera defining output coordinate system."""

    @staticmethod
    def create_warp_tiles(cameras: List[CameraType], canvas: CameraType) -> List[Tile]:
        """Create normalized warp tiles for all cameras."""
        # Build raw tiles
        tiles = [Tile.from_camera_pair(camera, canvas) for camera in cameras]
        tiles = [tile for tile in tiles if tile is not None]

        # Accumulate all weights
        weight_sum = np.zeros((canvas.height, canvas.width), np.float32)
        for tile in tiles:
            weight_sum[tile.rect.s] += tile.weights
        weight_sum = np.clip(weight_sum, 1e-6, None)  # Avoid division by zero

        # Normalize weights for each tile (also called feather weights)
        tiles = [
            tile.update_weights(tile.weights / weight_sum[tile.rect.s])
            for tile in tiles
        ]

        return tiles

    def _sanity_checks(self, images: List[np.ndarray]) -> None:
        """Sanity checks for the images."""
        if len(images) != len(self.cameras):
            raise ValueError(f"Expected {len(self.cameras)} images, got {len(images)}")

        # check if all images are the same dtype
        if not all(img.dtype == images[0].dtype for img in images):
            raise ValueError("All images must have the same dtype")

    def stitch(self, images: List[np.ndarray]) -> np.ndarray:
        """Stitch images into the virtual camera."""
        self._sanity_checks(images)

        stitched = np.zeros(self.virtual_camera.size[::-1], dtype=images[0].dtype)
        if not self.tiles:
            return stitched

        # 1. Warp images to virtual camera space
        warped_images = [
            tile.warp_image(img).astype(np.float32)
            for img, tile in zip(images, self.tiles)
        ]

        # 2. Apply exposure compensation
        corrected_images = self.compensator(self.tiles, warped_images)

        # 3. Blend corrected images into stitched result
        for corrected, tile in zip(corrected_images, self.tiles):
            stitched[tile.rect.s] += (corrected * tile.weights).astype(stitched.dtype)

        return stitched

    def __call__(self, images: List[np.ndarray]) -> np.ndarray:
        """Stitch images into panorama."""
        return self.stitch(images)


class HorizontalStitcher(ImageStitcher[PinholeCamera]):
    """Stitch cameras arranged horizontally (left-to-right)."""

    def _create_virtual_cam(self) -> PinholeCamera:
        # Concatenate all cameras horizontally
        virtual_cam = self.cameras[0]
        for cam in self.cameras[1:]:
            virtual_cam = PinholeCamera.hconcat(virtual_cam, cam)

        # Find bounding rectangle that contains all cameras
        all_corners = [
            cv2.perspectiveTransform(
                np.array(
                    [
                        [
                            [0, 0],
                            [cam.width, 0],
                            [cam.width, cam.height],
                            [0, cam.height],
                        ]
                    ],
                    dtype=np.float32,
                ),
                cam.compute_homography_to(virtual_cam),
            )[0]  # Remove batch dimension for each camera
            for cam in self.cameras
        ]
        all_corners = np.vstack(all_corners)
        x_min, y_min = all_corners.min(axis=0)
        x_max, y_max = all_corners.max(axis=0)

        # Compute margins needed to fit all corners
        left = max(0, -x_min)
        right = max(0, x_max - virtual_cam.width)
        top = max(0, -y_min)
        bottom = max(0, y_max - virtual_cam.height)

        # Symmetric horizontal margins for centering
        symmetric = max(left, right)
        return virtual_cam.crop(symmetric, top, symmetric, bottom)


# Convenience aliases
class LeftRightStitcher(HorizontalStitcher):
    """Stitch cameras arranged horizontally (left-to-right)."""

    def __init__(self, left_camera: PinholeCamera, right_camera: PinholeCamera) -> None:
        """Create a left-right stitcher."""
        super().__init__([left_camera, right_camera])
        self.left_camera = left_camera
        self.right_camera = right_camera
