cmake_minimum_required(VERSION 2.4)

project(csv_with_boost)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DBOOST_LOG_DYN_LINK -g")

FIND_PACKAGE(Boost REQUIRED COMPONENTS system)

if(Boost_FOUND)
  include_directories(${Boost_INCLUDE_DIRS})
  
  add_executable(simple_example_2 simple_example_2.cpp)
  target_link_libraries(simple_example_2 ${Boost_LIBRARIES})
endif()
