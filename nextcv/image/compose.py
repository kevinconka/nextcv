"""Image composition utilities.

Functions here combine two or more images into a single result.
Includes operations like:
- Simple overlays and alpha blending
- Masked compositing
- Pairwise stitching (left/right)
- Multi-image panorama creation

These functions typically perform geometric alignment, warping,
and optional seam blending to produce seamless composites.
"""
