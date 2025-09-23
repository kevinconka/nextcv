"""Tests for image stitching functionality."""

import numpy as np
import pytest

import nextcv as cvx


class TestLRStitcher:
    """Test cases for LRStitcher class."""

    @pytest.fixture
    def stitcher(self):
        """Create a stitcher instance for testing."""
        # Use hardcoded camera values instead of fixture
        t1 = cvx.sensors.Camera(
            width=640,
            height=512,
            fx=1487.0897209580626,
            fy=1486.893999534694,
            cx=319.5,
            cy=255.5,
            roll=-0.6953680852913573,
            pitch=0.3175409097871985,
            yaw=10.942382806743069,
        )
        t2 = cvx.sensors.Camera(
            width=640,
            height=512,
            fx=1492.120223972608,
            fy=1492.126838008826,
            cx=319.5,
            cy=255.5,
            roll=-0.25389265482939055,
            pitch=0.7082357267631507,
            yaw=-11.468243408503717,
        )

        config = cvx.image.StitchingConfig(
            lower_threshold=15000, upper_threshold=28000, transition_mode="cosine"
        )
        return cvx.image.LRStitcher(left_camera=t1, right_camera=t2, config=config)

    def test_stitcher_initialization(self, stitcher: cvx.image.LRStitcher):
        """Test that stitcher initializes correctly."""
        assert stitcher is not None
        assert stitcher.virtual_camera is not None
        assert stitcher.virtual_camera.width > 0
        assert stitcher.virtual_camera.height > 0

    def test_stitching_blending_behavior(self, stitcher: cvx.image.LRStitcher):
        """Test that stitched values lie between input values (as requested by user)."""
        # Create left image with constant intensity
        left_img = np.full((512, 640), 16000, dtype=np.uint16)
        # Create right image with different constant intensity
        right_img = np.full((512, 640), 24000, dtype=np.uint16)

        # Stitch the images
        stitched = stitcher(left_img, right_img)

        # Verify output properties
        assert stitched.shape[0] == 473  # Height is cropped to overlapping region
        assert stitched.shape[1] > 640  # Width should be larger (stitched)
        assert stitched.dtype == np.uint16
        assert np.sum(stitched == 0) == 0  # No black pixels

        # The key test: stitched values should lie between the input values
        assert stitched.min() >= 16000  # Should not go below left image value
        assert stitched.max() <= 24000  # Should not go above right image value

        # Print the actual range for verification (like the user's example)
        print(f"Stitched image range: {stitched.min()} to {stitched.max()}")
        print("Expected range: 16000 to 24000")
