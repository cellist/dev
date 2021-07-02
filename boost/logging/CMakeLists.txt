# https://theboostcpplibraries.com/boost.log
cmake_minimum_required(VERSION 2.4)

project(logging_with_boost)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DBOOST_LOG_DYN_LINK -g")

FIND_PACKAGE(Boost REQUIRED COMPONENTS log)

if(Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS}) 
    add_executable(trivial trivial.cpp)
    target_link_libraries(trivial ${Boost_LIBRARIES})
endif()
