cmake_minimum_required(VERSION 3.20)

project(NextCV LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

option(NEXTCV_BUILD_EXAMPLES "Build NextCV C++ examples" OFF)

# Find Python and pybind11
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)

# Try to find pybind11 in the Python environment first
execute_process(
  COMMAND ${Python3_EXECUTABLE} -c "import pybind11; print(pybind11.get_cmake_dir())"
  OUTPUT_VARIABLE pybind11_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
  RESULT_VARIABLE pybind11_found
)

if(pybind11_found EQUAL 0)
  message(STATUS "Found pybind11 at: ${pybind11_DIR}")
  find_package(pybind11 CONFIG REQUIRED PATHS ${pybind11_DIR} NO_DEFAULT_PATH)
else()
  # Fallback to system pybind11
  find_package(pybind11 CONFIG REQUIRED)
endif()

add_subdirectory(src)

# Install/export for C++ consumers
include(CMakePackageConfigHelpers)

install(TARGETS nextcv_core EXPORT NextCVTargets)

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
  ${CMAKE_CURRENT_LIST_DIR}/src/hello.hpp
  ${CMAKE_CURRENT_LIST_DIR}/src/invert.hpp
  DESTINATION include/nextcv
)

# Examples (not installed)
if(NEXTCV_BUILD_EXAMPLES)
  add_executable(cpp_hello examples/cpp_hello.cpp)
  target_link_libraries(cpp_hello PRIVATE nextcv_core)
  set_target_properties(cpp_hello PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/examples")

  add_executable(cpp_invert examples/cpp_invert.cpp)
  target_link_libraries(cpp_invert PRIVATE nextcv_core)
  set_target_properties(cpp_invert PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/examples")
endif()

