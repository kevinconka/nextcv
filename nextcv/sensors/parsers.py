"""Parsers for sensor calibration data."""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from .camera import Camera


@dataclass
class CalibrationInfo:
    """Calibration metadata information."""

    setup_date: datetime
    json_version: int
    calibrated_by: str
    camera_calibration_version: int
    imu_calibration_version: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CalibrationInfo":
        """Create CalibrationInfo from dictionary data.

        Args:
            data: Dictionary containing calibration info

        Returns:
            CalibrationInfo instance with parsed setup_date
        """
        # Parse the setup_date string to datetime
        setup_date_str = data.get("setup_date", "")
        # Parse the format: "2025-07-29 15:21:23.854239"
        setup_date = datetime.fromisoformat(setup_date_str)

        return cls(
            setup_date=setup_date,
            json_version=data.get("json_version", 0),
            calibrated_by=data.get("calibrated_by", ""),
            camera_calibration_version=data.get("camera_calibration_version", 0),
            imu_calibration_version=data.get("imu_calibration_version", 0),
        )


@dataclass
class CalibrationData:
    """Simple calibration data parser without heavy dependencies."""

    calibration_info: CalibrationInfo
    cameras: Dict[str, Dict[str, Any]]

    @classmethod
    def from_json(cls, file_path: str | Path) -> "CalibrationData":
        """Parse calibration data from JSON file.

        Args:
            file_path: Path to the JSON calibration file

        Returns:
            Parsed calibration data
        """
        with Path(file_path).open("r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(
            calibration_info=CalibrationInfo.from_dict(
                data.get("calibration_info", {})
            ),
            cameras=data.get("cameras", {}),
        )

    def get_camera(self, camera_id: str) -> Camera:
        """Convert camera data to Camera object.

        Args:
            camera_id: ID of the camera (e.g., "t1", "t2", "rgb1")

        Returns:
            Camera object with intrinsics and pose
        """
        camera_data = self.cameras[camera_id]

        # Extract values from nested structure
        def get_value(key: str) -> float:
            return camera_data.get(key, {}).get("value", 0.0)

        return Camera(
            fx=get_value("focal_length_x"),
            fy=get_value("focal_length_y"),
            cx=get_value("center_x"),
            cy=get_value("center_y"),
            roll=get_value("roll"),
            pitch=get_value("pitch"),
            yaw=get_value("yaw"),
        )
