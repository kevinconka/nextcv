"""Tests for sensor calibration parsers."""

from pathlib import Path

import numpy as np
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

    def test_camera_objects(self):
        """Test converting camera data to Camera objects."""
        fixture_path = Path(__file__).parent.parent / "fixtures" / "wk1280_sensors.json"
        calibration = cvx.sensors.CalibrationData.from_json(fixture_path)

        assert isinstance(calibration.cameras["t1"], cvx.sensors.Camera)
        assert isinstance(calibration.cameras["t2"], cvx.sensors.Camera)
        assert isinstance(calibration.cameras["rgb1"], cvx.sensors.Camera)

    def test_camera_matrices(self):
        """Test that camera matrices are computed correctly."""
        fixture_path = Path(__file__).parent.parent / "fixtures" / "wk1280_sensors.json"
        calibration = cvx.sensors.CalibrationData.from_json(fixture_path)

        camera = calibration.cameras["t1"]

        # Test intrinsics matrix
        K = camera.K
        assert K.shape == (3, 3)
        assert K[0, 0] == camera.fx  # fx
        assert K[1, 1] == camera.fy  # fy
        assert K[0, 2] == camera.cx  # cx
        assert K[1, 2] == camera.cy  # cy
        assert K[2, 2] == 1.0  # bottom-right should be 1

        # Test rotation matrix
        R = camera.R
        assert R.shape == (3, 3)
        # Rotation matrix should be orthogonal (R @ R.T = I)
        assert abs((R @ R.T - np.eye(3)).max()) < 1e-10

    def test_invalid_camera_id(self):
        """Test that invalid camera ID raises appropriate error."""
        fixture_path = Path(__file__).parent.parent / "fixtures" / "wk1280_sensors.json"
        calibration = cvx.sensors.CalibrationData.from_json(fixture_path)

        with pytest.raises(KeyError):
            _ = calibration.cameras["nonexistent_camera"]
