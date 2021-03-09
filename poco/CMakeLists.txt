#https://code.qt.io/cgit/qt/qtbase.git/tree/examples/qtconcurrent/wordcount?h=5.15

cmake_minimum_required(VERSION 3.13)

project(pocothreads VERSION 1.0.0 LANGUAGES CXX)

find_package(Poco REQUIRED Foundation)

add_executable(pocothreads thread.cc)

target_link_libraries(pocothreads Poco::Foundation)
