# https://www.bogotobogo.com/Qt/Qt5_Asynchronous_QTcpServer_QThreadPool.php
cmake_minimum_required(VERSION 3.13)

project(async-tcpserver VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Network Widgets REQUIRED)

add_executable(async-tcpserver
  main.cpp
  myclient.cpp
  myserver.cpp
  mytask.cpp
)

target_link_libraries(async-tcpserver Qt5::Network Qt5::Widgets)
