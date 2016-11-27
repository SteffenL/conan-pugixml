cmake_minimum_required(VERSION 2.8 FATAL_ERROR)

project(pugixml)
set(TARGET_NAME pugixml)

option(BUILD_SHARED_LIBS "Build shared instead of static library" OFF)

# Setup Conan
include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()


file(GLOB_RECURSE SOURCES "pugixml/src/*.cpp")

if(BUILD_SHARED_LIBS)
    set(LINK_TYPE SHARED)
else()
    set(LINK_TYPE STATIC)
endif()

add_library(${TARGET_NAME} ${LINK_TYPE} ${SOURCES})

target_include_directories(${TARGET_NAME} PRIVATE "pugixml/src")
