cmake_minimum_required(VERSION 3.13)

project(test_performance)

set (PackageName "TestPerformance" )

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



# ------------------------------------------------------------------------------
# spdlog

# find_package(spdlog 1.9...<1.11 QUIET)
# if (NOT spdlog_FOUND)
#   message(STATUS "spdlog not found, adding with FetchContent")
#   function(add_spdlog)
#     set(SPDLOG_INSTALL ON CACHE INTERNAL "spdlog should create an install target")
#     set(SPDLOG_FMT_EXTERNAL ON CACHE INTERNAL "spdlog shouldn't use its bundled fmtlib")
#     set(CMAKE_POSITION_INDEPENDENT_CODE True)
#     FetchContent_Declare(
#       spdlog
#       URL https://github.com/gabime/spdlog/archive/v1.9.2.zip
#       URL_HASH SHA256=130bd593c33e2e2abba095b551db6a05f5e4a5a19c03ab31256c38fa218aa0a6
#     )
#     FetchContent_MakeAvailable(spdlog)
#   endfunction()

#   add_spdlog()
# else()
#   message(STATUS "spdlog found: ${spdlog_VERSION}")
# endif()

# ------------------------------------------------------------------------------

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  /root/SETUP/symforce_install/include
  # /root/SETUP/symforce_install/include/spdlog
  # ${EIGEN3_INCLUDE_DIR} # seems to have no affect when comment it.
  )

# link_directories(${CMAKE_CURRENT_SOURCE_DIR}/lib)  
link_directories(/root/SETUP/symforce_install/lib)  

add_executable(test_symforce src/symforce_main.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/src/run_dynamic_size.cc
  ${CMAKE_CURRENT_SOURCE_DIR}/include/gen/measurements.cc
  )

target_link_libraries(test_symforce Eigen3::Eigen 
  fmt::fmt
  symforce_gen
  symforce_opt
  # /root/SETUP/symforce_install/lib/libsymforce_gen.so
  # /root/SETUP/symforce_install/lib/libsymforce_opt.so
  # spdlog::spdlog
  #/root/SETUP/symforce_install/lib/libspdlog.a
  )  

add_executable(test_ceres
  src/ceres_main.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/include/gen/measurements.cc
  )

target_link_libraries(test_ceres
  fmt::fmt
  symforce_gen
  symforce_opt
  # Ceres::ceres
  ${CERES_LIBRARIES}
  )


# target_link_libraries(ace_cpp ${OpenCV_LIBS} yaml-cpp jsoncpp mysqlclient tinyxml) # '-lpthread'
# target_include_directories(ace_cpp PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
