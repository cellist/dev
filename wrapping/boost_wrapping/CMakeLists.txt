cmake_minimum_required(VERSION 2.8.3)

find_package(PythonInterp REQUIRED)
find_package(PythonLibs REQUIRED)
find_package(Boost COMPONENTS python)

include_directories(${Boost_INCLUDE_DIR} ${PYTHON_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIR})

python_add_module(libcallme libcallme)
target_link_libraries(libcallme ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

# Put the test script where the library is
FILE(COPY try.py DESTINATION .)
