cmake_minimum_required(VERSION 3.5)

project(LoginDialogApp LANGUAGES CXX)

find_package(Qt6 COMPONENTS Widgets REQUIRED)

set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

add_executable(LoginDialogApp
    main.cpp
    login_dialog.h
    login_dialog.cpp
    credentials.h
)

target_link_libraries(LoginDialogApp PRIVATE Qt6::Widgets)
