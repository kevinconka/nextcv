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
  )
endfunction()

# Dynamic library discovery - automatically find all library directories
file(GLOB LIBRARY_DIRS RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} "*/")
list(FILTER LIBRARY_DIRS EXCLUDE REGEX "bindings")

# Create libraries dynamically
foreach(LIB_DIR ${LIBRARY_DIRS})
  # Remove trailing slash
  string(REGEX REPLACE "/$" "" LIB_NAME ${LIB_DIR})

  # Check if directory has .cpp files
  file(GLOB_RECURSE LIB_SOURCES "${LIB_DIR}/*.cpp")
  if(LIB_SOURCES)
    # Determine dependencies based on library name
    set(DEPS "")
    if(NOT ${LIB_NAME} STREQUAL "core")
      set(DEPS "nextcv_core")
    endif()

    # Create the library
    create_nextcv_library(nextcv_${LIB_NAME} "${LIB_DIR}/*.cpp" "${DEPS}")
  endif()
endforeach()


# Python bindings (only if Python is enabled)
if(NEXTCV_BUILD_PYTHON)
  # Automatically discover all .cpp files in bindings/
  file(GLOB_RECURSE BINDINGS_SOURCES "bindings/*.cpp")

  pybind11_add_module(nextcv_py MODULE ${BINDINGS_SOURCES})

  # Set modern target properties for Python module
  target_compile_features(nextcv_py PRIVATE cxx_std_17)
  target_link_libraries(nextcv_py PRIVATE nextcv_core nextcv_image)

  # Link optional libraries if they exist
  if(TARGET nextcv_postprocessing)
    target_link_libraries(nextcv_py PRIVATE nextcv_postprocessing)
  endif()

  # Set target properties using modern syntax
  set_target_properties(nextcv_py PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
  )

  # Ensure the Python module is placed inside the wheel under the nextcv package
  install(TARGETS nextcv_py DESTINATION nextcv/_cpp)
endif()

# Dynamic library installation - automatically install all created libraries
get_property(ALL_TARGETS DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} PROPERTY BUILDSYSTEM_TARGETS)
foreach(TARGET ${ALL_TARGETS})
  if(TARGET ${TARGET} AND ${TARGET} MATCHES "^nextcv_")
    list(APPEND INSTALL_TARGETS ${TARGET})
  endif()
endforeach()

# Install all libraries with modern syntax
install(TARGETS ${INSTALL_TARGETS}
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
