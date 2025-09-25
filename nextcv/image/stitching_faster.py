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

    def clamp_to(self, max_w: int, max_h: int) -> Optional["Rect"]:
        """Clamp region to bounds, return None if no overlap."""
        x = max(0, self.x)
        y = max(0, self.y)
        w = min(self.w, max_w - x)
        h = min(self.h, max_h - y)
        return Rect(x, y, w, h) if w > 0 and h > 0 else None

    @staticmethod
    def union(regions: List["Rect"]) -> "Rect":
        """Compute bounding region containing all input regions."""
        if not regions:
            return Rect(0, 0, 0, 0)
        x_min = min(r.x for r in regions)
        y_min = min(r.y for r in regions)
        x_max = max(r.x + r.w for r in regions)
        y_max = max(r.y + r.h for r in regions)
        return Rect(x_min, y_min, x_max - x_min, y_max - y_min)


@dataclass
class WarpTile:
    """A warped image tile with blending weights."""

    rect: Rect
    maps: tuple[np.ndarray, np.ndarray]  # source -> tile transform
    mask: np.ndarray  # (h,w) binary mask
    weights: np.ndarray  # (h,w) normalized blending weights

    def update_weights(self, weights: np.ndarray) -> "WarpTile":
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
    def project_camera_to(
        cls, camera: CameraType, target: CameraType
    ) -> Optional["WarpTile"]:
        """Create a warp tile from a camera."""
        # Get remapping maps from camera to target
        mapx, mapy = target.maps_from(camera)

        # Find bounding region in target coordinates using OpenCV
        # mapx, mapy are source coordinates for each target pixel
        valid_mask = (
            (mapx >= 0) & (mapx < camera.width) & (mapy >= 0) & (mapy < camera.height)
        ).astype(np.uint8)

        # Use OpenCV to find bounding rectangle of valid region
        points = cv2.findNonZero(valid_mask)
        if points is None:
            return None

        roi = Rect(*cv2.boundingRect(points)).clamp_to(*target.size)
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

        return WarpTile(rect=roi, maps=(roi_mapx, roi_mapy), mask=mask, weights=weights)


def create_warp_tiles(cameras: List[CameraType], target: CameraType) -> List[WarpTile]:
    """Create normalized warp tiles for all cameras."""
    # Build raw tiles
    raw_tiles = []
    for cam in cameras:
        tile = WarpTile.project_camera_to(cam, target)
        if tile:
            raw_tiles.append(tile)

    if not raw_tiles:
        return []

    return normalize_tile_weights(raw_tiles, target.size)


def normalize_tile_weights(
    tiles: List[WarpTile], target_wh: Tuple[int, int]
) -> List[WarpTile]:
    """Normalize tile weights so they sum to 1 at each pixel."""
    # Accumulate all weights
    weight_sum = np.zeros((target_wh[1], target_wh[0]), np.float32)
    for tile in tiles:
        weight_sum[tile.rect.numpy_slices()] += tile.weights
    weight_sum = np.clip(weight_sum, 1e-6, None)  # Avoid division by zero

    # Normalize each tile
    normalized_tiles = [
        tile.update_weights(tile.weights / weight_sum[tile.rect.numpy_slices()])
        for tile in tiles
    ]

    return normalized_tiles


class ImageStitcher(ABC, Generic[CameraType]):
    """Abstract base class for image stitching."""

    def __init__(self, cameras: List[CameraType]) -> None:
        """Create an image stitcher."""
        if not cameras:
            raise ValueError("At least one camera required")

        self.cameras = cameras
        self.virtual_camera = self._create_virtual_cam()
        self.tiles = create_warp_tiles(cameras, self.virtual_camera)

    @abstractmethod
    def _create_virtual_cam(self) -> CameraType:
        """Create virtual camera defining output coordinate system."""

    def stitch(self, images: List[np.ndarray]) -> np.ndarray:
        """Stitch images into the virtual camera."""
        if len(images) != len(self.cameras):
            raise ValueError(f"Expected {len(self.cameras)} images, got {len(images)}")

        stitched = np.zeros(self.virtual_camera.size[::-1], dtype=images[0].dtype)

        if not self.tiles:
            return stitched

        # construct stitched image
        for img, tile in zip(images, self.tiles):
            warped = tile.warp_image(img).astype(np.float32)
            slices = tile.rect.numpy_slices()
            stitched[slices] += (warped * tile.weights).astype(stitched.dtype)

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
