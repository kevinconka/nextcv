# Modern CMake with automatic source discovery
# This approach automatically finds all .cpp files without manual updates

# Core library - automatically discover all .cpp files in core/
file(GLOB_RECURSE CORE_SOURCES "core/*.cpp")
add_library(nextcv_core ${CORE_SOURCES})

target_include_directories(nextcv_core
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include>
)

set_target_properties(nextcv_core PROPERTIES
  EXPORT_NAME nextcv
  VERSION ${PROJECT_VERSION}
  SOVERSION ${PROJECT_VERSION_MAJOR}
)

# Image processing library - automatically discover all .cpp files in imgproc/
file(GLOB_RECURSE IMGPROC_SOURCES "imgproc/*.cpp")
add_library(nextcv_imgproc ${IMGPROC_SOURCES})

target_include_directories(nextcv_imgproc
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include>
)

target_link_libraries(nextcv_imgproc PUBLIC nextcv_core)

set_target_properties(nextcv_imgproc PROPERTIES
  EXPORT_NAME nextcv_imgproc
  VERSION ${PROJECT_VERSION}
  SOVERSION ${PROJECT_VERSION_MAJOR}
)

# Features library - automatically discover all .cpp files in features/
file(GLOB_RECURSE FEATURES_SOURCES "features/*.cpp")
if(FEATURES_SOURCES)
  add_library(nextcv_features ${FEATURES_SOURCES})
  
  target_include_directories(nextcv_features
    PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
      $<INSTALL_INTERFACE:include>
  )
  
  target_link_libraries(nextcv_features PUBLIC nextcv_core)
  
  set_target_properties(nextcv_features PROPERTIES
    EXPORT_NAME nextcv_features
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
  )
endif()

# Python bindings (only if Python is enabled)
if(NEXTCV_BUILD_PYTHON)
  # Automatically discover all .cpp files in bindings/
  file(GLOB_RECURSE BINDINGS_SOURCES "bindings/*.cpp")
  
  pybind11_add_module(nextcv_py MODULE ${BINDINGS_SOURCES})
  
  target_link_libraries(nextcv_py PRIVATE nextcv_core nextcv_imgproc)
  
  # Link features if it exists
  if(TARGET nextcv_features)
    target_link_libraries(nextcv_py PRIVATE nextcv_features)
  endif()
  
  # Ensure the Python module is placed inside the wheel under the nextcv package
  install(TARGETS nextcv_py DESTINATION nextcv)
endif()

# Install all libraries
install(TARGETS nextcv_core nextcv_imgproc
  EXPORT NextCVTargets
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
)

if(TARGET nextcv_features)
  install(TARGETS nextcv_features
    EXPORT NextCVTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
  )
endif()

# Install headers
install(DIRECTORY core/ imgproc/ features/
  DESTINATION include
  FILES_MATCHING PATTERN "*.hpp"
)