cmake_minimum_required(VERSION 3.20)
project(NextCVExamples)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find NextCV headers using Python to locate the package
execute_process(
  COMMAND python -c "import nextcv; import os; print(os.path.join(os.path.dirname(nextcv.__file__), '_cpp', 'src'))"
  OUTPUT_VARIABLE NEXTCV_INCLUDE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
  RESULT_VARIABLE NEXTCV_FOUND
)

if(NOT NEXTCV_FOUND EQUAL 0)
  message(FATAL_ERROR "NextCV not found. Make sure NextCV is installed via pip.")
endif()

# Find Eigen3
find_package(Eigen3 3.3 REQUIRED NO_MODULE)

# Build the C++ example
add_executable(cpp_example cpp_example.cpp)

# Link NextCV headers and Eigen3
target_include_directories(cpp_example PRIVATE ${NEXTCV_INCLUDE_DIR})
target_link_libraries(cpp_example PRIVATE Eigen3::Eigen)
