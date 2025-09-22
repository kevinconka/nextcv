"""Sensor representation and manipulation utilities."""

from typing import Any, Dict

import numpy as np
from pydantic import BaseModel, Field
from scipy.spatial.transform import Rotation as R


class Camera(BaseModel):
    """Represents a camera with its intrinsics and pose information."""

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
            data: Dictionary with keys "fx", "fy", "cx", "cy", "roll", "pitch", "yaw"

        Returns:
            Camera instance
        """
        return cls(
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
