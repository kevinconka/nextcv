# AGENTS.md

## Cursor Cloud specific instructions

**NextCV** is a Python-first computer vision library with C++ extensions (pybind11 + CMake + Eigen). It is a single installable package, not a monorepo; there are no services, databases, or APIs.

### System dependencies

The following must be installed before `uv sync` will succeed (already present in the VM snapshot):

- `libeigen3-dev` — C++ linear algebra library required at compile time
- `python3-dev` — Python development headers required by CMake's `FindPython3`
- `cmake` — build system for C++ extensions (pre-installed on most systems)
- `clang-format`, `clang-tidy` — C++ linting/formatting (used by Makefile and pre-commit)
- `ninja-build` — required for standalone CMake builds via `make build`

### Development workflow

- **Install deps + build C++ extensions:** `uv sync`
- **Run tests:** `uv run pytest` (32 tests, ~1s)
- **Lint (Python):** `uvx ruff check .` / `uvx ruff format --check .`
- **Lint (C++):** `make format` (clang-format) / `make tidy` (clang-tidy, requires `make build` first)
- **Pre-commit:** `uvx pre-commit run --all-files`
- **Standalone CMake build:** `make build` (uses `cmake --preset uv-env`; if ninja is not found, run `cmake --preset uv-env -DCMAKE_MAKE_PROGRAM=$(which ninja)` then `cmake --build --preset uv-env`)

### Gotchas

- `ruff` is not a direct project dependency; use `uvx ruff` (not `uv run ruff`).
- Pre-existing ruff naming warnings (N80x) are intentional — mathematical variable names (`A`, `K`, `R`) follow CV/linear algebra conventions.
- The Makefile `build` target may fail to locate ninja from within the uv-managed venv. Work around by passing `-DCMAKE_MAKE_PROGRAM=$(which ninja)` explicitly to `cmake --preset uv-env`.
- `uv sync` performs an editable install including C++ compilation via scikit-build-core. If C++ sources change, re-run `uv sync --reinstall` to rebuild.
