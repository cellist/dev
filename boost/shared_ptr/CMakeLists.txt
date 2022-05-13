cmake_minimum_required (VERSION 3.8)

find_package(Boost REQUIRED)

file(GLOB SRCS "*.cxx")
file(GLOB HEADERS "*.h")

add_executable(shared_ptr_demo ${SRCS})
