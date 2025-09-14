cmake_minimum_required(VERSION 3.20)

project(NextCV
  VERSION 0.0.1
  LANGUAGES CXX
  DESCRIPTION "NextCV is like OpenCV but with modern tooling"
)

# Set C++ standard globally
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Options
option(NEXTCV_BUILD_EXAMPLES "Build NextCV C++ examples" OFF)
option(NEXTCV_BUILD_PYTHON "Build Python bindings" ON)

# Find Python and pybind11 (compatible with scikit-build-core)
if(NEXTCV_BUILD_PYTHON)
  find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

  # For scikit-build-core, pybind11 is provided via Python
  find_package(pybind11 CONFIG QUIET)
  if(NOT pybind11_FOUND)
    # Fallback: find pybind11 via Python
    execute_process(
      COMMAND ${Python3_EXECUTABLE} -c "import pybind11; print(pybind11.get_cmake_dir())"
      OUTPUT_VARIABLE pybind11_DIR
      OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    find_package(pybind11 CONFIG REQUIRED PATHS ${pybind11_DIR})
  endif()
endif()

# Add source directory
add_subdirectory(src)

# Install/export for C++ consumers
include(CMakePackageConfigHelpers)

install(
  EXPORT NextCVTargets
  NAMESPACE NextCV::
  DESTINATION lib/cmake/NextCV
)

configure_package_config_file(
  ${CMAKE_CURRENT_LIST_DIR}/cmake/NextCVConfig.cmake.in
  ${CMAKE_CURRENT_BINARY_DIR}/NextCVConfig.cmake
  INSTALL_DESTINATION lib/cmake/NextCV
)

install(FILES
  ${CMAKE_CURRENT_BINARY_DIR}/NextCVConfig.cmake
  DESTINATION lib/cmake/NextCV
)

# Install headers for consumers
install(FILES
  ${CMAKE_CURRENT_LIST_DIR}/src/core/hello.hpp
  ${CMAKE_CURRENT_LIST_DIR}/src/image/invert.hpp
  DESTINATION include/nextcv
)

# Examples (integrated, not installed)
if(NEXTCV_BUILD_EXAMPLES)
  add_executable(cpp_example examples/cpp_example.cpp)
  target_link_libraries(cpp_example PRIVATE nextcv_core)
  set_target_properties(cpp_example PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/examples")
endif()
