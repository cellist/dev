# https://www.bogotobogo.com/Qt/Qt5_QNetworkRequest_Http_File_Download.php
cmake_minimum_required(VERSION 3.13)

project(httpDownload VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Network Widgets REQUIRED)

add_executable(httpDownload
  main.cpp
  httpdownload.cpp
  httpdownload.ui
)

target_link_libraries(httpDownload Qt5::Network Qt5::Widgets)
