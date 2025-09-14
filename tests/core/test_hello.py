"""Test core functionality."""

import nextcv.core


def test_hello_cpp():
    """Test the C++ hello function returns a valid greeting."""
    msg = nextcv.core.hello_cpp()
    assert isinstance(msg, str)
    assert msg.startswith("Hello")
    assert "C++" in msg


def test_hello_python():
    """Test the Python hello function returns a valid greeting."""
    msg = nextcv.core.hello_python()
    assert isinstance(msg, str)
    assert msg.startswith("Hello")
    assert "Python" in msg


def test_hello_functions_different():
    """Test that C++ and Python implementations return different messages."""
    cpp_msg = nextcv.core.hello_cpp()
    python_msg = nextcv.core.hello_python()

    assert cpp_msg != python_msg
    assert "C++" in cpp_msg
    assert "Python" in python_msg
