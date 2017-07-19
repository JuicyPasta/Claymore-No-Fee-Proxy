###########################################################
## PROJECT
###########################################################

cmake_minimum_required(VERSION 3.2)
project(tssx)

set(CMAKE_MACOSX_RPATH 1)

add_compile_options(-pthread)

###########################################################
## CONFIGURATION
###########################################################

add_compile_options(-g -O3 -Wall -DDEBUG)
# add_compile_options(-DNDEBUG)

# Apple's C standard library already contains the math functions
if(APPLE)
    add_compile_options(-std=c11)
else()
    add_compile_options(-std=gnu11)
    link_libraries(m)
endif()

link_libraries(pthread)

###########################################################
## INCLUDES
###########################################################

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

###########################################################
## SUBDIRECTORIES
###########################################################

add_subdirectory(test_area)

