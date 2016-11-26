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

if(BUILD_SHARED_LIBS)
    # https://github.com/zeux/pugixml/issues/113
    if(MSVC)
        set_property(TARGET ${TARGET_NAME} APPEND PROPERTY COMPILE_DEFINITIONS "PUGIXML_API=__declspec(dllexport)")
    endif()
endif()

target_include_directories(${TARGET_NAME} PRIVATE "pugixml/src")
