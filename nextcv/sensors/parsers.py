"""Parsers for sensor calibration data."""

import json
from pathlib import Path
from typing import Dict, Union

from pydantic import BaseModel, Field

from .camera import PinholeCamera


class CalibrationData(BaseModel):
    """Simple calibration data parser without heavy dependencies."""

    cameras: Dict[str, PinholeCamera] = Field(
        description="Dictionary of cameras with their calibration data"
    )

    @classmethod
    def from_json(cls, file_path: Union[str, Path]) -> "CalibrationData":
        """Parse calibration data from JSON file.

        Args:
            file_path: Path to the JSON calibration file

        Returns:
            Parsed calibration data
        """
        with Path(file_path).open("r", encoding="utf-8") as f:
            data = json.load(f)

        return cls(
            cameras={
                camera_id: PinholeCamera.from_dict(
                    {
                        "width": camera_data["resolution"]["value"][0],
                        "height": camera_data["resolution"]["value"][1],
                        "fx": camera_data["focal_length_x"]["value"],
                        "fy": camera_data["focal_length_y"]["value"],
                        "cx": camera_data["center_x"]["value"],
                        "cy": camera_data["center_y"]["value"],
                        "roll": camera_data["roll"]["value"],
                        "pitch": camera_data["pitch"]["value"],
                        "yaw": camera_data["yaw"]["value"],
                    }
                )
                for camera_id, camera_data in data.get("cameras", {}).items()
            },
        )
