"""Core utility functions for NextCV."""

from .._internal.nextcv_py import get_version as _get_version, get_build_info as _get_build_info


def get_version() -> str:
    """Get the NextCV version string.
    
    Returns:
        str: Version string (e.g., "0.1.0")
    """
    return _get_version()


def get_build_info() -> str:
    """Get build information string.
    
    Returns:
        str: Build information including version
    """
    return _get_build_info()