# https://www.boost.org/doc/libs/1_75_0/libs/log/doc/html/log/tutorial/trivial_filtering.html
cmake_minimum_required(VERSION 2.4)

project(logging_with_boost)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DBOOST_LOG_DYN_LINK -g")

FIND_PACKAGE(Boost REQUIRED COMPONENTS log)

if(Boost_FOUND)
  include_directories(${Boost_INCLUDE_DIRS})
  
  add_executable(filtering filtering.cpp)
  target_link_libraries(filtering ${Boost_LIBRARIES})
  
  add_executable(logfile logfile.cpp)
  target_link_libraries(logfile ${Boost_LIBRARIES})
  
  add_executable(trivial trivial.cpp)
  target_link_libraries(trivial ${Boost_LIBRARIES})
endif()
