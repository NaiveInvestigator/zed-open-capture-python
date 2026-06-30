cmake_minimum_required(VERSION 3.15)
project(sensor_capture VERSION 1.0)

# ----> Find Python and pybind11
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG QUIET)

if(NOT pybind11_FOUND)
    message(STATUS "pybind11 not found — installing via pip...")
    execute_process(COMMAND ${Python3_EXECUTABLE} -m pip install pybind11 --quiet)
    execute_process(
        COMMAND ${Python3_EXECUTABLE} -m pybind11 --cmakedir
        OUTPUT_VARIABLE pybind11_DIR OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    find_package(pybind11 CONFIG REQUIRED)
endif()
# <---- Find Python and pybind11

# ----> Find system-installed zed-open-capture (after `make install_zed_oc`)
find_path(ZED_OC_INCLUDE_DIR
    NAMES sensorcapture.hpp
    PATHS /usr/local/include /usr/include
    PATH_SUFFIXES zed-open-capture
)

find_library(ZED_OC_LIB
    NAMES zed_open_capture libzed_open_capture
    PATHS /usr/local/lib /usr/lib
)

message(STATUS "Found zed-open-capture headers: ${ZED_OC_INCLUDE_DIR}")
message(STATUS "Found zed-open-capture library:  ${ZED_OC_LIB}")

if(NOT ZED_OC_INCLUDE_DIR OR NOT ZED_OC_LIB)
    message(FATAL_ERROR
        "zed-open-capture not found.\n"
        "  Headers found: ${ZED_OC_INCLUDE_DIR}\n"
        "  Library found: ${ZED_OC_LIB}\n"
        "Run 'make install_zed_oc' first.")
endif()
# <---- Find system-installed zed-open-capture

# ----> Required system deps (used internally by zed-open-capture)
find_package(Threads REQUIRED)
find_library(USB_1_LIB usb-1.0 REQUIRED)
find_library(HIDAPI_LIB hidapi-libusb REQUIRED)

find_path(HIDAPI_INCLUDE_DIR
    NAMES hidapi.h
    PATHS /usr/include /usr/local/include
    PATH_SUFFIXES hidapi
)

if(NOT HIDAPI_INCLUDE_DIR)
    message(FATAL_ERROR "hidapi.h not found — install libhidapi-dev")
endif()

message(STATUS "HIDAPI_INCLUDE_DIR = ${HIDAPI_INCLUDE_DIR}")
# <---- Required system deps

# ----> Build the extension module
pybind11_add_module(sensor_capture src/sensor_bindings.cpp)

target_compile_definitions(sensor_capture PRIVATE
    SENSORS_MOD_AVAILABLE
)

target_include_directories(sensor_capture PRIVATE
    ${ZED_OC_INCLUDE_DIR}
    ${HIDAPI_INCLUDE_DIR}
)

target_link_libraries(sensor_capture PRIVATE
    ${ZED_OC_LIB}
    ${USB_1_LIB}
    ${HIDAPI_LIB}
    Threads::Threads
)

target_compile_features(sensor_capture PRIVATE cxx_std_14)
# <---- Build the extension module

# ----> Install into Python's site-packages
execute_process(
    COMMAND ${Python3_EXECUTABLE} -c
        "import site; print(site.getsitepackages()[0])"
    OUTPUT_VARIABLE PYTHON_SITE_PACKAGES
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

install(TARGETS sensor_capture
    LIBRARY DESTINATION ${PYTHON_SITE_PACKAGES}
)
# <---- Install into Python's site-packages

# ----> Install the Python wrapper package alongside the extension
install(DIRECTORY ${CMAKE_SOURCE_DIR}/src/python/zed_sensors
    DESTINATION ${PYTHON_SITE_PACKAGES}
)
# <---- Install the Python wrapper package
