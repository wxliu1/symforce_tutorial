cmake_minimum_required(VERSION 3.14)
project(test_symengine)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

message(STATUS "SYMFORCE_LIBRARY_TYPE=" ${SYMFORCE_LIBRARY_TYPE})

find_package(Eigen3 REQUIRED)

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}/include
  /root/SETUP/symforce_install/include
  )

link_directories(/root/SETUP/symforce_install/lib)  

add_executable(test_symengine
  ${CMAKE_CURRENT_SOURCE_DIR}/src/test_symengine.cpp
#   ${CMAKE_CURRENT_SOURCE_DIR}/include/gen/measurements.cc
  )

target_link_libraries(test_symengine Eigen3::Eigen 
#   fmt::fmt
  symforce_gen
  symforce_opt

  # /root/SETUP/symforce_install/lib/libsymforce_gen.so
  # /root/SETUP/symforce_install/lib/libsymforce_opt.so
  # spdlog::spdlog
  #/root/SETUP/symforce_install/lib/libspdlog.a
  )