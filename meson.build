project(
  'nextcv',
  'cpp',
  version: '0.0.1',
  default_options: ['cpp_std=c++17'],
)

cpp = meson.get_compiler('cpp')
py_mod = import('python')
fs = import('fs')
py = py_mod.find_installation(pure: false)

warning_args = []
if cpp.get_id() == 'msvc'
  warning_args += ['/W4', '/permissive-']
else
  warning_args += ['-Wall', '-Wextra', '-Wpedantic', '-Wconversion', '-Wsign-conversion']
  if ['gcc', 'clang'].contains(cpp.get_id())
    warning_args += [
      '-Wshadow',
      '-Wnon-virtual-dtor',
      '-Wold-style-cast',
      '-Wcast-align',
      '-Wunused',
      '-Woverloaded-virtual',
      '-Wnull-dereference',
      '-Wdouble-promotion',
      '-Wformat=2',
    ]
  endif
endif

eigen_dep = dependency('eigen3', required: false)
if not eigen_dep.found()
  eigen_include_dir = ''
  foreach candidate : ['/usr/include/eigen3', '/usr/local/include/eigen3', '/opt/homebrew/include/eigen3']
    if fs.is_dir(candidate)
      eigen_include_dir = candidate
      break
    endif
  endforeach
  if eigen_include_dir == ''
    error('Eigen3 not found. Install libeigen3-dev (Linux) or brew install eigen (macOS).')
  endif
  eigen_dep = declare_dependency(include_directories: include_directories(eigen_include_dir))
endif

pybind11_include = run_command(
  py,
  ['-c', 'import pybind11; print(pybind11.get_include())'],
  check: true,
).stdout().strip()
if pybind11_include == ''
  error('Unable to resolve pybind11 include path from Python.')
endif

# Cache pybind11 headers in the Meson build directory so editable rebuilds
# do not rely on temporary PEP 517 build environments.
pybind11_header_cache = join_paths(meson.current_build_dir(), 'pybind11-include')
run_command(
  py,
  [
    '-c',
    'import pathlib, shutil, sys; src = pathlib.Path(sys.argv[1]); dst = pathlib.Path(sys.argv[2]); shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst)',
    pybind11_include,
    pybind11_header_cache,
  ],
  check: true,
)

pybind11_dep = declare_dependency(
  compile_args: ['-I' + pybind11_header_cache],
)

subdir('nextcv/_cpp/src')

install_subdir(
  'nextcv',
  install_dir: py.get_install_dir(),
)
