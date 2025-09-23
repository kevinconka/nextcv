"""Tests for sensor calibration parsers."""

from pathlib import Path

import pytest

import nextcv as cvx


class TestCalibrationData:
    """Test CalibrationData parser."""

    def test_from_json(self):
        """Test parsing calibration data from JSON file."""
        # Get the path to the test fixture
        fixture_path = Path(__file__).parent.parent / "fixtures" / "wk1280_sensors.json"

        # Parse the calibration data
        calibration = cvx.sensors.CalibrationData.from_json(fixture_path)

        # Check that we have the expected cameras
        expected_cameras = {"t1", "t2", "rgb1"}
        assert set(calibration.cameras.keys()) == expected_cameras
        assert all(
            isinstance(camera, cvx.sensors.Camera)
            for camera in calibration.cameras.values()
        )

    def test_camera_resolution_parsing(self):
        """Test that camera resolution is parsed correctly from JSON."""
        fixture_path = Path(__file__).parent.parent / "fixtures" / "wk1280_sensors.json"
        calibration = cvx.sensors.CalibrationData.from_json(fixture_path)

        # Test thermal cameras (640x512)
        t1 = calibration.cameras["t1"]
        t2 = calibration.cameras["t2"]
        assert t1.width == 640 and t1.height == 512
        assert t2.width == 640 and t2.height == 512

        # Test RGB camera (3840x2160)
        rgb1 = calibration.cameras["rgb1"]
        assert rgb1.width == 3840 and rgb1.height == 2160

    def test_invalid_camera_id(self):
        """Test that invalid camera ID raises appropriate error."""
        fixture_path = Path(__file__).parent.parent / "fixtures" / "wk1280_sensors.json"
        calibration = cvx.sensors.CalibrationData.from_json(fixture_path)

        with pytest.raises(KeyError):
            _ = calibration.cameras["nonexistent_camera"]
