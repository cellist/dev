cmake_minimum_required(VERSION 2.8.3)

find_package(PythonInterp REQUIRED)
find_package(PythonLibs REQUIRED)
find_package(Boost COMPONENTS python)

include_directories(${Boost_INCLUDE_DIR} ${PYTHON_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIR})

python_add_module(pylib pylib.cpp Bonjour.cpp)
target_link_libraries(pylib ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})
