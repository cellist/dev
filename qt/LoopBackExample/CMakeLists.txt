# https://www.bogotobogo.com/Qt/Qt5_QTcpServer_Client_Server_Loopback_Example.php
cmake_minimum_required(VERSION 3.13)

project(loopback-example VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# find_package(log4cplus REQUIRED)
find_package(Qt5 COMPONENTS Network Widgets REQUIRED)

add_executable(loopback-example
    dialog.ui
    dialog.cpp
    main.cpp
)

target_link_libraries(loopback-example Qt5::Network Qt5::Widgets log4cplus)
