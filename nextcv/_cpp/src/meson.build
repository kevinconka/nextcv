nextcv_cpp_sources = files(
  'core/hello.cpp',
  'image/invert.cpp',
  'linalg/matvec.cpp',
  'postprocessing/nms.cpp',
)

nextcv_core = static_library(
  'nextcv_core',
  nextcv_cpp_sources,
  include_directories: include_directories('.'),
  dependencies: [eigen_dep],
  cpp_args: warning_args,
  pic: true,
)

py.extension_module(
  'nextcv_py',
  files('bindings/bindings.cpp'),
  include_directories: include_directories('.'),
  dependencies: [eigen_dep, pybind11_dep],
  link_with: nextcv_core,
  cpp_args: warning_args,
  install: true,
  subdir: 'nextcv/_cpp',
)
