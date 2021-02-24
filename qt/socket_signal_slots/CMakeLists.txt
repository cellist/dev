# https://www.bogotobogo.com/Qt/Qt5_QTcpSocket_Signals_Slots.php
cmake_minimum_required(VERSION 3.1.0)

project(socket_signal_slots)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Network REQUIRED)

add_executable(
  socket_signal_slots
  main.cpp
  mytcpsocket.cpp
  )

qt5_use_modules(socket_signal_slots Network)

target_link_libraries(socket_signal_slots Qt5::Network)
