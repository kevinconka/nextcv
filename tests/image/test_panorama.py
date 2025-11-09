"""Test panorama stitching with real-world camera arrangement."""

from typing import List

import numpy as np
import pytest

from nextcv.image.stitching import PanoramaStitcher
from nextcv.sensors import PinholeCamera


def compute_focal_length_from_fov(fov_deg: float, resolution: int) -> float:
    """Compute focal length from field of view and resolution.

    Args:
        fov_deg: Field of view in degrees
        resolution: Image dimension (width or height) in pixels

    Returns:
        Focal length in pixels
    """
    fov_rad = np.deg2rad(fov_deg)
    return resolution / (2 * np.tan(fov_rad / 2))


class TestPanoramaRealWorld:
    """Test panorama stitcher with real camera arrangement."""

    yaws = list(range(0, 360, 24))
    pitches = [-17.0, 0.0, 18.0]
    hfov = 32.0
    vfov = 25.839818081545385
    width = 640
    height = 512
    cx = (width - 1) / 2
    cy = (height - 1) / 2

    @pytest.fixture
    def cameras(self):
        """Create cameras with specified arrangement.

        - Yaw: 0, 12, 24, ..., 348 degrees (30 cameras)
        - Pitch: -17, 0, 18 degrees (3 rows)
        - FOV: 32° x 25.84°
        - Resolution: 640 x 512
        - Principal point: (319.5, 255.5)
        """
        # Compute focal lengths from FOV
        fx = compute_focal_length_from_fov(self.hfov, self.width)
        fy = compute_focal_length_from_fov(self.vfov, self.height)

        cameras = [
            PinholeCamera(
                width=self.width,
                height=self.height,
                fx=fx,
                fy=fy,
                cx=self.cx,
                cy=self.cy,
                roll=0,
                pitch=pitch,
                yaw=yaw,
            )
            for pitch in self.pitches
            for yaw in self.yaws
        ]

        return cameras

    def test_camera_count(self, cameras: List[PinholeCamera]):
        """Verify correct number of cameras."""
        # 30 yaw positions × 3 pitch positions = 90 cameras
        assert len(cameras) == 45

    def test_camera_fov(self, cameras: List[PinholeCamera]):
        """Verify cameras have correct FOV."""
        for cam in cameras:
            assert cam.hfov == pytest.approx(32.0, abs=0.1)
            assert cam.vfov == pytest.approx(25.84, abs=0.1)

    def test_panorama_creation(self, cameras: List[PinholeCamera]):
        """Test creating panorama from camera arrangement."""
        stitcher = PanoramaStitcher(cameras)
        vcam = stitcher.virtual_camera

        # Should detect full 360° coverage
        assert vcam.hfov == pytest.approx(360.0, abs=0.1)

        # Vertical FOV should cover all 3 rows
        # Rows at -17°, 0°, +18° with ~25.84° vfov each
        # Should be roughly: (18 + 25.84/2) - (-17 - 25.84/2) ≈ 60.76°
        assert 50 < vcam.vfov < 80  # Reasonable range

        # Center should be at average pitch
        expected_center_pitch = np.mean(self.pitches)
        assert vcam.pitch == pytest.approx(expected_center_pitch, abs=5.0)

        # verify 360 degree coverage
        assert stitcher.virtual_camera.hfov == pytest.approx(360.0, abs=0.1)

    def test_panorama_stitching(self, cameras: List[PinholeCamera]):
        """Test stitching images from all cameras."""
        stitcher = PanoramaStitcher(cameras)

        # Create test images (one per camera)
        images = [
            np.full((self.height, self.width), 10000, dtype=np.uint16)
            for _ in range(len(cameras))
        ]

        # Stitch
        panorama = stitcher(images)

        # Verify output
        assert panorama.shape[0] == stitcher.virtual_camera.height
        assert panorama.shape[1] == stitcher.virtual_camera.width
        assert panorama.dtype == np.uint16
