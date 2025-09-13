# Core library
add_library(nextcv_core
  core/hello.cpp
  core/utils.cpp
)

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

# Image processing library
add_library(nextcv_image
  image/operations/invert.cpp
  image/operations/threshold.cpp
)

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

# Python bindings (only if Python is enabled)
if(NEXTCV_BUILD_PYTHON)
  pybind11_add_module(nextcv_py MODULE
    bindings/bindings.cpp
  )
  
  target_link_libraries(nextcv_py PRIVATE nextcv_core nextcv_image)
  
  # Ensure the Python module is placed inside the wheel under the nextcv package
  install(TARGETS nextcv_py DESTINATION nextcv)
endif()

