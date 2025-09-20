cmake_minimum_required(VERSION 3.20)
project(NextCVExamples)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find NextCV (installed via pip install)
find_package(PkgConfig REQUIRED)
pkg_check_modules(NEXTCV REQUIRED nextcv)

# Build the C++ example
add_executable(cpp_example cpp_example.cpp)

# Link NextCV
target_include_directories(cpp_example PRIVATE ${NEXTCV_INCLUDE_DIRS})
target_link_libraries(cpp_example PRIVATE ${NEXTCV_LIBRARIES})
target_compile_options(cpp_example PRIVATE ${NEXTCV_CFLAGS_OTHER})
