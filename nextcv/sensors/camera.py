"""Sensor representation and manipulation utilities."""

from typing import Any, Dict, Tuple, Type, TypeVar

import numpy as np
from pydantic import BaseModel, Field, validator
from scipy.spatial.transform import Rotation as R

T = TypeVar("T", bound="Camera")


class Camera(BaseModel):
    """Represents a camera with its intrinsics, pose, and image resolution."""

    width: int = Field(description="Image width in pixels")
    height: int = Field(description="Image height in pixels")
    fx: float = Field(description="Focal length along x-axis in pixels")
    fy: float = Field(description="Focal length along y-axis in pixels")
    cx: float = Field(description="Principal point x-coordinate in pixels")
    cy: float = Field(description="Principal point y-coordinate in pixels")
    roll: float = Field(
        description="Camera roll angle in degrees (rotation around z-axis)"
    )
    pitch: float = Field(
        description="Camera pitch angle in degrees (rotation around x-axis)"
    )
    yaw: float = Field(
        description="Camera yaw angle in degrees (rotation around y-axis)"
    )

    # run after init/validation
    @validator("width", "height", allow_reuse=True)
    def must_be_even(cls, v: int) -> int:  # noqa: N805 # pylint: disable=no-self-argument
        """Ensure width and height are positive integers."""
        if v % 2 != 0:
            raise ValueError("must be even")
        return v

    @classmethod
    def from_dict(
        cls: Type[T],
        data: Dict[str, Any],
    ) -> T:
        """Create a Camera instance from intrinsics and pose dictionaries.

        Args:
            data: Dictionary with keys "fx", "fy", "cx", "cy", "width", "height",
                "roll", "pitch", "yaw"

        Returns:
            Camera instance of the correct subclass type
        """
        return cls(
            width=data["width"],
            height=data["height"],
            fx=data["fx"],
            fy=data["fy"],
            cx=data["cx"],
            cy=data["cy"],
            roll=data["roll"],
            pitch=data["pitch"],
            yaw=data["yaw"],
        )

    @property
    def size(self) -> Tuple[int, int]:
        """Get the camera size as an opencv-compatible tuple of width and height."""
        return self.width, self.height

    def maps_from(
        self, src: "Camera", neg_focal_length: bool = True
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Create pixel maps to warp images from source camera to this camera.

        Returns:
            Tuple of (mapx, mapy) arrays for use with cv2.remap()
        """
        raise NotImplementedError("Subclasses must implement get_warping_maps")


class PinholeCamera(Camera):
    """Represents a pinhole camera with its intrinsics and pose."""

    @property
    def hfov(self) -> float:
        """Get the horizontal field of view in degrees."""
        return np.rad2deg(2 * np.arctan(self.width / (2 * self.fx)))

    @property
    def vfov(self) -> float:
        """Get the vertical field of view in degrees."""
        return np.rad2deg(2 * np.arctan(self.height / (2 * self.fy)))

    @property
    def K(self) -> np.ndarray:
        """Get the camera intrinsics matrix."""
        return np.array(
            [
                [self.fx, 0, self.cx],
                [0, self.fy, self.cy],
                [0, 0, 1],
            ]
        )

    @property
    def R(self) -> np.ndarray:
        """Get the camera rotation matrix from Euler angles with pinhole convention.

        The pinhole convention is:
        - x is right
        - y is down
        - z is forward
        """
        return R.from_euler(
            "zxy", [self.roll, self.pitch, self.yaw], degrees=True
        ).as_matrix()

    def crop(
        self,
        left: float,
        top: float,
        right: float,
        bottom: float,
        force_even: bool = True,
    ) -> "PinholeCamera":
        """Return a new PinholeCamera cropped by margins (left, top, right, bottom)."""
        if any(v < 0 for v in (left, top, right, bottom)):
            raise ValueError("Margins must be >= 0.")

        new_w = int(self.width - left - right)
        new_h = int(self.height - top - bottom)
        if any(v <= 0 for v in (new_w, new_h)):
            raise ValueError("Crop exceeds image bounds.")

        # force even width and height
        if force_even:
            new_w = new_w // 2 * 2
            new_h = new_h // 2 * 2

        return PinholeCamera(
            width=new_w,
            height=new_h,
            fx=self.fx,
            fy=self.fy,
            cx=self.cx - left,  # shift principal point to the left
            cy=self.cy - top,  # shift principal point to the top
            roll=self.roll,
            pitch=self.pitch,
            yaw=self.yaw,
        )

    @classmethod
    def hconcat(cls, left: "PinholeCamera", right: "PinholeCamera") -> "PinholeCamera":
        """Create a virtual camera by concatenating left and right cams horizontally."""
        assert (left.height, left.width) == (
            right.height,
            right.width,
        ), "Left and right cameras must have the same resolution."
        return cls(
            width=left.width + right.width,
            height=max(left.height, right.height),
            fx=(left.fx + right.fx) / 2,
            fy=(left.fy + right.fy) / 2,
            cx=left.width + (right.cx - left.cx) / 2,  # Shift principal point
            cy=(left.height - 1) / 2,
            roll=0.0,
            pitch=(left.pitch + right.pitch) / 2,
            yaw=0.0,
        )

    @classmethod
    def vconcat(cls, top: "PinholeCamera", bottom: "PinholeCamera") -> "PinholeCamera":
        """Create a virtual camera by concatenating top and bottom cams vertically."""
        assert (top.width, top.height) == (
            bottom.width,
            bottom.height,
        ), "Top and bottom cameras must have the same resolution."
        return cls(
            width=max(top.width, bottom.width),
            height=top.height + bottom.height,
            fx=(top.fx + bottom.fx) / 2,
            fy=(top.fy + bottom.fy) / 2,
            cx=(top.cx + bottom.cx) / 2,
            cy=top.height + (bottom.cy - top.cy) / 2,  # Shift principal point
            roll=0.0,
            pitch=0.0,
            yaw=(top.yaw + bottom.yaw) / 2,
        )

    def compute_homography_to(
        self,
        target: "PinholeCamera",
        neg_focal_length: bool = True,
    ) -> np.ndarray:
        """Compute homography matrix that maps points from this camera to target camera.

        Args:
            target: Target camera to compute homography to
            neg_focal_length: Whether to negate the focal length

        Returns:
            Homography matrix that transforms points from this camera to target camera
        """
        # Get camera matrices
        R_source = self.R
        R_target = target.R
        K_source = self.K
        K_target = target.K

        if neg_focal_length:
            K_source = self.K @ np.diag([-1.0, -1.0, 1.0])
            K_target = target.K @ np.diag([-1.0, -1.0, 1.0])

        # Compute the homography matrix
        H = K_target @ np.linalg.inv(R_target) @ R_source @ np.linalg.inv(K_source)
        return H

    def maps_from(
        self, src: "PinholeCamera", neg_focal_length: bool = True
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Create remapping maps from source camera to this camera."""
        # src -> self homography (3x3)
        H = src.compute_homography_to(self, neg_focal_length).astype(np.float32)
        Hinv = np.linalg.inv(H).astype(np.float32)  # we need dst(self)->src map

        # Meshgrid of target pixel centers (x right, y down)
        xs, ys = np.meshgrid(
            np.arange(self.width, dtype=np.float32),
            np.arange(self.height, dtype=np.float32),
            indexing="xy",
        )

        # Homogeneous coords in target → map back into source
        ones = np.ones_like(xs, dtype=np.float32)
        dst_h = np.stack((xs, ys, ones), axis=-1)  # (H,W,3)
        src_h = dst_h @ Hinv.T  # (H,W,3)
        src_h[..., 2] = np.clip(src_h[..., 2], 1e-8, None)

        uv = src_h[..., :2] / src_h[..., 2:3]  # (H,W,2)
        mapx = np.ascontiguousarray(uv[..., 0], dtype=np.float32)
        mapy = np.ascontiguousarray(uv[..., 1], dtype=np.float32)
        return mapx, mapy


class EquirectangularCamera(Camera):
    """Equirectangular projection camera for 360° panoramas."""

    hfov: float = Field(description="Horizontal field of view in degrees")
    vfov: float = Field(description="Vertical field of view in degrees")
    fx: float = Field(default=np.nan, exclude=True)
    fy: float = Field(default=np.nan, exclude=True)
    cx: float = Field(default=np.nan, exclude=True)
    cy: float = Field(default=np.nan, exclude=True)

    @property
    def R(self) -> np.ndarray:
        """Get the camera rotation matrix from Euler angles.

        Uses same convention as PinholeCamera:
        - x is right
        - y is down
        - z is forward
        """
        return R.from_euler(
            "zxy", [self.roll, self.pitch, self.yaw], degrees=True
        ).as_matrix()

    def maps_from(
        self, src: "PinholeCamera", neg_focal_length: bool = True
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Create remapping matching the simple angular implementation.

        WARNING: This ignores proper camera geometry (R, K matrices).
        Only uses direct angular offset mapping.
        """
        # Create pixel grid for equirectangular image
        xs, ys = np.meshgrid(
            np.arange(self.width, dtype=np.float32),
            np.arange(self.height, dtype=np.float32),
            indexing="xy",
        )

        # Pure angular mapping: panorama pixel → world angles
        pixel_angle_h = self.hfov / self.width  # degrees per pixel
        pixel_angle_v = self.vfov / self.height

        # ===== SIMPLE CENTER-TO-CENTER MAPPING =====

        # HORIZONTAL: Panorama angle → offset from source center → source pixel
        # 1. Panorama pixel → world angle (0° at center)
        pan = (xs - self.width * 0.5) * pixel_angle_h + self.yaw
        pan = np.mod(pan, 360.0)  # Normalize to [0, 360) using modulo

        # 2. Angular offset from source center (shortest angular distance)
        pan_offset = np.mod(pan - src.yaw + 180.0, 360.0) - 180.0

        # 3. Convert to source pixel (center + offset)
        src_pixel_angle_h = src.hfov / src.width
        mapx = (src.width * 0.5 + pan_offset / src_pixel_angle_h).astype(np.float32)

        # VERTICAL: Panorama angle → offset from source center → source pixel
        # 1. Panorama pixel → world angle (0 at top, increases downward)
        tilt = self.pitch + self.vfov / 2 - ys * pixel_angle_v

        # 2. Angular offset from source center
        tilt_offset = tilt - src.pitch

        # 3. Convert to source pixel (center - offset, because y points down)
        src_pixel_angle_v = src.vfov / src.height
        mapy = (src.height / 2 - tilt_offset / src_pixel_angle_v).astype(np.float32)

        return np.ascontiguousarray(mapx), np.ascontiguousarray(mapy)
