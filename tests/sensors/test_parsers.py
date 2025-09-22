"""Tests for sensor calibration parsers."""

from pathlib import Path

import numpy as np
import pytest

import nextcv as cvx


class TestCalibrationInfo:
    """Test CalibrationInfo dataclass."""

    def test_from_dict(self):
        """Test creating CalibrationInfo from dictionary."""
        data = {
            "setup_date": "2025-07-29 15:21:23.854239",
            "json_version": 3,
            "calibrated_by": "NK",
            "camera_calibration_version": 2,
            "imu_calibration_version": 1,
        }

        info = cvx.sensors.CalibrationInfo.from_dict(data)

        assert info.json_version == 3
        assert info.calibrated_by == "NK"
        assert info.camera_calibration_version == 2
        assert info.imu_calibration_version == 1

        # Check that setup_date is parsed correctly
        assert info.setup_date.year == 2025
        assert info.setup_date.month == 7
        assert info.setup_date.day == 29
        assert info.setup_date.hour == 15
        assert info.setup_date.minute == 21
        assert info.setup_date.second == 23

    def test_from_dict_invalid_date(self):
        """Test CalibrationInfo with invalid date format raises exception."""
        data = {
            "setup_date": "invalid-date-format",
            "json_version": 1,
            "calibrated_by": "Test",
            "camera_calibration_version": 1,
            "imu_calibration_version": 1,
        }

        with pytest.raises(ValueError, match="Invalid isoformat string"):
            cvx.sensors.CalibrationInfo.from_dict(data)

    def test_from_dict_missing_date(self):
        """Test CalibrationInfo with missing date raises exception."""
        data = {
            "json_version": 1,
            "calibrated_by": "Test",
            "camera_calibration_version": 1,
            "imu_calibration_version": 1,
        }

        with pytest.raises(ValueError, match="Invalid isoformat string"):
            cvx.sensors.CalibrationInfo.from_dict(data)


class TestCalibrationData:
    """Test CalibrationData parser."""

    def test_from_json(self):
        """Test parsing calibration data from JSON file."""
        # Get the path to the test fixture
        fixture_path = (
            Path(__file__).parent.parent / "fixtures" / "watchkeeper_sensors.json"
        )

        # Parse the calibration data
        calibration = cvx.sensors.CalibrationData.from_json(fixture_path)

        # Check that we have the expected structure
        assert calibration.calibration_info.setup_date is not None
        assert calibration.calibration_info.json_version == 3
        assert calibration.calibration_info.calibrated_by == "NK"
        assert calibration.calibration_info.camera_calibration_version == 2
        assert calibration.calibration_info.imu_calibration_version == 1

        # Check that we have the expected cameras
        expected_cameras = {"t1", "t2", "rgb1"}
        assert set(calibration.cameras.keys()) == expected_cameras

    def test_get_camera(self):
        """Test converting camera data to Camera objects."""
        fixture_path = (
            Path(__file__).parent.parent / "fixtures" / "watchkeeper_sensors.json"
        )
        calibration = cvx.sensors.CalibrationData.from_json(fixture_path)

        # Test camera t1
        camera_t1 = calibration.get_camera("t1")
        assert camera_t1.fx == 1113.0780414201542
        assert camera_t1.fy == 1113.313551958476
        assert camera_t1.cx == 319.5
        assert camera_t1.cy == 255.5
        assert camera_t1.roll == -0.518605797686487
        assert camera_t1.pitch == 0.7992500957842668
        assert camera_t1.yaw == -11.45230705981723

        # Test camera t2
        camera_t2 = calibration.get_camera("t2")
        assert camera_t2.fx == 1110.8132591637204
        assert camera_t2.fy == 1111.272282345
        assert camera_t2.cx == 319.5
        assert camera_t2.cy == 255.5
        assert camera_t2.roll == 0.006156470523271985
        assert camera_t2.pitch == 0.7279144229902477
        assert camera_t2.yaw == 11.023918606114886

        # Test camera rgb1
        camera_rgb1 = calibration.get_camera("rgb1")
        assert camera_rgb1.fx == 1904.2649866903312
        assert camera_rgb1.fy == 1903.8527451625173
        assert camera_rgb1.cx == 1879.347047587519
        assert camera_rgb1.cy == 1129.052166343516
        assert camera_rgb1.roll == -0.4682761908214822
        assert camera_rgb1.pitch == 0.36743516001099635
        assert camera_rgb1.yaw == 0.0016027099197843011

    def test_camera_matrices(self):
        """Test that camera matrices are computed correctly."""
        fixture_path = (
            Path(__file__).parent.parent / "fixtures" / "watchkeeper_sensors.json"
        )
        calibration = cvx.sensors.CalibrationData.from_json(fixture_path)

        camera = calibration.get_camera("t1")

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
        fixture_path = (
            Path(__file__).parent.parent / "fixtures" / "watchkeeper_sensors.json"
        )
        calibration = cvx.sensors.CalibrationData.from_json(fixture_path)

        with pytest.raises(KeyError):
            calibration.get_camera("nonexistent_camera")
