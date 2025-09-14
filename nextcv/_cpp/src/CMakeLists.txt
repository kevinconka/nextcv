# Modern CMake with automatic source discovery
# This approach automatically finds all .cpp files without manual updates

# Function to create a NextCV library target with consistent properties
function(create_nextcv_library target_name source_pattern dependencies)
  # Discover source files
  file(GLOB_RECURSE SOURCES "${source_pattern}")

  # Create the library
  add_library(${target_name} ${SOURCES})

  # Set modern target properties
  target_compile_features(${target_name} PUBLIC cxx_std_17)
  target_include_directories(${target_name}
    PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include/nextcv>
  )

  # Link dependencies
  if(dependencies)
    target_link_libraries(${target_name} PUBLIC ${dependencies})
  endif()

  # Set target properties using modern syntax
  set_target_properties(${target_name} PROPERTIES
    EXPORT_NAME ${target_name}
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
    POSITION_INDEPENDENT_CODE ON
  )
endfunction()

# Single library approach - automatically discover all .cpp files
file(GLOB_RECURSE ALL_SOURCES "*.cpp")
list(FILTER ALL_SOURCES EXCLUDE REGEX "bindings/.*")

# Create include directory structure for development
file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/nextcv)
file(COPY core image postprocessing DESTINATION ${CMAKE_CURRENT_BINARY_DIR}/nextcv/)

# Create single library with all sources
add_library(nextcv ${ALL_SOURCES})

# Set modern target properties
target_compile_features(nextcv PUBLIC cxx_std_17)
target_include_directories(nextcv
  PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
  $<INSTALL_INTERFACE:include/nextcv>
)

# Set target properties using modern syntax
set_target_properties(nextcv PROPERTIES
  EXPORT_NAME nextcv
  VERSION ${PROJECT_VERSION}
  SOVERSION ${PROJECT_VERSION_MAJOR}
  CXX_STANDARD 17
  CXX_STANDARD_REQUIRED ON
  CXX_EXTENSIONS OFF
  POSITION_INDEPENDENT_CODE ON
)


# Python bindings (only if Python is enabled)
if(NEXTCV_BUILD_PYTHON)
  # Automatically discover all .cpp files in bindings/
  file(GLOB_RECURSE BINDINGS_SOURCES "bindings/*.cpp")

  pybind11_add_module(nextcv_py MODULE ${BINDINGS_SOURCES})

  # Set modern target properties for Python module
  target_compile_features(nextcv_py PRIVATE cxx_std_17)
  target_link_libraries(nextcv_py PRIVATE nextcv)

  # Set target properties using modern syntax
  set_target_properties(nextcv_py PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
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
