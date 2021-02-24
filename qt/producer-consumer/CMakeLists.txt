# https://www.bogotobogo.com/Qt/Qt5_QThreads_QSemaphore_Producer_Consumer_GuiThread.php
cmake_minimum_required(VERSION 3.1.0)

project(producer_consumer)


set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Widgets REQUIRED)

add_executable(
  producer_consumer
  conproddialog.ui
  main.cpp
  consumer.cpp
  producer.cpp
  conproddialog.cpp
  )

qt5_use_modules(producer_consumer Widgets)

target_link_libraries(producer_consumer Qt5::Widgets)
