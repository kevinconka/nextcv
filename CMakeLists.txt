cmake_minimum_required(VERSION 3.20)

project(NextCV LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

option(NEXTCV_BUILD_EXAMPLES "Build NextCV C++ examples" OFF)

find_package(pybind11 CONFIG REQUIRED)

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

