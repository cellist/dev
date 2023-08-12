cmake_minimum_required(VERSION 3.12)

project(Qt6CustomWindowExample)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 COMPONENTS Widgets REQUIRED)

add_executable(Qt6CustomWindowExample
    main.cpp
    customwindow.cpp
    customwindow.h
)

target_link_libraries(Qt6CustomWindowExample PRIVATE Qt6::Widgets)
