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
./build/examples/cpp_hello
```

## Python usage

```python
import nextcv
print(nextcv.hello())
print(nextcv.invert(b"\x00\x7f\xff"))
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

## Notes

- Build backend: `scikit_build_core.build` (auto-requires CMake/Ninja inside build env)
- `pybind11` is a build dependency only

## License

Apache-2.0. See `LICENSE`.

