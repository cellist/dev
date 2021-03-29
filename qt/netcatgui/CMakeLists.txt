# https://github.com/shinnok/netcatgui/
cmake_minimum_required(VERSION 3.13)

project(netcatgui VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Core Gui Widgets Network REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g")

add_executable(ncgui
  ./widgets/ncsessionconnectwidget.cpp
  ./widgets/ncsessionlistenwidget.cpp
  ./widgets/customplaintextedit.cpp
  ./widgets/ncsessionwidget.cpp
  main.cpp
  netcatgui.cpp
  resources/ncgui.rc
  resources/resources.qrc
)

target_include_directories(ncgui PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/widgets)

target_link_libraries(ncgui
  Qt5::Core
  Qt5::Gui
  Qt5::Widgets
  Qt5::Network)
