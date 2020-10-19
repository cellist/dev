set(CURSES_NEED_NCURSES TRUE)

cmake_minimum_required(VERSION 2.4)

project(ncurses_demo)

add_executable(ncurses_demo demo.cc)

target_link_libraries(ncurses_demo ncurses++ ncurses)
