#  https://www.bogotobogo.com/Qt/Qt5_QTcpServer_Client_Server_Loopback_Example.php
cmake_minimum_required(VERSION 3.13)

project(network-download VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)

find_package(Qt5 COMPONENTS Network REQUIRED)

add_executable(download
    downloadmanager.cpp
    main.cpp
)

target_link_libraries(download Qt5::Network)
