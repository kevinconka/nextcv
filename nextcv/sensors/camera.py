"""Sensor representation and manipulation utilities."""

from typing import Any, Dict

import numpy as np
from pydantic import BaseModel, Field
from scipy.spatial.transform import Rotation as R


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

    @classmethod
    def from_dict(
        cls,
        data: Dict[str, Any],
    ) -> "Camera":
        """Create a Camera instance from intrinsics and pose dictionaries.

        Args:
            data: Dictionary with keys "fx", "fy", "cx", "cy", "width", "height",
                "roll", "pitch", "yaw"

        Returns:
            Camera instance
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

    def compute_homography_to(
        self,
        target: "Camera",
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

    def crop(self, left: float, top: float, right: float, bottom: float) -> "Camera":
        """Return a new Camera cropped by margins (left, top, right, bottom)."""
        if any(v < 0 for v in (left, top, right, bottom)):
            raise ValueError("Margins must be >= 0.")
        if left + right >= self.width or top + bottom >= self.height:
            raise ValueError("Crop exceeds image bounds.")

        # Projective translation
        T_crop = np.array(
            [[1.0, 0.0, -left], [0.0, 1.0, -top], [0.0, 0.0, 1.0]], dtype=np.float64
        )

        Kp = T_crop @ self.K
        fxp, fyp, cxp, cyp = Kp[0, 0], Kp[1, 1], Kp[0, 2], Kp[1, 2]

        new_w = int(self.width - left - right)
        new_h = int(self.height - top - bottom)

        return self.copy(
            update={
                "width": new_w,
                "height": new_h,
                "fx": fxp,
                "fy": fyp,
                "cx": cxp,
                "cy": cyp,
            }
        )
