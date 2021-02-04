cmake_minimum_required(VERSION 3.13)
project(gtkmm_hello_world-project CXX)

# the `pkg_check_modules` function is created with this call
find_package(PkgConfig REQUIRED)

pkg_check_modules (GTKMM   gtkmm-3.0>=3.20)

add_executable(gtkmm_hello_world main.cc helloworld.cc)

target_link_libraries(gtkmm_hello_world ${GTKMM_LIBRARIES})
target_include_directories(gtkmm_hello_world PUBLIC ${GTKMM_INCLUDE_DIRS})
target_compile_options(gtkmm_hello_world PUBLIC ${GTKMM_CFLAGS_OTHER})
