cmake_minimum_required(VERSION 3.3)
project(google_post)

# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES google_post.cxx)
add_executable(google_post ${SOURCE_FILES})
target_link_libraries(google_post curl)
