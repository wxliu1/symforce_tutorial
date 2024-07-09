
cmake_minimum_required(VERSION 3.13)

project(test_values)

set (PackageName "TestValues" )

# set(CMAKE_CXX_FLAGS "-std=c++11")

# # Default to C++14
# if(NOT CMAKE_CXX_STANDARD)
#   set(CMAKE_CXX_STANDARD 14)
# endif()

# set(CMAKE_CXX_STANDARD 17)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

# for gdb debug.
# SET(CMAKE_BUILD_TYPE "Debug")
# SET(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -O0 -Wall -g -ggdb")
# the end.

SET(CMAKE_BUILD_TYPE "Release")
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")


MESSAGE(STATUS "aaaa This is ceres library dir " ${CERES_LIBRARIES})
message(STATUS "SYMFORCE_LIBRARY_TYPE=" ${SYMFORCE_LIBRARY_TYPE})
message(STATUS "OpenCV_LIBS=" ${OpenCV_LIBS})

#--------------------------------------------------------
# no use??  I am not certain: 
# link_libraries("/root/SETUP/symforce_install/lib")
#--------------------------------------------------------

include(FetchContent)

# find_package(TBB REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(Ceres REQUIRED)
find_package(fmt REQUIRED)

add_definitions(-DSPDLOG_FMT_EXTERNAL)

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  /root/SETUP/symforce_install/include
  # /root/SETUP/symforce_install/include/spdlog
  # ${EIGEN3_INCLUDE_DIR} # seems to have no affect when comment it.
  )

# link_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib)  
link_directories(/root/SETUP/symforce_install/lib)  

add_executable(test_values test_values.cpp
#   ${CMAKE_CURRENT_SOURCE_DIR}/src/run_dynamic_size.cc
#   ${CMAKE_CURRENT_SOURCE_DIR}/include/gen/measurements.cc
  )

target_link_libraries(test_values Eigen3::Eigen 
  fmt::fmt
  symforce_gen
  symforce_opt
  # /root/SETUP/symforce_install/lib/libsymforce_gen.so
  # /root/SETUP/symforce_install/lib/libsymforce_opt.so
  # spdlog::spdlog
  #/root/SETUP/symforce_install/lib/libspdlog.a
  )  