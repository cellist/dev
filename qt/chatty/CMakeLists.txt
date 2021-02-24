# https://riptutorial.com/qt/example/29873/tcp-client
cmake_minimum_required(VERSION 3.1.0)

project(chatting)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt5 COMPONENTS Network Widgets REQUIRED)

#
# Chat Server application
#
add_executable(chat_server
  server_window.ui
  server_window.cpp
  server.cpp
)

qt5_use_modules(chat_server Network Widgets)

target_link_libraries(chat_server Qt5::Network Qt5::Widgets)

#
# Chat Client application
#
add_executable(chat_client
  client_window.ui
  client_window.cpp
  client.cpp
)

qt5_use_modules(chat_client Network Widgets)

target_link_libraries(chat_client Qt5::Network Qt5::Widgets)
