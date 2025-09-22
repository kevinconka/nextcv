"""Sensor representation and manipulation utilities."""

from dataclasses import dataclass, field
from typing import Dict

import numpy as np
from scipy.spatial.transform import Rotation as R


@dataclass
class Camera:
    """Represents a camera with its intrinsics and pose information."""

    fx: float = field(metadata={"description": "Focal length along x-axis in pixels"})
    fy: float = field(metadata={"description": "Focal length along y-axis in pixels"})
    cx: float = field(metadata={"description": "Principal point x in pixels"})
    cy: float = field(metadata={"description": "Principal point y in pixels"})
    roll: float = field(metadata={"description": "Camera roll in degrees"})
    pitch: float = field(metadata={"description": "Camera pitch in degrees"})
    yaw: float = field(metadata={"description": "Camera yaw in degrees"})

    @classmethod
    def from_dict(
        cls,
        intrinsics: Dict[str, float],
        pose: Dict[str, float],
    ) -> "Camera":
        """Create a Camera instance from intrinsics and pose dictionaries.

        Args:
            intrinsics: Dictionary with keys "fx", "fy", "cx", "cy"
            pose: Dictionary with keys "roll", "pitch", "yaw" in degrees

        Returns:
            Camera instance
        """
        return cls(
            fx=intrinsics["fx"],
            fy=intrinsics["fy"],
            cx=intrinsics["cx"],
            cy=intrinsics["cy"],
            roll=pose["roll"],
            pitch=pose["pitch"],
            yaw=pose["yaw"],
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
