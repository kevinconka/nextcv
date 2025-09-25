"""Generalized image stitching framework.

Simple, extensible architecture for stitching images from multiple cameras.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

import cv2
import numpy as np

from nextcv.sensors.camera import PinholeCamera as Camera

_3C = 3


class ImageStitcher(ABC):
    """Abstract base class for image stitchers."""

    def __init__(self, cameras: List[Camera]) -> None:
        """Create a base stitcher.

        Args:
            cameras: List of cameras to stitch
        """
        self.cameras = cameras
        self.virtual_cam = self._create_virtual_cam()
        self.homographies = [
            cam.compute_homography_to(self.virtual_cam) for cam in self.cameras
        ]
        self.maps = self.make_maps(self.homographies, self.virtual_cam.size)
        self.masks = self.make_masks(
            self.cameras, self.homographies, self.virtual_cam.size
        )
        self.weights = self.make_feather_weights(self.masks)

    @abstractmethod
    def _create_virtual_cam(self) -> Camera:
        """Create virtual camera that encompasses all input cameras."""

    @staticmethod
    def make_maps(
        homographies: List[np.ndarray], dsize: tuple[int, int]
    ) -> List[Tuple[np.ndarray, np.ndarray]]:
        """Create maps for cv2.remap."""
        # inverse map: for each (x_d, y_d) in destination, find source (x_s, y_s)
        maps = []
        for H in homographies:
            xs, ys = np.meshgrid(
                np.arange(dsize[0], dtype=np.float32),
                np.arange(dsize[1], dtype=np.float32),
            )
            ones = np.ones_like(xs)
            dst_pts = np.stack([xs, ys, ones], axis=-1)  # (H, W, 3)
            src_pts = dst_pts @ np.linalg.inv(H).T  # homogeneous
            src_pts = src_pts[..., :2] / src_pts[..., 2:3]
            mapx, mapy = (
                src_pts[..., 0].astype(np.float32),
                src_pts[..., 1].astype(np.float32),
            )
            maps.append((mapx, mapy))
        return maps

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
    def make_feather_weights(masks: List[np.ndarray]) -> List[np.ndarray]:
        """Create masks for images."""
        weights = [
            cv2.distanceTransform(mask, cv2.DIST_L2, 3).astype(np.float32)
            for mask in masks
        ]
        W = np.stack(weights, axis=0)
        W = W / np.clip(np.sum(W, axis=0), 1e-6, None)
        return list(W)

    @staticmethod
    def warp_images(
        images: List[np.ndarray],
        homographies: List[np.ndarray],
        dsize: tuple[int, int],
    ) -> List[np.ndarray]:
        """Warp images and create masks."""
        return [
            cv2.warpPerspective(img, H, dsize) for img, H in zip(images, homographies)
        ]

    @staticmethod
    def warp_images_remap(
        images: List[np.ndarray],
        maps: List[Tuple[np.ndarray, np.ndarray]],
    ) -> List[np.ndarray]:
        """Warp images using cv2.remap."""
        return [
            cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
            for img, (mapx, mapy) in zip(images, maps)
        ]

    @staticmethod
    def compensate_exposure(
        images: List[np.ndarray], masks: List[np.ndarray]
    ) -> List[np.ndarray]:
        """Apply exposure compensation."""
        comp = cv2.detail.ExposureCompensator.createDefault(
            cv2.detail.ExposureCompensator_GAIN
        )
        corners = [(0, 0)] * len(images)
        comp.feed(corners, images, masks)  # type: ignore

        compensated = []
        for i, (img, mask) in enumerate(zip(images, masks)):
            compensated_img = img.copy()
            comp.apply(i, (0, 0), compensated_img, mask)
            compensated.append(compensated_img)
        return compensated

    @staticmethod
    def blend_images(images: List[np.ndarray], weights: List[np.ndarray]) -> np.ndarray:
        """Blend images together."""
        imgs = np.stack(images, axis=0).astype(np.float32)  # [N,H,W,(C)]
        wgts = np.stack(weights, axis=0)
        if imgs.ndim == _3C + 1:  # color
            out = np.einsum("nhwc,nhwc->hwc", imgs, wgts[..., None])
        else:  # grayscale
            out = np.einsum("nhw,nhw->hw", imgs, wgts)
        return out.astype(images[0].dtype)

    def stitch(self, images: List[np.ndarray]) -> np.ndarray:
        """Stitch images together."""
        warped_images = self.warp_images_remap(images, self.maps)
        warped_images = self.compensate_exposure(warped_images, self.masks)
        return self.blend_images(warped_images, self.weights)

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
