cmake_minimum_required(VERSION 3.20)

project(NextCVExamples LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add the src directory to include path
include_directories(../src)

# Create a simple library with just the core functions (no pybind11)
add_library(nextcv_core_simple
  ../src/hello.cpp
  ../src/invert.cpp
)

target_include_directories(nextcv_core_simple
  PUBLIC
    ../src
)

# Build examples
add_executable(cpp_hello cpp_hello.cpp)
target_link_libraries(cpp_hello PRIVATE nextcv_core_simple)

add_executable(cpp_invert cpp_invert.cpp)
target_link_libraries(cpp_invert PRIVATE nextcv_core_simple)