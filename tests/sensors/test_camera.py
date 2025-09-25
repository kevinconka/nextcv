"""Tests for Camera class."""

import numpy as np
import pytest

from nextcv.sensors import Camera, PinholeCamera


class TestCamera:
    """Test cases for Camera class."""

    def test_camera_creation(self):
        """Test basic camera creation."""
        camera = Camera(
            width=640,
            height=512,
            fx=1000.0,
            fy=1000.0,
            cx=320.0,
            cy=256.0,
            roll=0.0,
            pitch=0.0,
            yaw=0.0,
        )

        assert camera.width == 640
        assert camera.height == 512
        assert camera.fx == 1000.0
        assert camera.fy == 1000.0
        assert camera.cx == 320.0
        assert camera.cy == 256.0

    def test_camera_from_dict(self):
        """Test camera creation from dictionary."""
        data = {
            "width": 1280,
            "height": 720,
            "fx": 1500.0,
            "fy": 1500.0,
            "cx": 640.0,
            "cy": 360.0,
            "roll": 5.0,
            "pitch": -2.0,
            "yaw": 10.0,
        }

        camera = Camera.from_dict(data)

        assert camera.width == 1280
        assert camera.height == 720
        assert camera.fx == 1500.0
        assert camera.roll == 5.0
        assert camera.pitch == -2.0
        assert camera.yaw == 10.0


class TestPinholeCamera:
    """Test cases for PinholeCamera class."""

    camera = PinholeCamera(
        width=640,
        height=512,
        fx=1000.0,
        fy=1000.0,
        cx=320.0,
        cy=256.0,
        roll=0.0,
        pitch=0.0,
        yaw=0.0,
    )

    def test_intrinsics_matrix(self):
        """Test camera intrinsics matrix K."""
        K = self.camera.K
        expected_K = np.array(
            [
                [1000.0, 0.0, 320.0],
                [0.0, 1000.0, 256.0],
                [0.0, 0.0, 1.0],
            ]
        )

        np.testing.assert_array_equal(K, expected_K)

    def test_rotation_matrix(self):
        """Test camera rotation matrix R."""
        R = self.camera.R
        expected_R = np.eye(3)  # Identity matrix for zero rotation

        np.testing.assert_array_almost_equal(R, expected_R, decimal=10)

    def test_crop_method(self):
        """Test camera cropping functionality."""
        # Crop by 10 pixels on each side
        cropped = self.camera.crop(left=10, top=10, right=10, bottom=10)

        assert cropped.width == 620  # 640 - 10 - 10
        assert cropped.height == 492  # 512 - 10 - 10
        assert cropped.cx == 310.0  # 320 - 10
        assert cropped.cy == 246.0  # 256 - 10
        assert cropped.fx == 1000.0  # Should remain the same
        assert cropped.fy == 1000.0  # Should remain the same

    def test_crop_validation(self):
        """Test crop method validation."""
        # Test negative margins
        with pytest.raises(ValueError, match="Margins must be >= 0"):
            self.camera.crop(left=-1, top=0, right=0, bottom=0)

        # Test excessive cropping
        with pytest.raises(ValueError, match="Crop exceeds image bounds"):
            self.camera.crop(left=0, top=0, right=640, bottom=0)
