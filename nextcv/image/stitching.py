"""Generalized image stitching framework.

Simple, extensible architecture for stitching images from multiple cameras.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple

import cv2
import numpy as np

from nextcv.sensors.camera import PinholeCamera as Camera

_NDIM_3C = 3
_DEFAULT_BLENDER = cv2.detail.FeatherBlender(sharpness=0.02)


@dataclass
class Rect:
    """Image region defined by top-left corner and dimensions."""

    x: int
    y: int
    w: int
    h: int

    @property
    def corner(self) -> Tuple[int, int]:
        """Return (x, y)."""
        return self.x, self.y

    @property
    def size(self) -> Tuple[int, int]:
        """Return (w, h)."""
        return self.w, self.h

    def numpy_slices(self) -> Tuple[slice, slice]:
        """Return (y_slice, x_slice) for numpy indexing."""
        return (slice(self.y, self.y + self.h), slice(self.x, self.x + self.w))


class ImageStitcher(ABC):
    """Abstract base class for image stitchers."""

    def __init__(
        self,
        cameras: List[Camera],
        blender: cv2.detail.FeatherBlender = _DEFAULT_BLENDER,
    ) -> None:
        """Create a base stitcher.

        Args:
            cameras: List of cameras to stitch
            blender: Blender to use for blending images
        """
        self.cameras = cameras
        self.blender = blender
        self.virtual_cam = self._create_virtual_cam()

        # initial homographies and masks
        self.homographies = [
            cam.compute_homography_to(self.virtual_cam) for cam in self.cameras
        ]
        self.masks = self.make_masks(
            self.cameras, self.homographies, self.virtual_cam.size
        )

        # define rects for optimized processing
        self.rects = self._compute_rects(self.masks)
        self._translate_homographies()
        self._crop_masks()

    @staticmethod
    def _compute_rects(masks: List[np.ndarray]) -> List[Rect]:
        """Compute bounding boxes for each mask region."""
        rects = []
        for mask in masks:
            points = (
                (0, 0, 0, 0)
                if cv2.findNonZero(mask) is None
                else cv2.boundingRect(cv2.findNonZero(mask))
            )
            rects.append(Rect(*points))
        return rects

    def _crop_masks(self) -> None:
        """Crop masks based on rect positions."""
        for i, rect in enumerate(self.rects):
            if rect.w == 0 or rect.h == 0:  # Skip empty regions
                continue
            self.masks[i] = self.masks[i][rect.numpy_slices()]

    def _translate_homographies(self) -> None:
        """Adjust homographies with translation based on rect positions."""
        # Find the minimum offset to translate all rects to start from (0,0)
        for i, rect in enumerate(self.rects):
            if rect.w == 0 or rect.h == 0:  # Skip empty regions
                continue
            T = np.array(
                [[1, 0, -rect.x], [0, 1, -rect.y], [0, 0, 1]], dtype=np.float32
            )
            self.homographies[i] = T @ self.homographies[i]

    @abstractmethod
    def _create_virtual_cam(self) -> Camera:
        """Create virtual camera that encompasses all input cameras."""

    @staticmethod
    def make_masks(
        cameras: List[Camera], homographies: List[np.ndarray], dsize: tuple[int, int]
    ) -> List[np.ndarray]:
        """Create binary masks for images."""
        return [
            cv2.warpPerspective(
                np.ones((cam.height, cam.width), dtype=np.uint8), H, dsize
            )
            for cam, H in zip(cameras, homographies)
        ]

    @staticmethod
    def warp_images(
        images: List[np.ndarray],
        homographies: List[np.ndarray],
        rects: List[Rect],
    ) -> List[np.ndarray]:
        """Warp images and create masks."""
        return [
            cv2.warpPerspective(img, H, rect.size, borderMode=cv2.BORDER_REPLICATE)
            for img, H, rect in zip(images, homographies, rects)
        ]

    @staticmethod
    def compensate_exposure(
        images: List[np.ndarray],
        masks: List[np.ndarray],
        rects: List[Rect],
    ) -> List[np.ndarray]:
        """Apply exposure compensation."""
        comp = cv2.detail.ExposureCompensator.createDefault(
            cv2.detail.ExposureCompensator_GAIN
        )
        comp.feed([rect.corner for rect in rects], images, masks)  # type: ignore

        compensated = []
        for i, (img, mask, rect) in enumerate(zip(images, masks, rects)):
            compensated_img = img.copy()
            comp.apply(i, rect.corner, compensated_img, mask)
            compensated.append(compensated_img)
        return compensated

    @staticmethod
    def blend_images(
        blender: cv2.detail.FeatherBlender,
        images: List[np.ndarray],
        masks: List[np.ndarray],
        rects: List[Rect],
        dsize: tuple[int, int],
    ) -> np.ndarray:
        """Blend images using OpenCV's FeatherBlender."""

        def _convert_to_3ch(img: np.ndarray) -> np.ndarray:
            if img.ndim < _NDIM_3C:
                return np.repeat(img[..., None], _NDIM_3C, axis=-1)
            return img

        def _safe_convert_to_int16(img: np.ndarray) -> np.ndarray:
            """Safely convert image to int16 format for FeatherBlender."""
            if img.dtype == np.uint16:
                # Scale uint16 (0-65535) to int16 range (-32768 to 32767)
                # Use range 0-32767 to avoid negative values
                img_scaled = (img / 2).astype(np.int16)
            else:
                # For other types, convert directly
                img_scaled = img.astype(np.int16)
            return img_scaled

        def _convert_from_int16(
            result: np.ndarray, original_dtype: np.dtype
        ) -> np.ndarray:
            """Convert result back from int16 to original dtype."""
            if original_dtype == np.uint16:
                # Scale back from int16 range to uint16
                result = (result * 2).astype(np.uint16)
            else:
                result = result.astype(original_dtype)
            return result

        # Prepare the blender with destination region
        dst_roi = (0, 0, dsize[0], dsize[1])  # (x, y, w, h) - OpenCV convention
        blender.prepare(dst_roi)

        # Feed all images and masks using pre-computed regions
        for img, mask, rect in zip(images, masks, rects):
            if rect.w == 0 or rect.h == 0:  # Skip empty regions
                continue

            # Convert to required format and feed
            img_3ch = _convert_to_3ch(img)
            img_16s = _safe_convert_to_int16(img_3ch)
            blender.feed(img_16s, mask, rect.corner)

        # Blend and return result
        result, _ = blender.blend(None, None)  # type: ignore
        result = result[..., 0] if images[0].ndim < _NDIM_3C else result

        # Convert back to original dtype
        original_dtype = images[0].dtype
        result = _convert_from_int16(result, original_dtype)
        return result

    def stitch(self, images: List[np.ndarray]) -> np.ndarray:
        """Stitch images together."""
        warped_images = self.warp_images(images, self.homographies, self.rects)
        warped_images = self.compensate_exposure(warped_images, self.masks, self.rects)
        return self.blend_images(
            self.blender, warped_images, self.masks, self.rects, self.virtual_cam.size
        )

    def __call__(self, images: List[np.ndarray]) -> np.ndarray:
        """Stitch images together."""
        return self.stitch(images)


