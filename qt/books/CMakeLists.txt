cmake_minimum_required(VERSION 3.1.0)

# Largely borrowed from:
# https://code.qt.io/cgit/qt/qtbase.git/tree/examples/sql/books
#
project(books VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

if(CMAKE_VERSION VERSION_LESS "3.7.0")
    set(CMAKE_INCLUDE_CURRENT_DIR ON)
endif()

find_package(Qt5 COMPONENTS Sql Widgets REQUIRED)

# Configure Qt
SET( QT_USE_QTSQL TRUE )

add_executable(books
  bookwindow.ui
  bookwindow.cpp
  bookdelegate.cpp
  main.cpp
  books.qrc
)

qt5_use_modules(books Sql Widgets)

target_link_libraries(books Qt5::Widgets)
