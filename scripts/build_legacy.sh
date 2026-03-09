#!/usr/bin/env bash
# Build legacy wheel packages for older Python versions (3.6–3.8).
#
# This script captures the build process that was previously handled by the
# macos-13 GitHub Actions runner (the last runner with Python 3.6 support).
# Use it on any machine where a compatible Python version is installed.
#
# Prerequisites (install for your OS):
#   - Python 3.6, 3.7, or 3.8  (e.g. via pyenv, deadsnakes PPA, or system package)
#   - CMake >= 3.15             (brew install cmake / apt install cmake)
#   - Ninja                     (brew install ninja / apt install ninja-build)
#   - Eigen3                    (brew install eigen / apt install libeigen3-dev)
#   - pip for the target Python
#
# Usage:
#   ./scripts/build_legacy.sh                      # uses python3 from PATH
#   PYTHON=python3.6 ./scripts/build_legacy.sh     # explicit interpreter
#   PYTHON=python3.8 ./scripts/build_legacy.sh     # explicit interpreter
#
# The resulting .whl file is written to ./dist/

set -euo pipefail

PYTHON="${PYTHON:-python3}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
DIST_DIR="${ROOT_DIR}/dist"

# Validate that the requested Python exists
if ! command -v "${PYTHON}" &>/dev/null; then
    echo "Error: '${PYTHON}' not found. Set the PYTHON env var to the correct interpreter." >&2
    exit 1
fi

PY_VERSION="$("${PYTHON}" --version 2>&1)"
echo "Building legacy wheel with ${PY_VERSION}..."

# Backup pyproject.toml and restore it on exit (even on error)
PYPROJECT="${ROOT_DIR}/pyproject.toml"
PYPROJECT_BACKUP="$(mktemp)"
cp "${PYPROJECT}" "${PYPROJECT_BACKUP}"
trap 'cp "${PYPROJECT_BACKUP}" "${PYPROJECT}"; rm -f "${PYPROJECT_BACKUP}"; echo "Restored pyproject.toml."' EXIT

echo "Switching to legacy build configuration (pyproject.legacy.toml)..."
cp "${ROOT_DIR}/pyproject.legacy.toml" "${PYPROJECT}"

# Install the build-time dependencies that scikit-build needs
echo "Installing build dependencies..."
"${PYTHON}" -m pip install --upgrade \
    "scikit-build>=0.10" \
    "pybind11>=2.10" \
    "setuptools-scm<=8" \
    "wheel" \
    "cmake" \
    "ninja"

# Build the wheel (no transitive deps — only the package itself)
mkdir -p "${DIST_DIR}"
echo "Building wheel..."
"${PYTHON}" -m pip wheel --no-deps -w "${DIST_DIR}" "${ROOT_DIR}"

echo ""
echo "Build complete. Wheel written to ${DIST_DIR}/:"
ls "${DIST_DIR}"/*.whl
