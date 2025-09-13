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

# Image processing library - automatically discover all .cpp files in image/
file(GLOB_RECURSE IMAGE_SOURCES "image/*.cpp")
add_library(nextcv_image ${IMAGE_SOURCES})

target_include_directories(nextcv_image
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include>
)

target_link_libraries(nextcv_image PUBLIC nextcv_core)

set_target_properties(nextcv_image PROPERTIES
  EXPORT_NAME nextcv_image
  VERSION ${PROJECT_VERSION}
  SOVERSION ${PROJECT_VERSION_MAJOR}
)

# Postprocessing library - automatically discover all .cpp files in postprocessing/
file(GLOB_RECURSE POSTPROC_SOURCES "postprocessing/*.cpp")
if(POSTPROC_SOURCES)
  add_library(nextcv_postprocessing ${POSTPROC_SOURCES})
  
  target_include_directories(nextcv_postprocessing
    PUBLIC
      $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
      $<INSTALL_INTERFACE:include>
  )
  
  target_link_libraries(nextcv_postprocessing PUBLIC nextcv_core)
  
  set_target_properties(nextcv_postprocessing PROPERTIES
    EXPORT_NAME nextcv_postprocessing
    VERSION ${PROJECT_VERSION}
    SOVERSION ${PROJECT_VERSION_MAJOR}
  )
endif()

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
  
  target_link_libraries(nextcv_py PRIVATE nextcv_core nextcv_image)
  
  # Link optional libraries if they exist
  if(TARGET nextcv_postprocessing)
    target_link_libraries(nextcv_py PRIVATE nextcv_postprocessing)
  endif()
  
  if(TARGET nextcv_features)
    target_link_libraries(nextcv_py PRIVATE nextcv_features)
  endif()
  
  # Ensure the Python module is placed inside the wheel under the nextcv package
  install(TARGETS nextcv_py DESTINATION nextcv)
endif()

# Install all libraries
install(TARGETS nextcv_core nextcv_image
  EXPORT NextCVTargets
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
)

if(TARGET nextcv_postprocessing)
  install(TARGETS nextcv_postprocessing
    EXPORT NextCVTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
  )
endif()

if(TARGET nextcv_features)
  install(TARGETS nextcv_features
    EXPORT NextCVTargets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
  )
endif()

# Install headers
install(DIRECTORY core/ image/ postprocessing/ features/
  DESTINATION include
  FILES_MATCHING PATTERN "*.hpp"
)