#!/usr/bin/env python3
"""Example demonstrating Eigen matrix-vector multiplication in NextCV."""

import numpy as np
import sys
import os

# Add the build directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'build', 'nextcv', '_cpp', 'src'))

from nextcv_py import linalg as cpp_linalg

def main():
    print("NextCV Eigen Matrix-Vector Multiplication Example")
    print("=" * 50)
    
    # Create test data
    rng = np.random.default_rng(42)
    
    # Matrix A: 4x3
    A = rng.standard_normal((4, 3)).astype(np.float32)
    print(f"Matrix A ({A.shape}):")
    print(A)
    print()
    
    # Vector x: 3x1
    x = rng.standard_normal((3,)).astype(np.float32)
    print(f"Vector x ({x.shape}):")
    print(x)
    print()
    
    # Compute using NextCV (Eigen)
    y_cpp = cpp_linalg.matvec(A, x)
    print(f"Result y = A @ x using NextCV (Eigen):")
    print(f"  Shape: {y_cpp.shape}, dtype: {y_cpp.dtype}")
    print(f"  Values: {y_cpp}")
    print()
    
    # Compare with NumPy
    y_np = A @ x
    print(f"Result y = A @ x using NumPy:")
    print(f"  Shape: {y_np.shape}, dtype: {y_np.dtype}")
    print(f"  Values: {y_np}")
    print()
    
    # Verify they match
    if np.allclose(y_cpp, y_np, rtol=1e-6, atol=1e-6):
        print("✓ Results match perfectly!")
    else:
        print("✗ Results differ!")
    
    print()
    print("Example completed successfully!")

if __name__ == "__main__":
    main()