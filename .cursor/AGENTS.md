# AGENTS.md

## Cursor Cloud specific instructions

**NextCV** is a Python-first computer vision library with C++ extensions (pybind11 + CMake + Eigen). Single installable package — no services, databases, or APIs.

### System dependencies (pre-installed in VM snapshot)

- `libeigen3-dev` — Eigen3, required at compile time
- `python3-dev` — Python headers required by CMake's `FindPython3`
- `cmake`, `ninja-build` — C++ build system
- `clang-format`, `clang-tidy` — C++ linting/formatting

### Development workflow

- **Install deps + build C++ extensions:** `uv sync`
- **Run tests:** `uv run pytest`
- **Lint (Python):** `uvx ruff check .` / `uvx ruff format --check .`
- **Lint (C++):** `make format` / `make tidy` (requires `make build` first)
- **Pre-commit (all hooks):** `uvx pre-commit run --all-files`
- **Standalone CMake build:** `make build`

### Gotchas

- **Pre-commit install:** run `git config --unset-all core.hooksPath` (if set), then `uvx pre-commit install`.
- **`pre-commit-update` hook** auto-bumps hook versions on every commit. Use `SKIP=pre-commit-update git commit ...` to avoid mixing version bumps into unrelated commits.
- **ruff** is not a direct project dependency — invoke via `uvx ruff`, not `uv run ruff`.
- **Naming warnings (N80x)** from ruff are intentional; mathematical variable names (`A`, `K`, `R`) follow CV/linear algebra conventions. Ignore patterns are configured in `ruff.toml` under `[lint.pep8-naming]`.
- **Ninja not found:** `make build` may fail to locate ninja inside the uv-managed venv. Fix: `cmake --preset uv-env -DCMAKE_MAKE_PROGRAM=$(which ninja)` then `cmake --build --preset uv-env`.
- **C++ source changes** require `uv sync --reinstall` to rebuild the extensions.