class HorizontalStitcher(ImageStitcher):
    """Stitch cameras arranged horizontally (left-to-right)."""

    def _create_virtual_cam(self) -> Camera:
        # Concatenate all cameras horizontally
        virtual_cam = self.cameras[0]
        for cam in self.cameras[1:]:
            virtual_cam = Camera.hconcat(virtual_cam, cam)

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


class GridStitcher(ImageStitcher):
    """Stitch cameras arranged in a 2D grid."""

    def __init__(self, cameras: List[Camera], rows: int, cols: int) -> None:
        """Create a grid stitcher."""
        self.rows, self.cols = rows, cols
        if len(cameras) != rows * cols:
            raise ValueError(f"Expected {rows * cols} cameras, got {len(cameras)}")
        super().__init__(cameras)

    def _create_virtual_cam(self) -> Camera:
        # Build grid row by row
        grid_rows = []
        for r in range(self.rows):
            row_start = r * self.cols
            row_cameras = self.cameras[row_start : row_start + self.cols]

            # Concatenate horizontally
            row_cam = row_cameras[0]
            for cam in row_cameras[1:]:
                row_cam = Camera.hconcat(row_cam, cam)
            grid_rows.append(row_cam)

        # Concatenate vertically
        result = grid_rows[0]
        for row_cam in grid_rows[1:]:
            result = Camera.vconcat(result, row_cam)

        return result


# Convenience aliases
class LeftRightStitcher(HorizontalStitcher):
    """Stitch cameras arranged horizontally (left-to-right)."""

    def __init__(self, left_camera: Camera, right_camera: Camera) -> None:
        """Create a left-right stitcher."""
        super().__init__([left_camera, right_camera])
        self.left_camera = left_camera
        self.right_camera = right_camera
