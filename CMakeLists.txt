cmake_minimum_required(VERSION 3.25)

# Prevent in-source builds
if(CMAKE_SOURCE_DIR STREQUAL CMAKE_BINARY_DIR)
  message(FATAL_ERROR "In-source builds are not allowed. Please create a separate build directory.")
endif()

project(NextCV
  VERSION 0.0.1
  LANGUAGES CXX
  DESCRIPTION "NextCV is like OpenCV but with modern tooling"
)

# Enable compile commands for tooling
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


# Set C++ standard globally (will be overridden by target_compile_features)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Modern compile options and warnings
if(MSVC)
  add_compile_options(/W4 /permissive-)
else()
  add_compile_options(-Wall -Wextra -Wpedantic -Wconversion -Wsign-conversion)
  if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(-Wshadow -Wnon-virtual-dtor -Wold-style-cast -Wcast-align -Wunused -Woverloaded-virtual -Wnull-dereference -Wdouble-promotion -Wformat=2)
  endif()
endif()

# Options
option(NEXTCV_BUILD_EXAMPLES "Build NextCV C++ examples" OFF)
option(NEXTCV_BUILD_PYTHON "Build Python bindings" ON)

# Find Python and pybind11 (compatible with scikit-build-core)
if(NEXTCV_BUILD_PYTHON)
  find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
  # Try to find NumPy component, but don't fail if not found (for scikit-build-core)
  find_package(Python3 COMPONENTS NumPy QUIET)

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
add_subdirectory(nextcv/_cpp/src)

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

# Headers are installed by src/CMakeLists.txt

# Examples are built separately for testing purposes
