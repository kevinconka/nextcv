# NextCV

**NextCV is like OpenCV but with modern tooling.** A minimal, experimental CV library built with C++ + Python, packaged via scikit-build-core, managed with uv, and usable from both Python and C++.

## Python (uv)

```bash
uv sync
uv run python -c "import nextcv; print(nextcv.hello())"
uv build   # builds sdist + wheel using PEP 517 backend
```

Example script: `examples/python_example.py`

```bash
uv run python examples/python_example.py
```

## C++

```bash
cmake -B build -DNEXTCV_BUILD_EXAMPLES=ON
cmake --build build
./build/examples/cpp_example
```

## Python usage

```python
import nextcv
import numpy as np

print(nextcv.hello())

# Invert pixel values using numpy arrays
data = np.array([0, 127, 255], dtype=np.uint8)
inverted = nextcv.invert(data)
print(inverted)  # [255 128   0]
```

## C++ usage

```cmake
find_package(NextCV REQUIRED)
add_executable(app main.cpp)
target_link_libraries(app PRIVATE NextCV::nextcv)
```

## Packaging checks

```bash
uv build
python - <<'PY'
import glob, zipfile, tarfile
whl = glob.glob('dist/*.whl')[0]
print('Wheel contents:')
with zipfile.ZipFile(whl) as z:
    z.printdir()
sdist = glob.glob('dist/*.tar.gz')[0]
print('\nSDist contents (first 50 entries):')
with tarfile.open(sdist) as t:
    for m in t.getmembers()[:50]:
        print(m.name)
PY
```

## 🤝 Contributing to NextCV

Welcome to the NextCV party! 🎉 Whether you're a Python wizard, a C++ sorcerer, or someone who just thinks computer vision is pretty neat, we'd love to have you contribute. Here's your roadmap to becoming a NextCV contributor:

### 🚀 Quick Start for Contributors

**Python Developers** (the easy path):
```bash
# Clone and set up
git clone <your-fork-url>
cd nextcv
uv sync

# Make your changes, then test
uv run python -c "import nextcv; print(nextcv.hello())"
uv run python examples/python_example.py
uv run pytest tests/ -v

# Build and verify
uv build
```

**C++ Developers** (the fun path):
```bash
# Clone and build
git clone <your-fork-url>
cd nextcv
cmake -B build -DNEXTCV_BUILD_EXAMPLES=ON
cmake --build build

# Test your changes
./build/examples/cpp_example
```

### 🎯 What We're Looking For

**Python Side:**
- New computer vision algorithms (the more creative, the better!)
- Performance improvements to existing functions
- Better error handling and user experience
- Documentation improvements (we love good docs!)
- Test cases that make us go "wow, we didn't think of that"

**C++ Side:**
- Core algorithm implementations
- Performance optimizations (make it go brrrr 🚀)
- Memory management improvements
- Cross-platform compatibility fixes
- Modern C++ features that make the code cleaner

**Both Sides:**
- Bug fixes (the unsung heroes of open source)
- Documentation that makes complex things simple
- Examples that make people go "I can do that too!"
- CI/CD improvements
- Code that's so clean it sparkles ✨

### 🛠️ Development Workflow

1. **Fork & Branch**: Create a feature branch with a name that tells a story
   - `feature/awesome-blur-algorithm`
   - `fix/memory-leak-in-invert`
   - `docs/improve-readme-clarity`

2. **Code with Style**: 
   - Python: We use `ruff` for linting (it's fast and opinionated)
   - C++: Follow the existing style, and if you're feeling fancy, run `clang-format`
   - Write tests. Seriously. We love tests.

3. **Test Everything**:
   ```bash
   # Python tests
   uv run pytest tests/ -v --cov=nextcv
   
   # C++ build test
   cmake -B build -DNEXTCV_BUILD_EXAMPLES=ON
   cmake --build build
   ./build/examples/cpp_example
   
   # Full integration test
   uv build
   ```

4. **Submit PR**: Write a description that makes us excited to review your code!

### 🧪 Testing Philosophy

We believe in testing that actually catches bugs (revolutionary, we know). Here's our testing strategy:

**Python Tests:**
- Unit tests for individual functions
- Integration tests with real numpy arrays
- Edge case testing (empty arrays, weird shapes, etc.)
- Performance regression tests

**C++ Tests:**
- The example executable serves as our integration test
- Memory leak detection (we use sanitizers when possible)
- Cross-platform compatibility testing

**Golden Rule**: If your change breaks existing functionality, we'll gently ask you to fix it. If it adds new functionality, we'll probably high-five you through the internet.

### 🎨 Code Style Guidelines

**Python:**
- Use `ruff` for formatting and linting
- Type hints are encouraged (but not mandatory)
- Docstrings should explain the "why" not just the "what"
- Variable names should be self-explanatory

**C++:**
- Follow modern C++ practices (C++17+)
- Use `const` everywhere it makes sense
- Prefer `auto` when the type is obvious
- Write code that your future self will thank you for

### 🐛 Bug Reports & Feature Requests

**Found a bug?** 🐛
- Check if it's already reported
- Provide a minimal reproduction case
- Include your system info (OS, Python version, etc.)
- Bonus points for including a fix!

**Want a feature?** ✨
- Open an issue and tell us why it would be awesome
- If you're feeling ambitious, implement it and submit a PR
- We love creative ideas that push the boundaries of what's possible

### 🏗️ Architecture Decisions

**Why C++ + Python?**
- C++ for performance-critical algorithms
- Python for ease of use and rapid prototyping
- pybind11 for seamless integration between the two

**Why scikit-build-core?**
- Modern Python packaging with CMake
- Better than the old setuptools approach
- Handles the complexity so we don't have to

**Why uv?**
- Fast dependency resolution
- Better lock file management
- It's the future of Python packaging (and we're here for it)

### 🎉 Recognition

Contributors get:
- Their name in the README (if they want it)
- Eternal gratitude from the maintainers
- The satisfaction of making computer vision more accessible
- Bragging rights about contributing to "the next OpenCV"

### 💬 Community

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub discussions for questions and ideas
- **Code Review**: We review every PR with care and constructive feedback

### 🚨 Breaking Changes

We're still in early development (v0.0.1), so breaking changes are expected. We'll:
- Document them clearly in release notes
- Provide migration guides when possible
- Give advance notice for major changes
- Try to make the pain as minimal as possible

---

**Ready to contribute?** We can't wait to see what you'll build! 🚀

## Notes

- Build backend: `scikit_build_core.build` (auto-requires CMake/Ninja inside build env)
- `pybind11` is a build dependency only

## License

Apache-2.0. See `LICENSE`.

