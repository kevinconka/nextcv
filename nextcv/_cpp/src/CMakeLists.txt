# Modern CMake with automatic source discovery

# Eigen (header-only)
find_package(Eigen3 3.3 REQUIRED NO_MODULE)

# Create NextCV core library
file(GLOB_RECURSE NEXTCV_SOURCES "*.cpp")
list(FILTER NEXTCV_SOURCES EXCLUDE REGEX "bindings/.*")

add_library(nextcv ${NEXTCV_SOURCES})

# Set modern C++ features and include directories
target_compile_features(nextcv PUBLIC cxx_std_17)
target_include_directories(nextcv
  PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
  $<INSTALL_INTERFACE:include/nextcv>
)

# Link Eigen to the core library
target_link_libraries(nextcv PUBLIC Eigen3::Eigen)

# Set library properties
set_target_properties(nextcv PROPERTIES
  EXPORT_NAME nextcv
  VERSION ${PROJECT_VERSION}
  SOVERSION ${PROJECT_VERSION_MAJOR}
  POSITION_INDEPENDENT_CODE ON
)


# Python bindings (only if Python is enabled)
if(NEXTCV_BUILD_PYTHON)
  # Automatically discover all .cpp files in bindings/
  file(GLOB_RECURSE BINDINGS_SOURCES "bindings/*.cpp")

  pybind11_add_module(nextcv_py MODULE ${BINDINGS_SOURCES})

  # Link core library
  target_link_libraries(nextcv_py PRIVATE nextcv pybind11::module pybind11::headers)

  # Add Python include directories for IDE and tooling support
  target_include_directories(nextcv_py SYSTEM PRIVATE
    ${Python3_INCLUDE_DIRS}
  )

  # Set Python module properties
  target_compile_features(nextcv_py PRIVATE cxx_std_17)
  set_target_properties(nextcv_py PROPERTIES
    POSITION_INDEPENDENT_CODE ON
  )

  # Ensure the Python module is placed inside the wheel under the nextcv package
  install(TARGETS nextcv_py DESTINATION nextcv/_cpp)
endif()

# Install the single library
install(TARGETS nextcv
  EXPORT NextCVTargets
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
  COMPONENT libraries
)

# Install headers (dynamic discovery)
install(DIRECTORY .
  DESTINATION include/nextcv
  FILES_MATCHING
  PATTERN "*.hpp"
  PATTERN "*.h"
  PATTERN "bindings" EXCLUDE
  PATTERN "*.cpp" EXCLUDE
  PATTERN "CMakeLists.txt" EXCLUDE
)
