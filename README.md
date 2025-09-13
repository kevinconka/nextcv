# NextCV

**NextCV is like OpenCV but with modern tooling.** A minimal, experimental CV library built with C++ + Python, packaged via scikit-build-core, managed with uv, and usable from both Python and C++.

## Python (uv)

```bash
uv sync
uv run python -c "import nextcv; print(nextcv.hello())"
uv build   # builds sdist + wheel using PEP 517 backend
```

Or install directly from git:
```bash
pip install git+https://github.com/your-username/nextcv.git
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

## 🤝 Contributing

Welcome to the NextCV party! 🎉 Whether you're a Python wizard, a C++ sorcerer, or someone who just thinks computer vision is pretty neat, we'd love to have you contribute.

### Quick Start

**Python:**
```bash
git clone <your-fork-url>
cd nextcv
uv sync
uv run pytest tests/ -v
uv build
```

**C++:**
```bash
git clone <your-fork-url>
cd nextcv
cmake -B build -DNEXTCV_BUILD_EXAMPLES=ON
cmake --build build
./build/examples/cpp_example
```

### What We Want
- New CV algorithms (the more creative, the better!)
- Performance improvements (make it go brrrr 🚀)
- Bug fixes (the unsung heroes of open source)
- Tests that make us go "wow, we didn't think of that"
- Code that's so clean it sparkles ✨

### Development
1. Fork & create a feature branch
2. Write tests (seriously, we love tests)
3. Run `uv run pytest tests/ -v` and `cmake --build build`
4. Submit a PR that makes us excited to review it!

**Ready to contribute?** We can't wait to see what you'll build! 🚀

## Notes

- Build backend: `scikit_build_core.build` (auto-requires CMake/Ninja inside build env)
- `pybind11` is a build dependency only

## License

Apache-2.0. See `LICENSE`.

